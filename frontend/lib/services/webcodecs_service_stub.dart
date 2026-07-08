import 'dart:typed_data';

class WebCodecsService {
  void initialize(Function(Uint8List) onChunk) {
    // No-op for non-web platforms
  }

  Future<void> encodeFrame(Uint8List jpegBytes) async {
    // No-op for non-web platforms
  }
}
