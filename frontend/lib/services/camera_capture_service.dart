import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter/foundation.dart';
import '../models/camera_frame.dart';
import '../models/camera_state.dart';
import 'web_capture_stub.dart' if (dart.library.js_interop) 'web_capture_web.dart';

class CameraCaptureService extends ChangeNotifier with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  
  WebCaptureService? _webCaptureService;

  CameraController? get controller => _controller;

  Widget buildPreview() {
    if (kIsWeb) {
      if (_webCaptureService == null) return const SizedBox();
      return _webCaptureService!.buildPreview();
    }
    if (_controller == null) return const SizedBox();
    return CameraPreview(_controller!);
  }

  double get aspectRatio {
    if (kIsWeb) {
      return 4.0 / 3.0; // Default web aspect ratio
    }
    return _controller?.value.aspectRatio ?? (4.0 / 3.0);
  }

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
    if (kIsWeb) {
      if (_webCaptureService != null) {
        _state = CameraState.ready;
        return _state;
      }
      _state = CameraState.initializing;
      try {
        _webCaptureService = WebCaptureService();
        await _webCaptureService!.initialize();
        _state = CameraState.ready;
        notifyListeners();
        return _state;
      } catch (e) {
        _state = CameraState.errorUnknown;
        notifyListeners();
        return _state;
      }
    }

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
    if (kIsWeb) {
      if (_webCaptureService == null) return;
      if (isStreaming) return;

      _state = CameraState.streaming;
      _frameCount = 0;
      notifyListeners();

      try {
        _webCaptureService!.startStreaming((frame) {
          if (!_frameController.isClosed) {
            _frameController.add(frame);
          }
        });
      } catch (e) {
        _state = CameraState.errorUnknown;
        notifyListeners();
        throw Exception('Failed to start web camera stream: $e');
      }
      return;
    }

    if (_controller == null || !_controller!.value.isInitialized) return;
    if (isStreaming) return;

    _state = CameraState.streaming;
    _frameCount = 0;
    notifyListeners();

    try {
      _controller!.startImageStream((CameraImage image) {
        if (_frameController.isClosed) return;
        
        final frame = CameraFrame<CameraImage>(
          payload: image,
          timestamp: DateTime.now(),
          frameNumber: _frameCount++,
          width: image.width,
          height: image.height,
          imageFormat: image.format.group == ImageFormatGroup.yuv420
              ? FrameFormat.yuv420
              : image.format.group == ImageFormatGroup.bgra8888
                  ? FrameFormat.bgra8888
                  : FrameFormat.unknown,
        );
        _frameController.add(frame);
      });
    } catch (e) {
      _state = CameraState.errorUnknown;
      notifyListeners();
      throw Exception('Failed to start camera stream: $e');
    }
  }

  void stopStreaming() {
    if (!isStreaming) return;
    
    if (kIsWeb) {
      try {
        _webCaptureService?.stopStreaming();
      } catch (e) {
        // Ignored
      }
    } else {
      try {
        _controller?.stopImageStream();
      } catch (e) {
        // Ignored gracefully
      }
    }
    
    _state = CameraState.ready;
    notifyListeners();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    stopStreaming();
    _frameController.close();
    
    if (kIsWeb) {
      _webCaptureService?.dispose();
      _webCaptureService = null;
    } else {
      _controller?.dispose();
      _controller = null;
    }
    
    _state = CameraState.initial;
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused || state == AppLifecycleState.inactive) {
      stopStreaming();
      
      if (kIsWeb) {
        _webCaptureService?.dispose();
        _webCaptureService = null;
      } else {
        _controller?.dispose();
        _controller = null;
      }
      
      _state = CameraState.initial;
      notifyListeners();
    } else if (state == AppLifecycleState.resumed) {
      initialize().then((_) {
        // If we were streaming before, we could auto-resume here if needed.
      });
    }
  }
}
