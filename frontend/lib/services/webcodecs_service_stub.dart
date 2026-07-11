import 'dart:typed_data';

import '../models/camera_frame.dart';
import '../transport/frame_encoder.dart';

/// DEVELOPMENT STUB:
/// This desktop stub only exists to keep the transport pipeline alive for architectural testing.
/// It does NOT produce H.264. It is not a production encoder and should not be represented as one.
class WebCodecsService implements FrameEncoder {
  Function(Uint8List, [CameraFrame?])? onChunkEncoded;

  @override
  void initialize(Function(Uint8List, [CameraFrame?]) onChunk) {
    onChunkEncoded = onChunk;
  }

  @override
  Future<void> encodeFrame(CameraFrame frame) async {
    onChunkEncoded?.call(Uint8List(0), frame);
  }
}
