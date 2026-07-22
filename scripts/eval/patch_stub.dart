import 'dart:typed_data';
import '../models/camera_frame.dart';
import '../transport/frame_encoder.dart';

class WebCodecsService implements FrameEncoder {
  Function(Uint8List, [CameraFrame?])? onChunkEncoded;

  @override
  void initialize(Function(Uint8List, [CameraFrame?]) onChunk) {
    onChunkEncoded = onChunk;
  }

  @override
  Future<void> encodeFrame(CameraFrame frame) async {
    // We send a dummy byte array instead of 0 bytes, so it passes through the websocket!
    onChunkEncoded?.call(Uint8List.fromList([0, 1, 2, 3]), frame);
  }
}
