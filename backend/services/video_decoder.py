import av
import numpy as np

class WebCodecsDecoder:
    """
    Decodes a stream of H.264 NAL units (Annex B) into BGR numpy arrays for the fusion pipeline.
    """
    def __init__(self):
        # Create a codec context for decoding H.264
        self.codec = av.CodecContext.create("h264", "r")
        
    def decode_chunk(self, data: bytes):
        """
        Takes raw encoded chunk data (bytes) and yields decoded frames (BGR numpy arrays).
        """
        packets = self.codec.parse(data)
        frames = []
        for packet in packets:
            for frame in self.codec.decode(packet):
                img_array = frame.to_ndarray(format="bgr24")
                frames.append(img_array)
        return frames

    def close(self):
        if self.codec:
            try:
                self.codec.close()
                self.codec = None
            except Exception:
                pass
