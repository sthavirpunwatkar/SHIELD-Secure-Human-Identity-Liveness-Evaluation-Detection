"""
SHIELD – Verification Session Manager

Manages active verification sessions, combining the
:class:`ChallengeSession` state machine with the
:class:`TemporalValidator` integrity checker.

Security features:
* Per-frame SHA-256 hashing → detects duplicate (replayed) frames.
* Session TTL → stale sessions are automatically expired.
* Per-client rate limiting → prevents brute-force attempts.
"""

import hashlib
import time
import uuid
from typing import Dict, Optional, Set

import numpy as np

from inference.challenge_engine import ChallengeSession
from inference.temporal_validator import TemporalValidator


class VerificationSession:
    """A single end-to-end liveness-verification session.

    Bundles a :class:`ChallengeSession` (action challenges) and a
    :class:`TemporalValidator` (frame-integrity checks) together with
    per-session bookkeeping such as frame hashing and expiry.

    :param session_ttl: Time-to-live for this session in seconds.
    :param num_challenges: Number of challenges passed to
        :class:`ChallengeSession`.
    :param timeout_per_challenge: Per-challenge timeout in seconds.
    """

    def __init__(
        self,
        session_ttl: float = 120.0,
        num_challenges: int = 3,
        timeout_per_challenge: float = 5.0,
    ) -> None:
        self.session_id: str = str(uuid.uuid4())
        self.created_at: float = time.time()
        self.expires_at: float = self.created_at + session_ttl

        self.challenge_session: ChallengeSession = ChallengeSession(
            num_challenges=num_challenges,
            timeout_per_challenge=timeout_per_challenge,
        )
        self.temporal_validator: TemporalValidator = TemporalValidator()

        self.frame_count: int = 0
        self.frame_hashes: Set[str] = set()
        self._base_identity_signature = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_expired(self) -> bool:
        """Check whether this session has exceeded its TTL.

        :return: ``True`` when the current time is past ``expires_at``.
        """
        return time.time() > self.expires_at

    def add_frame(self, frame: np.ndarray, landmarks=None) -> Dict:
        """Ingest a single video frame for verification.

        Performs the following in order:

        1. Expiry check.
        2. Duplicate-frame detection (SHA-256 of raw bytes).
        3. Forwards the frame to ``temporal_validator``.

        :param frame: BGR image as ``np.ndarray``.
        :return: Dict with keys ``accepted``, ``duplicate``, ``expired``,
            ``frame_number``, and ``reason``.
        """
        result: Dict = {
            "accepted": False,
            "duplicate": False,
            "expired": False,
            "frame_number": self.frame_count,
            "reason": "",
        }

        if self.is_expired():
            result["expired"] = True
            result["reason"] = "session_expired"
            return result

        if frame is None or frame.size == 0:
            result["reason"] = "empty_frame"
            return result

        # --- Duplicate detection via SHA-256 hash ---
        frame_hash = hashlib.sha256(frame.tobytes()).hexdigest()
        if frame_hash in self.frame_hashes:
            result["duplicate"] = True
            result["reason"] = "duplicate_frame_detected"
            return result

        # --- Identity Consistency Check ---
        if landmarks is not None:
            signature = self._calculate_landmark_signature(landmarks)
            if signature is not None:
                if self._base_identity_signature is None:
                    self._base_identity_signature = signature
                else:
                    distance = np.linalg.norm(self._base_identity_signature - signature)
                    if distance > 0.50:
                        result["reason"] = "identity_swap_detected"
                        return result

        self.frame_hashes.add(frame_hash)
        self.frame_count += 1
        result["frame_number"] = self.frame_count

        # --- Forward to temporal validator ---
        self.temporal_validator.add_frame(frame)

        result["accepted"] = True
        result["reason"] = "frame_accepted"
        return result

    def _get_landmark_coords(self, landmark):
        if hasattr(landmark, "x"):
            return np.array([landmark.x, landmark.y, landmark.z])
        elif isinstance(landmark, dict):
            return np.array([landmark.get("x", 0.0), landmark.get("y", 0.0), landmark.get("z", 0.0)])
        else:
            return np.array([landmark[0], landmark[1], landmark[2]])

    def _calculate_landmark_signature(self, landmarks):
        try:
            # MediaPipe standard indices:
            # 1: nose tip, 33: left eye corner, 263: right eye corner
            # 152: chin, 61: left mouth corner, 291: right mouth corner
            p_nose = self._get_landmark_coords(landmarks[1])
            p_leye = self._get_landmark_coords(landmarks[33])
            p_reye = self._get_landmark_coords(landmarks[263])
            p_chin = self._get_landmark_coords(landmarks[152])
            p_lmouth = self._get_landmark_coords(landmarks[61])
            p_rmouth = self._get_landmark_coords(landmarks[291])
            
            interocular = np.linalg.norm(p_leye - p_reye)
            if interocular == 0:
                return None
                
            d_nose_leye = np.linalg.norm(p_nose - p_leye) / interocular
            d_nose_reye = np.linalg.norm(p_nose - p_reye) / interocular
            d_mouth_width = np.linalg.norm(p_lmouth - p_rmouth) / interocular
            d_face_height = np.linalg.norm(p_nose - p_chin) / interocular
            
            return np.array([d_nose_leye, d_nose_reye, d_mouth_width, d_face_height])
        except Exception:
            return None

    def get_final_result(self) -> Dict:
        """Compile the combined verification result.

        Merges the challenge score from ``challenge_session`` with the
        temporal integrity checks from ``temporal_validator``.

        :return: Dict with ``session_id``, ``challenge_score``,
            ``frame_coherence``, ``background_consistency``,
            ``frame_count``, ``duplicate_frames_detected``, and
            overall ``verdict``.
        """
        challenge_score = self.challenge_session.get_challenge_score()

        coherent, coherence_score = (
            self.temporal_validator.check_frame_coherence()
        )
        bg_ok, bg_score = (
            self.temporal_validator.check_background_consistency()
        )

        # Final verdict: challenge must pass AND temporal checks must hold
        temporal_ok = coherent and bg_ok
        overall_pass = challenge_score >= 0.5 and temporal_ok

        return {
            "session_id": self.session_id,
            "challenge_score": challenge_score,
            "challenge_status": self.challenge_session.get_session_status(),
            "frame_coherence": {
                "is_coherent": coherent,
                "score": coherence_score,
            },
            "background_consistency": {
                "is_consistent": bg_ok,
                "score": bg_score,
            },
            "temporal_valid": temporal_ok,
            "frame_count": self.frame_count,
            "duplicate_frames_detected": len(self.frame_hashes) < self.frame_count,
            "verdict": "Live" if overall_pass else "Spoof",
        }


