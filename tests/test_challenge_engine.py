"""
SHIELD – Sprint D: Active Challenge-Response Test Suite

Comprehensive pytest tests for the three core Sprint D modules:
  1. inference.challenge_engine.ChallengeSession
  2. inference.temporal_validator.TemporalValidator
  3. inference.session_manager.SessionManager / VerificationSession

Uses very small timeouts (0.01 s) so that timeout-related tests
complete in milliseconds.  Dummy frames are generated with NumPy.
"""

import time

import numpy as np
import pytest

from inference.challenge_engine import ChallengeSession, ChallengeType
from inference.temporal_validator import TemporalValidator
from inference.session_manager import SessionManager, VerificationSession


# =====================================================================
# Helper utilities
# =====================================================================

def _make_frame(value: int = 128, shape: tuple = (480, 640, 3)) -> np.ndarray:
    """Create a uniform BGR dummy frame filled with *value*."""
    return np.full(shape, value, dtype=np.uint8)


def _make_noisy_frame(
    base_value: int = 128,
    noise_std: float = 2.0,
    shape: tuple = (480, 640, 3),
) -> np.ndarray:
    """Create a BGR dummy frame with slight Gaussian noise."""
    base = np.full(shape, base_value, dtype=np.uint8)
    noise = np.random.normal(0, noise_std, shape).astype(np.int16)
    return np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)


# =====================================================================
# 1 – ChallengeSession Tests
# =====================================================================

class TestChallengeSequenceUniqueness:
    """Verify that the generated challenge sequence contains unique items."""

    def test_challenge_sequence_uniqueness(self):
        """Each challenge in a session's sequence must be unique."""
        session = ChallengeSession(num_challenges=5, timeout_per_challenge=5.0)
        assert len(session.challenges) == len(set(session.challenges)), (
            "Duplicate challenges detected in sequence"
        )


class TestChallengeSequenceRandomness:
    """Verify that sequences are randomised across sessions."""

    def test_challenge_sequence_randomness(self):
        """10 independent sessions should NOT all produce the same order."""
        sequences = []
        for _ in range(10):
            session = ChallengeSession(num_challenges=3, timeout_per_challenge=5.0)
            sequences.append(tuple(session.challenges))

        unique_sequences = set(sequences)
        assert len(unique_sequences) > 1, (
            "All 10 sessions produced the identical challenge sequence — "
            "randomisation is not working"
        )


class TestChallengePassAll:
    """Simulate passing every challenge and verify a perfect score."""

    def test_challenge_pass_all(self):
        """Passing all challenges should yield score == 1.0."""
        session = ChallengeSession(num_challenges=3, timeout_per_challenge=5.0)

        while session.get_current_challenge() is not None:
            session.start_current_challenge()
            result = session.submit_frame_result(action_detected=True)

        assert session.get_challenge_score() == 1.0
        assert result["session_complete"] is True


class TestChallengeFailAll:
    """Simulate failing every challenge via timeout and verify score == 0.0."""

    def test_challenge_fail_all(self):
        """Timing out on all challenges (with max_retries=0) → score == 0.0."""
        session = ChallengeSession(
            num_challenges=3,
            timeout_per_challenge=0.01,
            max_retries=0,
        )

        for _ in range(session.num_challenges):
            if session.get_current_challenge() is None:
                break
            session.start_current_challenge()
            time.sleep(0.02)  # exceed 0.01 s timeout
            session.submit_frame_result(action_detected=False)

        assert session.get_challenge_score() == 0.0


class TestChallengePartialPass:
    """Pass 2 out of 3 challenges and verify the resulting score."""

    def test_challenge_partial_pass(self):
        """Passing 2/3 challenges should yield score ≈ 0.6667."""
        session = ChallengeSession(
            num_challenges=3,
            timeout_per_challenge=0.01,
            max_retries=0,
        )

        for i in range(session.num_challenges):
            if session.get_current_challenge() is None:
                break
            session.start_current_challenge()

            if i < 2:
                # Pass the first two challenges (requires frames_required consecutive frames)
                for _ in range(session.frames_required):
                    session.submit_frame_result(action_detected=True)
            else:
                # Fail the third via timeout
                time.sleep(0.02)
                session.submit_frame_result(action_detected=False)

        score = session.get_challenge_score()
        assert abs(score - 2.0 / 3.0) < 0.01, (
            f"Expected score ≈ 0.6667, got {score}"
        )


class TestChallengeTimeoutDetection:
    """Verify that `is_timed_out()` fires correctly."""

    def test_challenge_timeout_detection(self):
        """Starting a challenge and sleeping past the timeout should flag it."""
        session = ChallengeSession(
            num_challenges=1,
            timeout_per_challenge=0.01,
        )
        session.start_current_challenge()
        time.sleep(0.02)

        assert session.is_timed_out() is True


class TestChallengeRetryLogic:
    """Verify that retries are consumed before a challenge is marked failed."""

    def test_challenge_retry_logic(self):
        """With max_retries=2, three timeouts are needed to fail a challenge."""
        session = ChallengeSession(
            num_challenges=1,
            timeout_per_challenge=0.01,
            max_retries=2,
        )
        session.start_current_challenge()

        # First timeout → retry 1 (timer resets)
        time.sleep(0.02)
        r1 = session.submit_frame_result(action_detected=False)
        # It sets challenge_failed=True to notify UI, but keeps session active
        assert r1["challenge_failed"] is True
        assert r1["next_challenge"] is not None

        # Second timeout → retry 2 (timer resets)
        time.sleep(0.02)
        r2 = session.submit_frame_result(action_detected=False)
        assert r2["challenge_failed"] is True
        assert r2["next_challenge"] is not None

        # Third timeout → retries exhausted → fail and move on
        time.sleep(0.02)
        r3 = session.submit_frame_result(action_detected=False)
        assert r3["challenge_failed"] is True
        assert r3["session_complete"] is True


