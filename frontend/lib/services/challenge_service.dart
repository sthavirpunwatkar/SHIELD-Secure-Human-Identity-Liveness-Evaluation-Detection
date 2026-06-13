import 'dart:async';
import 'package:flutter/material.dart';
import '../models/liveness_result.dart';

/// Possible states for the active challenge-response flow.
enum ChallengeState {
  idle,
  connecting,
  challengeActive,
  waiting,
  allPassed,
  failed,
  error,
}

/// Manages challenge lifecycle: receives server messages, runs countdown
/// timers, and emits [ChallengeState] updates via a broadcast stream.
class ChallengeService {
  ChallengeState _state = ChallengeState.idle;
  String _currentAction = '';
  int _timeoutSeconds = 5;
  int _currentIndex = 0;
  int _totalChallenges = 3;
  int _passedCount = 0;
  double _challengeScore = 0.0;
  bool? _temporalValid;
  Timer? _countdownTimer;
  int _remainingSeconds = 5;
  final List<ChallengeResult> _results = [];

  // ---------------------------------------------------------------------------
  // Getters
  // ---------------------------------------------------------------------------
  ChallengeState get state => _state;
  String get currentAction => _currentAction;
  int get timeoutSeconds => _timeoutSeconds;
  int get currentIndex => _currentIndex;
  int get totalChallenges => _totalChallenges;
  int get passedCount => _passedCount;
  double get challengeScore => _challengeScore;
  bool? get temporalValid => _temporalValid;
  int get remainingSeconds => _remainingSeconds;
  List<ChallengeResult> get results => List.unmodifiable(_results);

  // ---------------------------------------------------------------------------
  // Stream
  // ---------------------------------------------------------------------------
  final StreamController<ChallengeState> _stateController =
      StreamController<ChallengeState>.broadcast();

  Stream<ChallengeState> get stateStream => _stateController.stream;

  // ---------------------------------------------------------------------------
  // Server message handling
  // ---------------------------------------------------------------------------

  /// Routes an incoming JSON message from the backend to the correct handler
  /// based on its `type` field (`challenge`, `challenge_result`, `verdict`).
  void handleServerMessage(Map<String, dynamic> json) {
    final String type = json['type'] ?? '';

    switch (type) {
      case 'challenge':
        _handleChallenge(json);
        break;
      case 'challenge_result':
        _handleChallengeResult(json);
        break;
      case 'verdict':
        _handleVerdict(json);
        break;
      default:
        // Ignore unrecognized message types
        break;
    }
  }

  void _handleChallenge(Map<String, dynamic> json) {
    _currentAction = json['current_challenge'] ?? json['action'] ?? '';
    _timeoutSeconds = json['challenge_timeout_s'] ?? json['timeout_s'] ?? 5;
    _currentIndex = json['challenge_index'] ?? json['index'] ?? _currentIndex;
    _totalChallenges = json['challenge_total'] ?? json['total'] ?? _totalChallenges;
    _remainingSeconds = _timeoutSeconds;

    _setState(ChallengeState.challengeActive);
    _startCountdown(_timeoutSeconds);
  }

  void _handleChallengeResult(Map<String, dynamic> json) {
    _countdownTimer?.cancel();

    final result = ChallengeResult(
      action: json['action'] ?? _currentAction,
      passed: json['passed'] ?? false,
      responseTimeMs: (json['response_time_ms'] ?? 0.0).toDouble(),
    );
    _results.add(result);

    if (result.passed) {
      _passedCount++;
    }

    // Brief waiting state before the next challenge / verdict arrives
    _setState(ChallengeState.waiting);
  }

