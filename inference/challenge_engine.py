"""
SHIELD – Active Challenge-Response Engine

Server-side state machine that generates, tracks, and scores
challenge sequences for liveness verification.

Each ChallengeSession picks N unique random actions (e.g. BLINK,
TURN_LEFT, SMILE …) and walks the user through them one at a time.
Per-challenge timeout and retry limits keep the interaction bounded.
"""

import random
import time
from enum import Enum
from typing import Dict, List, Optional


class ChallengeType(Enum):
    """Enumeration of supported liveness-challenge actions."""

    BLINK = "blink"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    NOD_UP = "nod_up"
    NOD_DOWN = "nod_down"
    SMILE = "smile"
    OPEN_MOUTH = "open_mouth"


class ChallengeSession:
    """State machine for a single active-challenge verification session.

    Generates a random sequence of *unique* challenges, tracks the
    user's progress through them, and computes a final score (0 → 1).

    Typical lifecycle::

        session = ChallengeSession(num_challenges=3, timeout_per_challenge=5.0)
        while session.get_current_challenge() is not None:
            session.start_current_challenge()
            # … receive frames, run action recognition …
            result = session.submit_frame_result(action_detected=True)
            if result["session_complete"]:
                break

        score = session.get_challenge_score()
    """

    def __init__(
        self,
        num_challenges: int = 3,
        timeout_per_challenge: float = 5.0,
        max_retries: int = 2,
    ) -> None:
        """Initialises a ChallengeSession and generates its challenge sequence.

        :param num_challenges: Number of unique challenges to present.
            Clamped to the total number of available ChallengeType values.
        :param timeout_per_challenge: Seconds allowed per challenge before
            it counts as a failure.
        :param max_retries: Maximum retries permitted per individual challenge.
        """
        if num_challenges < 1:
            raise ValueError("num_challenges must be >= 1")
        if timeout_per_challenge <= 0:
            raise ValueError("timeout_per_challenge must be > 0")

        self.num_challenges: int = min(num_challenges, len(ChallengeType))
        self.timeout_per_challenge: float = timeout_per_challenge
        self.max_retries: int = max_retries

        # Ordered list of challenges the user must complete.
        self.challenges: List[ChallengeType] = self._generate_random_sequence(
            self.num_challenges
        )
        # Index into self.challenges for the current challenge.
        self._current_index: int = 0

        # Per-challenge bookkeeping
        self._challenge_start_time: Optional[float] = None
        self._retries_used: int = 0
        self._passed: int = 0
        self._failed: int = 0
        self._completed: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current_challenge(self) -> Optional[ChallengeType]:
        """Returns the ChallengeType the user should perform next.

        :return: Current ChallengeType, or ``None`` if the session is
            already complete (all challenges attempted).
        """
        if self._completed or self._current_index >= len(self.challenges):
            return None
        return self.challenges[self._current_index]

    def start_current_challenge(self) -> None:
        """Marks the start time for the current challenge.

        Must be called before ``submit_frame_result`` so that the
        timeout clock begins.

        :raises RuntimeError: If the session has already completed.
        """
        if self._completed:
            raise RuntimeError("Session is already complete.")
        self._challenge_start_time = time.time()
        self._retries_used = 0

    def submit_frame_result(self, action_detected: bool) -> Dict:
        """Process a single frame's action-recognition result.

        Call this for each analysed frame while the current challenge is
        active.  The method handles timeout checks, retry logic, and
        session advancement.

        :param action_detected: ``True`` when the frame analysis confirms
            the requested action was performed.
        :return: Status dict with keys:
            * ``challenge_passed`` – this challenge was just passed
            * ``challenge_failed`` – this challenge was just failed
            * ``session_complete`` – all challenges finished
            * ``next_challenge`` – the upcoming ChallengeType (or ``None``)
            * ``challenge_score`` – running score (0.0 – 1.0)
        """
        result: Dict = {
            "challenge_passed": False,
            "challenge_failed": False,
            "session_complete": False,
            "next_challenge": None,
            "challenge_score": self.get_challenge_score(),
        }

        if self._completed:
            result["session_complete"] = True
            return result

        # --- Check for timeout first ---
        if self.is_timed_out():
            self._retries_used += 1
            if self._retries_used > self.max_retries:
                # Challenge failed – move on
                self._failed += 1
                result["challenge_failed"] = True
                self._advance()
            else:
                # Allow retry – restart the timer
                self._challenge_start_time = time.time()

            result["session_complete"] = self._completed
            result["next_challenge"] = (
                self.get_current_challenge().value
                if self.get_current_challenge()
                else None
            )
            result["challenge_score"] = self.get_challenge_score()
            return result

        # --- Normal frame evaluation ---
        if action_detected:
            self._passed += 1
            result["challenge_passed"] = True
            self._advance()
        # If not detected, we simply wait for the next frame (no action).

        result["session_complete"] = self._completed
        result["next_challenge"] = (
            self.get_current_challenge().value
            if self.get_current_challenge()
            else None
        )
        result["challenge_score"] = self.get_challenge_score()
        return result

    def get_challenge_score(self) -> float:
        """Returns the running challenge score as passed / total.

        :return: Float between 0.0 and 1.0.
        """
        total = self._passed + self._failed
        if total == 0:
            return 0.0
        return round(self._passed / total, 4)

    def get_session_status(self) -> Dict:
        """Returns the full session state, suitable for WebSocket responses.

        :return: Dictionary with challenge list, progress, score, and
            completion flag.
        """
        return {
            "challenges": [c.value for c in self.challenges],
            "current_index": self._current_index,
            "current_challenge": (
                self.get_current_challenge().value
                if self.get_current_challenge()
                else None
            ),
            "passed": self._passed,
            "failed": self._failed,
            "retries_used": self._retries_used,
            "score": self.get_challenge_score(),
            "completed": self._completed,
            "timed_out": self.is_timed_out() if not self._completed else False,
        }

    def is_timed_out(self) -> bool:
        """Checks whether the current challenge has exceeded its timeout.

        :return: ``True`` if time elapsed since ``start_current_challenge``
            exceeds ``timeout_per_challenge``.  Always ``False`` if the
            timer has not been started yet.
        """
        if self._challenge_start_time is None:
            return False
        return (time.time() - self._challenge_start_time) > self.timeout_per_challenge

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _advance(self) -> None:
        """Move to the next challenge or mark the session as complete."""
        self._current_index += 1
        self._challenge_start_time = None
        self._retries_used = 0
        if self._current_index >= len(self.challenges):
            self._completed = True

    @staticmethod
    def _generate_random_sequence(n: int) -> List[ChallengeType]:
        """Selects *n* unique random ChallengeTypes.

        :param n: Number of challenges to pick (≤ len(ChallengeType)).
        :return: List of unique ChallengeType members in random order.
        """
        pool = list(ChallengeType)
        return random.sample(pool, k=min(n, len(pool)))


# ------------------------------------------------------------------
# Quick smoke-test
# ------------------------------------------------------------------
if __name__ == "__main__":
    session = ChallengeSession(num_challenges=3, timeout_per_challenge=5.0)
    print(f"Generated challenges: {[c.value for c in session.challenges]}")
    print(f"Session status: {session.get_session_status()}")

    # Simulate passing each challenge immediately
    while session.get_current_challenge() is not None:
        current = session.get_current_challenge()
        print(f"\n→ Challenge: {current.value}")
        session.start_current_challenge()
        result = session.submit_frame_result(action_detected=True)
        print(f"  Result: {result}")

    print(f"\nFinal score: {session.get_challenge_score()}")
    print(f"Final status: {session.get_session_status()}")