# =====================================================================
# 2 – TemporalValidator Tests
# =====================================================================

class TestTemporalFrameCoherence:
    """Test frame coherence detection."""

    def test_temporal_frame_coherence(self):
        """Two similar frames → coherent; one wildly different → incoherent."""
        validator = TemporalValidator(max_frame_diff_threshold=10.0)

        # Two nearly identical frames should be coherent
        frame_a = _make_frame(value=128)
        frame_b = _make_noisy_frame(base_value=128, noise_std=1.0)
        validator.add_frame(frame_a)
        validator.add_frame(frame_b)

        coherent, score = validator.check_frame_coherence()
        assert coherent is True, f"Similar frames flagged incoherent (diff={score})"

        # Add a wildly different frame
        frame_wild = _make_frame(value=10)
        validator.add_frame(frame_wild)

        coherent, score = validator.check_frame_coherence()
        assert coherent is False, f"Wildly different frame not flagged (diff={score})"


class TestTemporalResponseTiming:
    """Test that suspiciously fast responses are flagged."""

    def test_temporal_response_timing(self):
        """A response faster than min_response_time should be invalid."""
        validator = TemporalValidator(min_response_time=0.3)

        challenge_start = time.time()
        # Add a frame almost immediately (well within 0.3 s)
        frame = _make_frame()
        validator.add_frame(frame, timestamp=challenge_start + 0.05)

        is_valid, reason = validator.check_response_timing(challenge_start)
        assert is_valid is False, f"Fast response not flagged: {reason}"
        assert "response_too_fast" in reason


class TestTemporalBackgroundConsistency:
    """Test background consistency detection."""

    def test_temporal_background_consistency(self):
        """Frames with the same background should be consistent."""
        validator = TemporalValidator(max_frame_diff_threshold=10.0)

        # Two frames with the same background
        frame_a = _make_frame(value=100)
        frame_b = _make_noisy_frame(base_value=100, noise_std=1.0)
        validator.add_frame(frame_a)
        validator.add_frame(frame_b)

        consistent, bg_score = validator.check_background_consistency()
        assert consistent is True, (
            f"Same-background frames flagged inconsistent (diff={bg_score})"
        )


# =====================================================================
# 3 – SessionManager Tests
# =====================================================================

class TestSessionManagerCreate:
    """Test basic session creation and lookup."""

    def test_session_manager_create(self):
        """Creating a session should make it retrievable by ID."""
        manager = SessionManager(session_ttl=60.0)
        session = manager.create_session(client_id="test_client")

        assert session is not None
        assert manager.get_session(session.session_id) is session
        assert manager.active_session_count == 1


class TestSessionManagerDuplicateFrame:
    """Test duplicate-frame detection in a VerificationSession."""

    def test_session_manager_duplicate_frame(self):
        """Submitting the same frame twice should flag the second as duplicate."""
        session = VerificationSession(session_ttl=60.0)
        frame = _make_frame(value=200)

        first = session.add_frame(frame)
        assert first["accepted"] is True
        assert first["duplicate"] is False

        second = session.add_frame(frame)
        assert second["accepted"] is False
        assert second["duplicate"] is True
        assert "duplicate" in second["reason"]


class TestSessionManagerRateLimit:
    """Test per-client rate limiting."""

    def test_session_manager_rate_limit(self):
        """Creating sessions up to the rate limit should block the next one."""
        limit = 3
        manager = SessionManager(
            session_ttl=60.0,
            max_sessions=100,
            max_attempts_per_ip=limit,
        )
        client = "192.168.1.42"

        # Create exactly `limit` sessions — should succeed
        for _ in range(limit):
            manager.create_session(client_id=client)

        # Next creation should raise RuntimeError
        with pytest.raises(RuntimeError, match="Rate limit exceeded"):
            manager.create_session(client_id=client)


# =====================================================================
# Standalone smoke-test
# =====================================================================

if __name__ == "__main__":
    print("--- SHIELD Sprint D: Challenge Engine Test Suite ---\n")

    # Quick manual runs of each test class
    test_classes = [
        TestChallengeSequenceUniqueness,
        TestChallengeSequenceRandomness,
        TestChallengePassAll,
        TestChallengeFailAll,
        TestChallengePartialPass,
        TestChallengeTimeoutDetection,
        TestChallengeRetryLogic,
        TestTemporalFrameCoherence,
        TestTemporalResponseTiming,
        TestTemporalBackgroundConsistency,
        TestSessionManagerCreate,
        TestSessionManagerDuplicateFrame,
        TestSessionManagerRateLimit,
    ]

    for cls in test_classes:
        instance = cls()
        for name in dir(instance):
            if name.startswith("test_"):
                print(f"Running {cls.__name__}.{name} ... ", end="")
                try:
                    getattr(instance, name)()
                    print("PASSED")
                except AssertionError as exc:
                    print(f"FAILED: {exc}")
                except Exception as exc:
                    print(f"ERROR: {exc}")

    print("\n--- Test Suite Complete ---")
