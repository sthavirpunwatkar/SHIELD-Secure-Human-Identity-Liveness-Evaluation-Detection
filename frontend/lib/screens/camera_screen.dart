import 'dart:async';
import 'dart:io' show Platform;
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';
import '../widgets/liveness_overlay.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isStreaming = false;
  bool _isCapturing = false;
  DateTime? _lastFrameTime;
  final int _throttleMs = 500; // Slower for desktop fallback
  Timer? _timer;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        setState(() {
          _errorMessage = 'No cameras found on this device.';
        });
        return;
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
      if (mounted) {
        setState(() {
          _errorMessage = null;
        });
        _startStreaming();
      }
    } catch (e) {
      print('Camera initialization error: $e');
      if (mounted) {
        setState(() {
          _errorMessage = 'Failed to initialize camera: $e';
        });
      }
    }
  }

  void _toggleStreaming() {
    if (_isStreaming) {
      _stopStreaming();
    } else {
      _startStreaming();
    }
  }

  void _stopStreaming() {
    try {
      // Check if streaming is actually active before stopping
      // This is safely handled by the camera package usually, but let's be careful
    } catch (e) {
      print('Error stopping stream: $e');
    }
    
    _timer?.cancel();
    setState(() {
      _isStreaming = false;
    });
  }

  void _startStreaming() {
    if (_controller == null || !_controller!.value.isInitialized) return;

    final provider = Provider.of<LivenessProvider>(context, listen: false);
    if (!provider.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Not connected to server')),
      );
      return;
    }

    setState(() {
      _isStreaming = true;
    });

    // Use the robust timer fallback to capture and encode frames as JPEGs cross-platform
    _useTimerFallback(provider);
  }

  void _useTimerFallback(LivenessProvider provider) {
    _timer?.cancel();
    _isCapturing = false;
    _timer = Timer.periodic(Duration(milliseconds: _throttleMs), (timer) async {
      if (!_isStreaming || !mounted) {
        timer.cancel();
        return;
      }
      if (_isCapturing) return; // Skip frame if previous capture is still in progress
      _isCapturing = true;
      try {
        final XFile file = await _controller!.takePicture();
        final bytes = await file.readAsBytes();
        provider.sendFrame(bytes);
      } catch (e) {
        print('Error in fallback streaming: $e');
      } finally {
        _isCapturing = false;
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_errorMessage != null) {
      return Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, color: Colors.red, size: 60),
                const SizedBox(height: 16),
                Text(_errorMessage!, textAlign: TextAlign.center),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _initializeCamera,
                  child: const Text('Retry'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 16),
              Text('Initializing Camera...'),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('SHIELD Liveness'),
        actions: [
          IconButton(
            icon: Icon(_isStreaming ? Icons.stop : Icons.play_arrow),
            onPressed: _toggleStreaming,
          ),
        ],
      ),
      body: Center(
        child: AspectRatio(
          aspectRatio: _controller!.value.aspectRatio,
          child: Stack(
            fit: StackFit.expand,
            children: [
              CameraPreview(_controller!),
              const LivenessOverlay(),
            ],
          ),
        ),
      ),
    );
  }
}
