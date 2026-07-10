import 'dart:typed_data';

import '../transport/frame_encoder.dart';

class WebCodecsService implements FrameEncoder {
  @override
  void initialize(Function(Uint8List) onChunk) {
    // No-op for non-web platforms
  }

  @override
  Future<void> encodeFrame(Uint8List jpegBytes) async {
    // No-op for non-web platforms
  }
}
