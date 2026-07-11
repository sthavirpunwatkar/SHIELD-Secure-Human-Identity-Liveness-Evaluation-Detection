import 'package:flutter/widgets.dart';
import '../models/camera_frame.dart';

class WebCaptureService {
  Future<void> initialize() async {
    throw UnsupportedError('WebCaptureService is only supported on the web.');
  }

  void startStreaming(Function(CameraFrame<dynamic>) onFrame) {
    throw UnsupportedError('WebCaptureService is only supported on the web.');
  }

  void stopStreaming() {}
  void dispose() {}
  
  Widget buildPreview() => const SizedBox();
}
