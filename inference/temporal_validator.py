"""
SHIELD – Temporal Validator

Validates that challenge responses are temporally consistent and not
pre-recorded.  Analyses are purely frame-based (OpenCV + NumPy) so
they add negligible latency to the inference pipeline.

Three complementary checks:
1. **Frame coherence** – consecutive frames should be similar; jump-cuts
   or scene changes suggest video splicing.
2. **Response timing** – sub-human reaction times suggest automation.
3. **Background consistency** – the periphery of the frame should stay
   stable; drastic changes suggest scene substitution or replay attack.
"""

import time
from collections import deque
from typing import List, Optional, Tuple

import cv2
import numpy as np


class TemporalValidator:
    """Lightweight temporal-consistency checker for liveness verification.

    Maintains a sliding window of recent frames and their timestamps so
    that coherence, timing, and background stability can be assessed
    without keeping the full video in memory.

    Usage::

        validator = TemporalValidator()
        for frame in stream:
            validator.add_frame(frame)
            ok, score = validator.check_frame_coherence()
            if not ok:
                print("Possible replay / splice detected")
    """

    # Maximum number of frames retained for analysis.
    _MAX_BUFFER_SIZE: int = 10

    def __init__(
        self,
        min_response_time: float = 0.3,
        max_frame_diff_threshold: float = 50.0,
    ) -> None:
        """Initialise the TemporalValidator.

        :param min_response_time: Minimum credible human response time
            (seconds).  Responses faster than this are flagged as
            suspicious automation.
        :param max_frame_diff_threshold: Maximum mean-absolute-difference
            between consecutive frames before a *jump-cut* is declared
            (pixel-intensity scale 0–255).
        """
        if min_response_time <= 0:
            raise ValueError("min_response_time must be > 0")
        if max_frame_diff_threshold <= 0:
            raise ValueError("max_frame_diff_threshold must be > 0")

        self.min_response_time: float = min_response_time
        self.max_frame_diff_threshold: float = max_frame_diff_threshold

        # Sliding buffer of (frame_grey, timestamp) tuples.
        self._frame_buffer: deque = deque(maxlen=self._MAX_BUFFER_SIZE)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_frame(self, frame: np.ndarray, timestamp: Optional[float] = None) -> None:
        """Store a frame (converted to greyscale) and its timestamp.

        :param frame: BGR or greyscale image (``np.ndarray``).
        :param timestamp: POSIX timestamp; defaults to ``time.time()``.
        """
        if frame is None or frame.size == 0:
            return

        ts = timestamp if timestamp is not None else time.time()

        if len(frame.shape) == 3 and frame.shape[2] == 3:
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            grey = frame.copy()

        self._frame_buffer.append((grey, ts))

    def check_frame_coherence(self) -> Tuple[bool, float]:
        """Compare the last two frames to detect jump-cuts or scene changes.

        Uses mean absolute difference (MAD) between greyscale frames.
        If the difference exceeds ``max_frame_diff_threshold`` the pair
        is considered *incoherent* (possible splice / replay).

        :return: ``(is_coherent, similarity_score)`` where
            ``similarity_score`` is the MAD value (lower = more similar).
            If fewer than two frames are available returns ``(True, 0.0)``.
        """
        if len(self._frame_buffer) < 2:
            return True, 0.0

        prev_frame, _ = self._frame_buffer[-2]
        curr_frame, _ = self._frame_buffer[-1]

        # Resize to match if shapes differ (e.g. camera resolution change)
        if prev_frame.shape != curr_frame.shape:
            curr_frame = cv2.resize(
                curr_frame,
                (prev_frame.shape[1], prev_frame.shape[0]),
            )

        diff = cv2.absdiff(prev_frame, curr_frame)
        mean_diff: float = float(np.mean(diff))

        is_coherent = mean_diff <= self.max_frame_diff_threshold
        return is_coherent, round(mean_diff, 4)

    def check_response_timing(
        self, challenge_start_time: float
    ) -> Tuple[bool, str]:
        """Validate that the user's response time is humanly plausible.

        :param challenge_start_time: POSIX timestamp when the challenge
            was first displayed to the user.
        :return: ``(is_valid, reason)`` – ``is_valid`` is ``False`` when
            the elapsed time is shorter than ``min_response_time``
            (suspicious automation).
        """
        if not self._frame_buffer:
            return False, "no_frames_received"

        _, latest_ts = self._frame_buffer[-1]
        elapsed = latest_ts - challenge_start_time

        if elapsed < self.min_response_time:
            return False, (
                f"response_too_fast ({elapsed:.3f}s < "
                f"{self.min_response_time:.3f}s)"
            )

        return True, f"timing_ok ({elapsed:.3f}s)"

    def check_background_consistency(self) -> Tuple[bool, float]:
        """Check that the background region stays stable across stored frames.

        The *background* is approximated by the outer border of each
        frame (top/bottom 15 % of rows, left/right 15 % of columns).
        We compute the MAD between the first and last background patches
        in the buffer; a large difference signals scene substitution.

        :return: ``(is_consistent, bg_diff_score)`` where
            ``bg_diff_score`` is the mean absolute difference of the
            background regions.  Returns ``(True, 0.0)`` when fewer
            than two frames are available.
        """
        if len(self._frame_buffer) < 2:
            return True, 0.0

        first_frame, _ = self._frame_buffer[0]
        last_frame, _ = self._frame_buffer[-1]

        # Resize to match if shapes differ
        if first_frame.shape != last_frame.shape:
            last_frame = cv2.resize(
                last_frame,
                (first_frame.shape[1], first_frame.shape[0]),
            )

        first_bg = self._extract_background_mask(first_frame)
        last_bg = self._extract_background_mask(last_frame)

        diff = cv2.absdiff(first_bg, last_bg)
        bg_diff: float = float(np.mean(diff))

        # Reuse the same threshold – background should be even more stable
        is_consistent = bg_diff <= self.max_frame_diff_threshold
        return is_consistent, round(bg_diff, 4)

    def reset(self) -> None:
        """Clear the internal frame buffer."""
        self._frame_buffer.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_background_mask(grey: np.ndarray) -> np.ndarray:
        """Extract the background border region of a greyscale frame.

        Keeps only the outer 15 % on each side and blacks-out the centre,
        yielding an image of the same shape that represents just the
        background.

        :param grey: Single-channel greyscale image.
        :return: Background-only greyscale image (same shape).
        """
        h, w = grey.shape[:2]
        margin_y = max(int(h * 0.15), 1)
        margin_x = max(int(w * 0.15), 1)

        mask = np.zeros_like(grey)
        # Top band
        mask[:margin_y, :] = grey[:margin_y, :]
        # Bottom band
        mask[h - margin_y :, :] = grey[h - margin_y :, :]
        # Left band
        mask[:, :margin_x] = grey[:, :margin_x]
        # Right band
        mask[:, w - margin_x :] = grey[:, w - margin_x :]
        return mask


# ------------------------------------------------------------------
# Quick smoke-test
# ------------------------------------------------------------------
if __name__ == "__main__":
    validator = TemporalValidator()

    # Simulate a short burst of similar frames
    base = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    for i in range(5):
        noisy = base.copy()
        # Add a tiny bit of Gaussian noise to simulate real camera jitter
        noise = np.random.normal(0, 2, noisy.shape).astype(np.int16)
        noisy = np.clip(noisy.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        validator.add_frame(noisy)

    coherent, score = validator.check_frame_coherence()
    print(f"Frame coherence: coherent={coherent}, diff={score}")

    bg_ok, bg_score = validator.check_background_consistency()
    print(f"Background consistency: ok={bg_ok}, diff={bg_score}")

    timing_ok, reason = validator.check_response_timing(time.time() - 1.0)
    print(f"Response timing: ok={timing_ok}, reason={reason}")

    validator.reset()
    print("Buffer reset – TemporalValidator ready.")
