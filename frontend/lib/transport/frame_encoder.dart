import 'dart:typed_data';
import '../models/camera_frame.dart';

abstract class FrameEncoder {
  void initialize(Function(Uint8List, [CameraFrame? frame]) onChunkEncoded);
  Future<void> encodeFrame(CameraFrame frame);
}
