import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../services/challenge_service.dart';
import 'package:shield_app/l10n/app_localizations.dart';

/// Animated overlay that displays the current challenge instruction,
/// countdown timer, and progress dots during the challenge-response flow.
class ChallengePrompt extends StatefulWidget {
  final String currentAction;
  final int remainingSeconds;
  final int totalSeconds;
  final int currentIndex;
  final int totalChallenges;
  final ChallengeState state;

  const ChallengePrompt({
    super.key,
    required this.currentAction,
    required this.remainingSeconds,
    this.totalSeconds = 5,
    required this.currentIndex,
    required this.totalChallenges,
    required this.state,
  });

  @override
  State<ChallengePrompt> createState() => _ChallengePromptState();
}

class _ChallengePromptState extends State<ChallengePrompt>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  late AnimationController _resultController;
  late Animation<double> _resultScaleAnimation;

  @override
  void initState() {
    super.initState();

    // Pulse animation for the action icon
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 0.9, end: 1.15).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    // Scale-up animation for the success / failure icon
    _resultController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );

    _resultScaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _resultController, curve: Curves.elasticOut),
    );
  }

  @override
  void didUpdateWidget(ChallengePrompt oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (widget.state == ChallengeState.allPassed ||
        widget.state == ChallengeState.failed) {
      _pulseController.stop();
      _resultController.forward(from: 0);

      // Provide haptic feedback on result
      if (widget.state == ChallengeState.allPassed) {
        HapticFeedback.heavyImpact();
      } else {
        HapticFeedback.vibrate();
      }
    } else if (widget.state == ChallengeState.challengeActive) {
      if (!_pulseController.isAnimating) {
        _pulseController.repeat(reverse: true);
      }
      _resultController.reset();
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _resultController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 400),
      switchInCurve: Curves.easeOut,
      switchOutCurve: Curves.easeIn,
      child: _buildContent(),
    );
  }

  Widget _buildContent() {
    final l10n = AppLocalizations.of(context)!;
    switch (widget.state) {
      case ChallengeState.idle:
      case ChallengeState.connecting:
        return _buildIdleCard(l10n);
      case ChallengeState.challengeActive:
        return _buildActiveCard(l10n);
      case ChallengeState.waiting:
        return _buildWaitingCard(l10n);
      case ChallengeState.allPassed:
        return _buildResultIcon(
          icon: Icons.check_circle,
          color: Colors.greenAccent,
          label: l10n.allChallengesPassed,
        );
      case ChallengeState.failed:
        return _buildResultIcon(
          icon: Icons.cancel,
          color: Colors.redAccent,
          label: l10n.challengeFailed,
        );
      case ChallengeState.error:
        return _buildResultIcon(
          icon: Icons.error_outline,
          color: Colors.orangeAccent,
          label: l10n.anErrorOccurred,
        );
    }
  }

  // ---------------------------------------------------------------------------
  // Card builders
  // ---------------------------------------------------------------------------

  Widget _buildIdleCard(AppLocalizations l10n) {
    return _glassCard(
      key: ValueKey('idle_${widget.state.name}'),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.face_retouching_natural, size: 48, color: Colors.white70),
          const SizedBox(height: 12),
          Text(
            widget.state == ChallengeState.connecting
                ? l10n.connecting
                : l10n.readyToStart,
            style: const TextStyle(color: Colors.white, fontSize: 18),
          ),
        ],
      ),
    );
  }

  Widget _buildActiveCard(AppLocalizations l10n) {
    final icon = ChallengeService.getActionIcon(widget.currentAction);
    final text = ChallengeService.getActionDisplayText(widget.currentAction, l10n);

    return _glassCard(
      key: ValueKey('active_${widget.currentIndex}_${widget.currentAction}'),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Animated action icon
          ScaleTransition(
            scale: _pulseAnimation,
            child: Icon(icon, size: 64, color: Colors.blueAccent),
          ),
          const SizedBox(height: 16),
          // Instruction text
          Text(
            text,
            textAlign: TextAlign.center,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 20),
          // Countdown ring
          SizedBox(
            width: 72,
            height: 72,
            child: CustomPaint(
              painter: _CountdownRingPainter(
                progress: widget.totalSeconds > 0
                    ? widget.remainingSeconds / widget.totalSeconds
                    : 0,
                color: widget.remainingSeconds <= 2
                    ? Colors.redAccent
                    : Colors.blueAccent,
              ),
              child: Center(
                child: Text(
                  '${widget.remainingSeconds}',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Progress dots
          _buildProgressDots(),
        ],
      ),
    );
  }

  Widget _buildWaitingCard(AppLocalizations l10n) {
    return _glassCard(
      key: ValueKey('waiting_${widget.currentIndex}'),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(
            width: 32,
            height: 32,
            child: CircularProgressIndicator(strokeWidth: 3, color: Colors.blueAccent),
          ),
          const SizedBox(height: 12),
          Text(
            l10n.processing,
            style: const TextStyle(color: Colors.white70, fontSize: 16),
          ),
          const SizedBox(height: 12),
          _buildProgressDots(),
        ],
      ),
    );
  }

  Widget _buildResultIcon({
    required IconData icon,
    required Color color,
    required String label,
  }) {
    return _glassCard(
      key: ValueKey(label),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ScaleTransition(
            scale: _resultScaleAnimation,
            child: Icon(icon, size: 72, color: color),
          ),
          const SizedBox(height: 12),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  // ---------------------------------------------------------------------------
  // Progress dots
  // ---------------------------------------------------------------------------

  Widget _buildProgressDots() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(widget.totalChallenges, (i) {
        Color dotColor;
        Widget dot;
        if (i < widget.currentIndex) {
          dotColor = Colors.greenAccent; // Completed
          dot = const Icon(Icons.check_circle, color: Colors.greenAccent, size: 16);
        } else {
          if (i == widget.currentIndex) {
            dotColor = Colors.blueAccent; // Active
          } else {
            dotColor = Colors.white24; // Upcoming
          }
          dot = AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            width: i == widget.currentIndex ? 14 : 10,
            height: i == widget.currentIndex ? 14 : 10,
            decoration: BoxDecoration(
              color: dotColor,
              shape: BoxShape.circle,
              boxShadow: i == widget.currentIndex
                  ? [BoxShadow(color: dotColor.withValues(alpha: 0.6), blurRadius: 8)]
                  : null,
            ),
          );
        }

        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4),
          child: dot,
        );
      }),
    );
  }

  // ---------------------------------------------------------------------------
  // Glassmorphism container
  // ---------------------------------------------------------------------------

  Widget _glassCard({required Key key, required Widget child}) {
    return Container(
      key: key,
      margin: const EdgeInsets.symmetric(horizontal: 24),
      padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 24),
      decoration: BoxDecoration(
        color: Colors.black.withValues(alpha: 0.55),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white12),
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Colors.white.withValues(alpha: 0.08),
            Colors.white.withValues(alpha: 0.02),
          ],
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.4),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: child,
    );
  }
}

// =============================================================================
// Custom painter for the countdown ring
// =============================================================================

class _CountdownRingPainter extends CustomPainter {
  final double progress; // 0.0 → 1.0
  final Color color;

  _CountdownRingPainter({required this.progress, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2 - 4;

    // Background ring
    final bgPaint = Paint()
      ..color = Colors.white12
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5;
    canvas.drawCircle(center, radius, bgPaint);

    // Progress arc
    final progressPaint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -pi / 2, // start at 12-o'clock
      2 * pi * progress,
      false,
      progressPaint,
    );
  }

  @override
  bool shouldRepaint(_CountdownRingPainter oldDelegate) =>
      oldDelegate.progress != progress || oldDelegate.color != color;
}