  void _handleVerdict(Map<String, dynamic> json) {
    _countdownTimer?.cancel();
    _challengeScore =
        json['challenge_score'] != null ? (json['challenge_score']).toDouble() : 0.0;
    _temporalValid = json['temporal_valid'];

    // Parse aggregated results if the server sends them
    if (json['challenge_results'] != null) {
      _results.clear();
      for (final r in json['challenge_results']) {
        _results.add(ChallengeResult.fromJson(r as Map<String, dynamic>));
      }
      _passedCount = _results.where((r) => r.passed).length;
    }

    final String verdict = json['verdict'] ?? '';
    // Server verdict is final. Fallback to passedCount if verdict is unknown.
    bool passed = false;
    if (verdict == 'Live') {
      passed = true;
    } else if (verdict == 'Spoof') {
      passed = false;
    } else {
      passed = _passedCount >= (_totalChallenges / 2); // Simple majority fallback
    }

    // If temporal validation failed, it's a spoof regardless of challenge scores
    if (_temporalValid == false) {
      passed = false;
    }

    if (passed) {
      _setState(ChallengeState.allPassed);
    } else {
      _setState(ChallengeState.failed);
    }
  }

  // ---------------------------------------------------------------------------
  // Countdown timer
  // ---------------------------------------------------------------------------

  void _startCountdown(int seconds) {
    _countdownTimer?.cancel();
    _remainingSeconds = seconds;

    _countdownTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      _remainingSeconds--;
      if (_remainingSeconds <= 0) {
        timer.cancel();
      }
      // Re-emit current state so listeners can update the countdown display
      _stateController.add(_state);
    });
  }

  // ---------------------------------------------------------------------------
  // Lifecycle helpers
  // ---------------------------------------------------------------------------

  /// Marks the service as [ChallengeState.connecting] while the WebSocket
  /// handshake is in progress.
  void setConnecting() {
    _setState(ChallengeState.connecting);
  }

  /// Resets all state back to [ChallengeState.idle].
  void reset() {
    _countdownTimer?.cancel();
    _state = ChallengeState.idle;
    _currentAction = '';
    _timeoutSeconds = 5;
    _currentIndex = 0;
    _totalChallenges = 3;
    _passedCount = 0;
    _challengeScore = 0.0;
    _remainingSeconds = 5;
    _results.clear();
    _stateController.add(_state);
  }

  /// Releases resources held by this service.
  void dispose() {
    _countdownTimer?.cancel();
    _stateController.close();
  }

  void _setState(ChallengeState newState) {
    _state = newState;
    _stateController.add(newState);
  }

  // ---------------------------------------------------------------------------
  // Static display helpers
  // ---------------------------------------------------------------------------

  /// Returns a user-friendly instruction string for the given [action].
  static String getActionDisplayText(String action) {
    switch (action.toLowerCase()) {
      case 'blink':
        return 'Please blink your eyes';
      case 'smile':
        return 'Please smile';
      case 'turn_left':
        return 'Turn your head left';
      case 'turn_right':
        return 'Turn your head right';
      case 'nod_up':
        return 'Nod your head up';
      case 'nod_down':
        return 'Nod your head down';
      case 'nod':
        return 'Nod your head up and down';
      case 'open_mouth':
        return 'Open your mouth wide';
      case 'raise_eyebrows':
        return 'Raise your eyebrows';
      default:
        return 'Perform: $action';
    }
  }

  /// Returns an appropriate [IconData] for the given [action].
  static IconData getActionIcon(String action) {
    switch (action.toLowerCase()) {
      case 'blink':
        return Icons.visibility;
      case 'smile':
        return Icons.sentiment_satisfied_alt;
      case 'turn_left':
        return Icons.arrow_back;
      case 'turn_right':
        return Icons.arrow_forward;
      case 'nod_up':
        return Icons.arrow_upward;
      case 'nod_down':
        return Icons.arrow_downward;
      case 'nod':
        return Icons.swap_vert;
      case 'open_mouth':
        return Icons.mic_external_on;
      case 'raise_eyebrows':
        return Icons.face;
      default:
        return Icons.help_outline;
    }
  }
}
