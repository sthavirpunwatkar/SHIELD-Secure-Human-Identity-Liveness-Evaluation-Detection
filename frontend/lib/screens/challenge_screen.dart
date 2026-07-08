import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';
import '../services/challenge_service.dart';
import '../widgets/challenge_prompt.dart';
import '../services/camera_capture_service.dart';
import '../models/camera_frame.dart';
import '../models/camera_state.dart';
import 'package:shield_app/l10n/app_localizations.dart';

/// Screen that combines a live camera preview with the active
/// challenge-response verification flow managed by [ChallengeService].
class ChallengeScreen extends StatefulWidget {
  const ChallengeScreen({super.key});

  @override
  State<ChallengeScreen> createState() => _ChallengeScreenState();
}

class _ChallengeScreenState extends State<ChallengeScreen> {
  late CameraCaptureService _cameraService;
  StreamSubscription<CameraFrame>? _frameSub;
  bool _isStreaming = false;
  String? _errorMessage;
  int _tryCount = 0;

  StreamSubscription<ChallengeState>? _challengeSub;

  @override
  void initState() {
    super.initState();
    _cameraService = Provider.of<CameraCaptureService>(context, listen: false);
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
        setState(() => _errorMessage = null);
        _startChallenge();
      }
    } catch (e) {
      print('Camera initialization error: $e');
      if (mounted) {
        setState(() => _errorMessage = AppLocalizations.of(context)!.cameraInitError(e.toString()));
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Frame streaming
  // ---------------------------------------------------------------------------

  void _startStreaming() {
    if (_cameraService.controller == null || !_cameraService.controller!.value.isInitialized) return;

    final provider = Provider.of<LivenessProvider>(context, listen: false);
    if (!provider.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.notConnected)),
      );
      return;
    }

    setState(() => _isStreaming = true);
    _cameraService.startStreaming();
  }

  void _stopStreaming() {
    _cameraService.stopStreaming();
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
    if (_tryCount >= 3) return;
    setState(() => _tryCount++);
    final provider = Provider.of<LivenessProvider>(context, listen: false);
    provider.resetChallenge();
    _stopStreaming();
  }

  // ---------------------------------------------------------------------------
  // Lifecycle
  // ---------------------------------------------------------------------------

  @override
  void dispose() {
    _frameSub?.cancel();
    _challengeSub?.cancel();
    _cameraService.stopStreaming();
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
        appBar: AppBar(title: Text(AppLocalizations.of(context)!.challengeVerification)),
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

    // Loading state
    if (_cameraService.controller == null || !_cameraService.controller!.value.isInitialized) {
      return Scaffold(
        appBar: AppBar(title: Text(AppLocalizations.of(context)!.challengeVerification)),
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

    return Consumer<LivenessProvider>(
      builder: (context, provider, _) {
        final cs = provider.challengeService;
        final challengeState = cs.state;
        final isFinished = challengeState == ChallengeState.allPassed ||
            challengeState == ChallengeState.failed;

        return Scaffold(
          appBar: AppBar(
            title: Text(AppLocalizations.of(context)!.challengeVerification),
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
                    aspectRatio: _cameraService.controller!.value.aspectRatio,
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        CameraPreview(_cameraService.controller!),
                        
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
                          label: Text(AppLocalizations.of(context)!.startVerification),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12)),
                            backgroundColor: Colors.blueAccent,
                          ),
                        ),
                      ),
                    if (isFinished && _tryCount < 3)
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: _resetChallenge,
                          icon: const Icon(Icons.refresh),
                          label: Text(AppLocalizations.of(context)!.tryAgain),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12)),
                            backgroundColor: Colors.blueGrey,
                          ),
                        ),
                      ),
                    if (isFinished && _tryCount >= 3)
                      Expanded(
                        child: Text(
                          "Max tries reached",
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.redAccent, fontSize: 16, fontWeight: FontWeight.bold),
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
    final l10n = AppLocalizations.of(context)!;

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
            allPassed ? l10n.verificationPassed : l10n.verificationFailed,
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
                l10n.score((cs.challengeScore * 100).toStringAsFixed(1)),
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
                    cs.temporalValid! ? l10n.temporalOk : l10n.temporalFailed,
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
                      ChallengeService.getActionDisplayText(r.action, l10n),
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
