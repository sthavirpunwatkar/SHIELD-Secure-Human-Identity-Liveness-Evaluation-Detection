import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';
import '../services/challenge_service.dart';
import '../widgets/challenge_prompt.dart';

/// Screen that combines a live camera preview with the active
/// challenge-response verification flow managed by [ChallengeService].
class ChallengeScreen extends StatefulWidget {
  const ChallengeScreen({super.key});

  @override
  State<ChallengeScreen> createState() => _ChallengeScreenState();
}

class _ChallengeScreenState extends State<ChallengeScreen> {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isStreaming = false;
  Timer? _frameTimer;
  final int _throttleMs = 500;
  String? _errorMessage;

  StreamSubscription<ChallengeState>? _challengeSub;

  @override
  void initState() {
    super.initState();
    _initializeCamera();

    // Subscribe to challenge state changes so the UI rebuilds
    final provider = Provider.of<LivenessProvider>(context, listen: false);
    _challengeSub = provider.challengeStateStream.listen((_) {
      if (mounted) setState(() {});
    });
  }

  // ---------------------------------------------------------------------------
  // Camera setup (matches camera_screen.dart pattern)
  // ---------------------------------------------------------------------------

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        setState(() => _errorMessage = 'No cameras found on this device.');
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
      if (mounted) setState(() => _errorMessage = null);
    } catch (e) {
      print('Camera initialization error: $e');
      if (mounted) {
        setState(() => _errorMessage = 'Failed to initialize camera: $e');
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Frame streaming
  // ---------------------------------------------------------------------------

  void _startStreaming() {
    if (_controller == null || !_controller!.value.isInitialized) return;

    final provider = Provider.of<LivenessProvider>(context, listen: false);
    if (!provider.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Not connected to server')),
      );
      return;
    }

    setState(() => _isStreaming = true);

    _frameTimer?.cancel();
    _frameTimer = Timer.periodic(Duration(milliseconds: _throttleMs), (timer) async {
      if (!_isStreaming || !mounted) {
        timer.cancel();
        return;
      }
      try {
        final XFile file = await _controller!.takePicture();
        final bytes = await file.readAsBytes();
        provider.sendFrame(bytes);
      } catch (e) {
        print('Error in challenge streaming: $e');
      }
    });
  }

  void _stopStreaming() {
    _frameTimer?.cancel();
    setState(() => _isStreaming = false);
  }

  // ---------------------------------------------------------------------------
  // Challenge control
  // ---------------------------------------------------------------------------

  void _startChallenge() {
    final provider = Provider.of<LivenessProvider>(context, listen: false);
    provider.startChallengeSession();
    if (!_isStreaming) _startStreaming();
  }

  void _resetChallenge() {
    final provider = Provider.of<LivenessProvider>(context, listen: false);
    provider.resetChallenge();
    _stopStreaming();
  }

  // ---------------------------------------------------------------------------
  // Lifecycle
  // ---------------------------------------------------------------------------

  @override
  void dispose() {
    _frameTimer?.cancel();
    _challengeSub?.cancel();
    _controller?.dispose();
    super.dispose();
  }

  // ---------------------------------------------------------------------------
  // Build
  // ---------------------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    // Error state
    if (_errorMessage != null) {
      return Scaffold(
        appBar: AppBar(title: const Text('SHIELD Challenge Verification')),
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

    // Loading state
    if (_controller == null || !_controller!.value.isInitialized) {
      return Scaffold(
        appBar: AppBar(title: const Text('SHIELD Challenge Verification')),
        body: const Center(
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

    return Consumer<LivenessProvider>(
      builder: (context, provider, _) {
        final cs = provider.challengeService;
        final challengeState = cs.state;
        final isFinished = challengeState == ChallengeState.allPassed ||
            challengeState == ChallengeState.failed;

        return Scaffold(
          appBar: AppBar(
            title: const Text('SHIELD Challenge Verification'),
            actions: [
              if (_isStreaming)
                IconButton(
                  icon: const Icon(Icons.stop),
                  onPressed: _stopStreaming,
                ),
            ],
          ),
          body: Column(
            children: [
              // Camera preview with overlays
              Expanded(
                child: Center(
                  child: AspectRatio(
                    aspectRatio: _controller!.value.aspectRatio,
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        CameraPreview(_controller!),
                        // Face guide oval
                        CustomPaint(painter: _FaceGuideOvalPainter()),
                        // Challenge prompt overlay
                        Positioned(
                          bottom: 24,
                          left: 0,
                          right: 0,
                          child: ChallengePrompt(
                            currentAction: cs.currentAction,
                            remainingSeconds: cs.remainingSeconds,
                            totalSeconds: cs.timeoutSeconds,
                            currentIndex: cs.currentIndex,
                            totalChallenges: cs.totalChallenges,
                            state: challengeState,
                          ),
                        ),
                        // Connection badge
                        Positioned(
                          top: 10,
                          right: 10,
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: provider.isConnected
                                  ? Colors.green
                                  : Colors.red,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              provider.isConnected
                                  ? 'Connected'
                                  : 'Disconnected',
                              style: const TextStyle(
                                  color: Colors.white, fontSize: 12),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),

              // Result summary card (shown when challenges finish)
              if (isFinished) _buildResultSummary(cs),

              // Bottom controls
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    if (!isFinished)
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: challengeState == ChallengeState.idle ||
                                  challengeState == ChallengeState.error
                              ? _startChallenge
                              : null,
                          icon: const Icon(Icons.play_arrow),
                          label: const Text('Start Verification'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12)),
                            backgroundColor: Colors.blueAccent,
                          ),
                        ),
                      ),
                    if (isFinished)
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: _resetChallenge,
                          icon: const Icon(Icons.refresh),
                          label: const Text('Try Again'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12)),
                            backgroundColor: Colors.blueGrey,
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  // ---------------------------------------------------------------------------
  // Result summary card
  // ---------------------------------------------------------------------------

  Widget _buildResultSummary(ChallengeService cs) {
    final allPassed = cs.state == ChallengeState.allPassed;
    final color = allPassed ? Colors.greenAccent : Colors.redAccent;

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black87,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            allPassed ? 'Verification Passed' : 'Verification Failed',
            style: TextStyle(
              color: color,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Score: ${(cs.challengeScore * 100).toStringAsFixed(1)}%',
            style: const TextStyle(color: Colors.white, fontSize: 16),
          ),
          const Divider(color: Colors.white24, height: 24),
          // Individual challenge results
          ...cs.results.map((r) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 3),
              child: Row(
                children: [
                  Icon(
                    r.passed ? Icons.check_circle : Icons.cancel,
                    color: r.passed ? Colors.greenAccent : Colors.redAccent,
                    size: 20,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      ChallengeService.getActionDisplayText(r.action),
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                    ),
                  ),
                  Text(
                    '${r.responseTimeMs.toStringAsFixed(0)} ms',
                    style: const TextStyle(color: Colors.white70, fontSize: 13),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}

// =============================================================================
// Face guide oval painter
// =============================================================================

class _FaceGuideOvalPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.white.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    final center = Offset(size.width / 2, size.height * 0.38);
    final ovalRect = Rect.fromCenter(
      center: center,
      width: size.width * 0.55,
      height: size.height * 0.45,
    );

    canvas.drawOval(ovalRect, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
