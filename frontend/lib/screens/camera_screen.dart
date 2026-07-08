import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';
import '../widgets/liveness_overlay.dart';
import '../services/security_service.dart';
import '../services/camera_capture_service.dart';
import '../models/camera_frame.dart';
import '../models/camera_state.dart';
import 'package:shield_app/l10n/app_localizations.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraCaptureService _cameraService;
  StreamSubscription<CameraFrame>? _frameSub;
  bool _isStreaming = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _cameraService = Provider.of<CameraCaptureService>(context, listen: false);
    _cameraService.addListener(_onServiceUpdated);
    _initializeCamera();
  }

  void _onServiceUpdated() {
    if (mounted) setState(() {});
  }

  Future<void> _initializeCamera() async {
    try {
      final isVirtual = await SecurityService.hasVirtualCamera();
      if (isVirtual) {
        if (mounted) {
          setState(() {
            _errorMessage = AppLocalizations.of(context)!.virtualCameraAlert;
          });
        }
        return;
      }

      final state = await _cameraService.initialize();
      
      if (state == CameraState.errorNoCamera) {
        if (mounted) setState(() => _errorMessage = AppLocalizations.of(context)!.noCameras);
        return;
      } else if (state == CameraState.errorPermission) {
        if (mounted) setState(() => _errorMessage = "Camera permission denied.");
        return;
      } else if (state != CameraState.ready) {
        if (mounted) setState(() => _errorMessage = "Camera initialization failed.");
        return;
      }

      _frameSub = _cameraService.frameStream.listen((CameraFrame frame) {
        // Continuous capture only, no backend streaming yet.
      });

      if (mounted) {
        setState(() {
          _errorMessage = null;
        });
        _startStreaming();
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = AppLocalizations.of(context)!.cameraInitError(e.toString());
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
    _cameraService.stopStreaming();
    setState(() {
      _isStreaming = false;
    });
  }

  void _startStreaming() {
    if (_cameraService.controller == null || !_cameraService.controller!.value.isInitialized) return;

    final provider = Provider.of<LivenessProvider>(context, listen: false);
    if (!provider.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.notConnected)),
      );
      return;
    }

    setState(() {
      _isStreaming = true;
    });

    _cameraService.startStreaming();
  }

  @override
  void dispose() {
    _cameraService.removeListener(_onServiceUpdated);
    _frameSub?.cancel();
    _cameraService.stopStreaming();
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
                  child: Text(AppLocalizations.of(context)!.retry),
                ),
              ],
            ),
          ),
        ),
      );
    }

    if (_cameraService.controller == null || !_cameraService.controller!.value.isInitialized) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const CircularProgressIndicator(),
              const SizedBox(height: 16),
              Text(AppLocalizations.of(context)!.initCamera),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.passiveCheck),
        actions: [
          IconButton(
            icon: Icon(_isStreaming ? Icons.stop : Icons.play_arrow),
            onPressed: _toggleStreaming,
          ),
        ],
      ),
      body: Center(
        child: AspectRatio(
          aspectRatio: _cameraService.controller!.value.aspectRatio,
          child: Stack(
            fit: StackFit.expand,
            children: [
              CameraPreview(_cameraService.controller!),
              const LivenessOverlay(),
            ],
          ),
        ),
      ),
    );
  }
}
