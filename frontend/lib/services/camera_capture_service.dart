import 'dart:async';
import 'package:camera/camera.dart';
import '../models/camera_frame.dart';
import '../models/camera_state.dart';

class CameraCaptureService {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  
  CameraController? get controller => _controller;

  final StreamController<CameraFrame> _frameController = StreamController<CameraFrame>.broadcast();
  Stream<CameraFrame> get frameStream => _frameController.stream;

  CameraState _state = CameraState.initial;
  CameraState get state => _state;

  bool get isStreaming => _state == CameraState.streaming;

  Future<CameraState> initialize() async {
    if (_controller != null && _controller!.value.isInitialized) {
      _state = CameraState.ready;
      return _state;
    }

    _state = CameraState.initializing;
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        _state = CameraState.errorNoCamera;
        return _state;
      }

    CameraDescription? selectedCamera;
    for (var camera in _cameras!) {
      if (camera.lensDirection == CameraLensDirection.front) {
        selectedCamera = camera;
        break;
      }
    }
    selectedCamera ??= _cameras![0];

    _controller = CameraController(
      selectedCamera,
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await _controller!.initialize();
    _state = CameraState.ready;
    return _state;
  } catch (e) {
      if (e is CameraException && e.code == 'CameraAccessDenied') {
        _state = CameraState.errorPermission;
      } else {
        _state = CameraState.errorUnknown;
      }
      return _state;
    }
  }

  void startStreaming() {
    if (_controller == null || !_controller!.value.isInitialized) return;
    if (isStreaming) return;

    _state = CameraState.streaming;
    _controller!.startImageStream((CameraImage image) {
      if (!_frameController.isClosed) {
        _frameController.add(CameraFrame(image: image, timestamp: DateTime.now()));
      }
    }).catchError((e) {
      print('Error starting image stream: $e');
      _state = CameraState.ready;
    });
  }

  void stopStreaming() {
    if (!isStreaming) return;
    try {
      _controller?.stopImageStream();
    } catch (e) {
      print('Error stopping stream: $e');
    }
    _state = CameraState.ready;
  }

  void dispose() {
    stopStreaming();
    _frameController.close();
    _controller?.dispose();
    _controller = null;
    _state = CameraState.initial;
  }
}
