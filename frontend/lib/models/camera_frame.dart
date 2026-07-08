import 'package:camera/camera.dart';

class CameraFrame {
  final CameraImage image;
  final DateTime timestamp;

  CameraFrame({
    required this.image,
    required this.timestamp,
  });
}