class SessionManager:
    """Registry of active :class:`VerificationSession` instances.

    Handles session lifecycle (create / lookup / expire) and enforces
    per-client rate limits to mitigate brute-force attacks.

    :param session_ttl: Default time-to-live for new sessions (seconds).
    :param max_sessions: Hard cap on the number of concurrent sessions.
    :param max_attempts_per_ip: Maximum sessions a single ``client_id``
        may create before being rate-limited.
    """

    def __init__(
        self,
        session_ttl: float = 120.0,
        max_sessions: int = 100,
        max_attempts_per_ip: int = 10,
    ) -> None:
        self.session_ttl: float = session_ttl
        self.max_sessions: int = max_sessions
        self.max_attempts_per_ip: int = max_attempts_per_ip

        # session_id → VerificationSession
        self._sessions: Dict[str, VerificationSession] = {}
        # client_id → list of creation timestamps
        self._rate_tracker: Dict[str, list] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_session(
        self, client_id: Optional[str] = None
    ) -> VerificationSession:
        """Create and register a new verification session.

        :param client_id: Optional client identifier (IP / device-id)
            for rate-limit tracking.
        :return: A fresh :class:`VerificationSession`.
        :raises RuntimeError: If ``max_sessions`` has been reached or the
            client is rate-limited.
        """
        # Housekeeping – prune stale sessions first
        self.cleanup_expired()

        if len(self._sessions) >= self.max_sessions:
            raise RuntimeError(
                f"Maximum concurrent sessions ({self.max_sessions}) reached."
            )

        if client_id and not self.check_rate_limit(client_id):
            raise RuntimeError(
                f"Rate limit exceeded for client '{client_id}'."
            )

        session = VerificationSession(session_ttl=self.session_ttl)
        self._sessions[session.session_id] = session

        # Track creation for rate limiting
        if client_id:
            self._rate_tracker.setdefault(client_id, []).append(time.time())

        return session

    def get_session(self, session_id: str) -> Optional[VerificationSession]:
        """Look up a session by its ID.

        :param session_id: UUID string of the desired session.
        :return: The :class:`VerificationSession` if found and not expired,
            otherwise ``None``.
        """
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.is_expired():
            del self._sessions[session_id]
            return None
        return session

    def cleanup_expired(self) -> int:
        """Remove all expired sessions from the registry.

        :return: Number of sessions removed.
        """
        expired_ids = [
            sid for sid, sess in self._sessions.items() if sess.is_expired()
        ]
        for sid in expired_ids:
            del self._sessions[sid]
        return len(expired_ids)

    def check_rate_limit(self, client_id: str) -> bool:
        """Check whether a client_id is within its rate limit.

        Only sessions created within the current ``session_ttl`` window
        count towards the limit (older entries are pruned).

        :param client_id: Client identifier.
        :return: ``True`` if the client may create another session.
        """
        timestamps = self._rate_tracker.get(client_id, [])
        if not timestamps:
            return True

        # Prune entries older than the TTL window
        cutoff = time.time() - self.session_ttl
        recent = [t for t in timestamps if t > cutoff]
        self._rate_tracker[client_id] = recent

        return len(recent) < self.max_attempts_per_ip

    @property
    def active_session_count(self) -> int:
        """Number of currently active (non-expired) sessions."""
        return len(self._sessions)


# ------------------------------------------------------------------
# Quick smoke-test
# ------------------------------------------------------------------
if __name__ == "__main__":
    manager = SessionManager(session_ttl=60, max_sessions=10, max_attempts_per_ip=5)

    # Create a session
    session = manager.create_session(client_id="127.0.0.1")
    print(f"Created session: {session.session_id}")
    print(f"Expires at: {time.ctime(session.expires_at)}")

    # Simulate adding a frame
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    frame_result = session.add_frame(dummy_frame)
    print(f"Frame result: {frame_result}")

    # Try adding the same frame again (duplicate)
    dup_result = session.add_frame(dummy_frame)
    print(f"Duplicate result: {dup_result}")

    # Lookup
    found = manager.get_session(session.session_id)
    print(f"Session lookup: {'found' if found else 'not found'}")

    # Final result
    final = session.get_final_result()
    print(f"Final result: {final}")

    # Cleanup
    removed = manager.cleanup_expired()
    print(f"Expired sessions removed: {removed}")
    print(f"Active sessions: {manager.active_session_count}")
