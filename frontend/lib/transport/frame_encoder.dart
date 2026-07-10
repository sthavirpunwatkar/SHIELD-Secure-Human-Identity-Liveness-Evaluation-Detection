import 'dart:typed_data';

abstract class FrameEncoder {
  void initialize(Function(Uint8List) onChunkEncoded);
  Future<void> encodeFrame(Uint8List frameData);
}
