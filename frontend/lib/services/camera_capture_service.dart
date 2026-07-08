import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/widgets.dart';
import '../models/camera_frame.dart';
import '../models/camera_state.dart';

class CameraCaptureService extends ChangeNotifier with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  
  CameraController? get controller => _controller;

  final StreamController<CameraFrame> _frameController = StreamController<CameraFrame>.broadcast();
  Stream<CameraFrame> get frameStream => _frameController.stream;

  CameraState _state = CameraState.initial;
  CameraState get state => _state;

  bool get isStreaming => _state == CameraState.streaming;
  int _frameCount = 0;

  CameraCaptureService() {
    WidgetsBinding.instance.addObserver(this);
  }

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
    notifyListeners();
    return _state;
  } catch (e) {
      if (e is CameraException && e.code == 'CameraAccessDenied') {
        _state = CameraState.errorPermission;
      } else {
        _state = CameraState.errorUnknown;
      }
      notifyListeners();
      return _state;
    }
  }

  void startStreaming() {
    if (_controller == null || !_controller!.value.isInitialized) return;
    if (isStreaming) return;

    _state = CameraState.streaming;
    _frameCount = 0;
    notifyListeners();
    
    try {
      _controller!.startImageStream((CameraImage image) {
        if (!_frameController.isClosed) {
          _frameController.add(CameraFrame(image: image, timestamp: DateTime.now(), frameNumber: _frameCount++));
        }
      });
    } catch (e) {
      _state = CameraState.ready;
      notifyListeners();
    }
  }

  void stopStreaming() {
    if (!isStreaming) return;
    try {
      _controller?.stopImageStream();
    } catch (e) {
      // Ignored gracefully
    }
    _state = CameraState.ready;
    notifyListeners();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    stopStreaming();
    _frameController.close();
    _controller?.dispose();
    _controller = null;
    _state = CameraState.initial;
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused || state == AppLifecycleState.inactive) {
      stopStreaming();
      _controller?.dispose();
      _controller = null;
      _state = CameraState.initial;
      notifyListeners();
    } else if (state == AppLifecycleState.resumed) {
      initialize();
    }
  }
}
