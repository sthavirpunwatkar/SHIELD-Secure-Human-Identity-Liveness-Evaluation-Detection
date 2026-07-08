import 'package:camera/camera.dart';

class CameraFrame {
  final CameraImage image;
  final DateTime timestamp;
  final int frameNumber;

  CameraFrame({
    required this.image,
    required this.timestamp,
    required this.frameNumber,
  });
}
