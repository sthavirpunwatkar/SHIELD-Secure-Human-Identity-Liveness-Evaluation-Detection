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
  bool _isCapturing = false;
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
    _challengeSub = provider.challengeService.stateStream.listen((_) {
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

      await Future.delayed(const Duration(milliseconds: 2000)); // Release hardware lock from previous screen
      await _controller!.initialize();
      if (mounted) {
        setState(() => _errorMessage = null);
        _startChallenge();
      }
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
    _isCapturing = false;
    _frameTimer = Timer.periodic(Duration(milliseconds: _throttleMs), (timer) async {
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
        print('Error in challenge streaming: $e');
      } finally {
        _isCapturing = false;
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
                        
                        // Face guide oval with dynamic feedback
                        _buildDynamicFaceGuide(provider, cs, challengeState),

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
  // Dynamic Face Guide and Spotlight
  // ---------------------------------------------------------------------------

  Widget _buildDynamicFaceGuide(
    LivenessProvider provider,
    ChallengeService cs,
    ChallengeState challengeState,
  ) {
    final qm = provider.currentResult.qualityMetrics;
    Color guideColor = Colors.white30;
    String? warning;

    if (provider.currentResult.verdict == 'No Face Detected') {
      warning = 'Position your face in the oval';
      guideColor = Colors.orangeAccent;
    } else if (qm.isBlurry) {
      warning = 'Hold still - image is blurry';
      guideColor = Colors.redAccent;
    } else if (qm.illuminationStatus == 'underexposed') {
      warning = 'Too dark - find better lighting';
      guideColor = Colors.redAccent;
    } else if (qm.illuminationStatus == 'overexposed') {
      warning = 'Too bright - avoid direct light';
      guideColor = Colors.redAccent;
    } else if (qm.poseStatus != 'frontal' && qm.poseStatus != 'unknown') {
      warning = 'Look straight at the camera';
      guideColor = Colors.orangeAccent;
    } else if (provider.currentResult.status == 'success') {
      guideColor = Colors.greenAccent;
    }

    return Stack(
      fit: StackFit.expand,
      children: [
        CustomPaint(
          painter: _FaceGuideOvalPainter(
            color: guideColor,
            warning: warning,
            bbox: provider.currentResult.bbox,
            frameSize: provider.currentResult.frameSize,
          ),
        ),
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
      ],
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
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Score: ${(cs.challengeScore * 100).toStringAsFixed(1)}%',
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
              if (cs.temporalValid != null) ...[
                const SizedBox(width: 16),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: cs.temporalValid! ? Colors.green.withOpacity(0.2) : Colors.red.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(4),
                    border: Border.all(color: cs.temporalValid! ? Colors.green : Colors.red, width: 0.5),
                  ),
                  child: Text(
                    cs.temporalValid! ? 'Temporal OK' : 'Temporal Failed',
                    style: TextStyle(
                      color: cs.temporalValid! ? Colors.greenAccent : Colors.redAccent,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ],
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
// Face guide oval painter with dynamic colors and spotlight effect
// =============================================================================

class _FaceGuideOvalPainter extends CustomPainter {
  final Color color;
  final String? warning;
  final List<double>? bbox;
  final List<int>? frameSize;

  _FaceGuideOvalPainter({this.color = Colors.white30, this.warning, this.bbox, this.frameSize});

  @override
  void paint(Canvas canvas, Size size) {
    Rect ovalRect;

    if (bbox != null && bbox!.length == 4 && frameSize != null && frameSize!.length == 2) {
      // Dynamic tracking using backend bounding box
      final scaleX = size.width / frameSize![0];
      final scaleY = size.height / frameSize![1];
      
      final left = bbox![0] * scaleX;
      final top = bbox![1] * scaleY;
      final width = (bbox![2] - bbox![0]) * scaleX;
      final height = (bbox![3] - bbox![1]) * scaleY;
      
      ovalRect = Rect.fromLTWH(left, top, width, height);
      // Inflate slightly so the oval nicely surrounds the face instead of clipping it
      ovalRect = ovalRect.inflate(30);
    } else {
      // Static fallback: vertical portrait oval
      final center = Offset(size.width / 2, size.height * 0.45);
      final height = size.height * 0.6;
      final width = height * 0.7; // Vertical aspect ratio
      
      ovalRect = Rect.fromCenter(
        center: center,
        width: width,
        height: height,
      );
    }

    final center = ovalRect.center;
    final height = ovalRect.height;

    // 1. Draw Spotlight (Darkened background except for the face area)
    final backgroundPath = Path()..addRect(Rect.fromLTWH(0, 0, size.width, size.height));
    final ovalPath = Path()..addOval(ovalRect);
    final spotlightPath = Path.combine(PathOperation.difference, backgroundPath, ovalPath);

    final spotlightPaint = Paint()
      ..color = Colors.black.withOpacity(0.65)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
    canvas.drawPath(spotlightPath, spotlightPaint);

    // 2. Draw the Oval Guide
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;

    // Outer glow for the oval
    final glowPaint = Paint()
      ..color = color.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
    canvas.drawOval(ovalRect, glowPaint);
    canvas.drawOval(ovalRect, paint);

    // 3. Draw Warning Text if any
    if (warning != null) {
      final textPainter = TextPainter(
        text: TextSpan(
          text: warning,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 16,
            fontWeight: FontWeight.bold,
            backgroundColor: Colors.black45,
          ),
        ),
        textDirection: TextDirection.ltr,
        textAlign: TextAlign.center,
      );
      textPainter.layout(minWidth: 0, maxWidth: size.width * 0.8);
      textPainter.paint(
        canvas,
        Offset(size.width / 2 - textPainter.width / 2, center.dy + height / 2 + 20),
      );
    }
  }

  @override
  bool shouldRepaint(covariant _FaceGuideOvalPainter oldDelegate) =>
      oldDelegate.color != color || 
      oldDelegate.warning != warning ||
      oldDelegate.bbox != bbox || 
      oldDelegate.frameSize != frameSize;
}
