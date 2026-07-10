import av
import numpy as np
import time
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class DecodedFrame:
    image: np.ndarray
    capture_timestamp: str
    arrival_timestamp: float
    frame_number: int
    sequence_number: int
    resolution: str
    metadata: Dict[str, Any]

class StreamingDecoder:
    """
    Decodes a stream of H.264 NAL units (Annex B) into DecodedFrame objects for the fusion pipeline.
    Maintains session synchronization and frame validation.
    """
    def __init__(self):
        self.codec = av.CodecContext.create("h264", "r")
        self.last_frame_number = -1
        self.last_capture_time = None
        self.sequence_counter = 0

    def decode_chunk(self, data: bytes, metadata: Optional[Dict[str, Any]] = None) -> List[DecodedFrame]:
        """
        Takes raw encoded chunk data (bytes) and metadata, validates, and yields decoded frames.
        """
        if metadata is None:
            logger.warning("Rejecting chunk: Missing metadata")
            return []

        frame_number = metadata.get("frameNumber", -1)
        if frame_number <= self.last_frame_number:
            logger.warning(f"Rejecting chunk: Duplicate or out-of-order packet (got {frame_number}, expected > {self.last_frame_number})")
            return []

        # Assuming captureTime is an ISO8601 string, we could do timestamp regression check
        capture_time = metadata.get("captureTime")
        if self.last_capture_time and capture_time and capture_time < self.last_capture_time:
            logger.warning(f"Rejecting chunk: Timestamp regression detected")
            return []

        self.last_frame_number = frame_number
        if capture_time:
            self.last_capture_time = capture_time
        
        arrival_timestamp = time.time()
        
        try:
            packets = self.codec.parse(data)
        except Exception as e:
            logger.warning(f"Rejecting chunk: Corrupted packet parse error - {e}")
            return []

        frames = []
        for packet in packets:
            try:
                for frame in self.codec.decode(packet):
                    img_array = frame.to_ndarray(format="bgr24")
                    
                    self.sequence_counter += 1
                    decoded_frame = DecodedFrame(
                        image=img_array,
                        capture_timestamp=capture_time or "",
                        arrival_timestamp=arrival_timestamp,
                        frame_number=frame_number,
                        sequence_number=self.sequence_counter,
                        resolution=metadata.get("resolution", f"{img_array.shape[1]}x{img_array.shape[0]}"),
                        metadata=metadata
                    )
                    frames.append(decoded_frame)
            except Exception as e:
                logger.warning(f"Rejecting chunk: Corrupted packet decode error - {e}")
                continue

        return frames

    def close(self):
        if self.codec:
            try:
                self.codec.close()
                self.codec = None
            except Exception:
                pass
