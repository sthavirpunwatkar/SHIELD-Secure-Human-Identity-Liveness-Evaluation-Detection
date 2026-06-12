/// Represents the result of a single challenge action (e.g., blink, smile).
class ChallengeResult {
  final String action;
  final bool passed;
  final double responseTimeMs;

  ChallengeResult({
    required this.action,
    required this.passed,
    required this.responseTimeMs,
  });

  factory ChallengeResult.fromJson(Map<String, dynamic> json) {
    return ChallengeResult(
      action: json['action'] ?? '',
      passed: json['passed'] ?? false,
      responseTimeMs: (json['response_time_ms'] ?? 0.0).toDouble(),
    );
  }
}

/// Aggregated liveness result from the backend, optionally including
/// active challenge-response data when running in challenge mode.
class LivenessResult {
  final String verdict;
  final double confidence;
  final String status;
  final int processingTimeMs;
  final LivenessDetails details;
  final List<double>? bbox;
  final List<int>? frameSize;

  // Challenge-response fields
  final List<ChallengeResult>? challengeResults;
  final double? challengeScore;
  final String? currentChallenge;
  final int? challengeTimeoutS;
  final int? challengeIndex;
  final int? challengeTotal;
  final String? messageType;

  LivenessResult({
    required this.verdict,
    required this.confidence,
    required this.status,
    required this.processingTimeMs,
    required this.details,
    this.bbox,
    this.frameSize,
    this.challengeResults,
    this.challengeScore,
    this.currentChallenge,
    this.challengeTimeoutS,
    this.challengeIndex,
    this.challengeTotal,
    this.messageType,
  });

  factory LivenessResult.fromJson(Map<String, dynamic> json) {
    List<ChallengeResult>? parsedChallenges;
    if (json['challenge_results'] != null) {
      var list = json['challenge_results'] as List;
      parsedChallenges = list.map((i) => ChallengeResult.fromJson(i)).toList();
    }

    return LivenessResult(
      verdict: json['verdict'] ?? 'Unknown',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      status: json['status'] ?? 'fail',
      processingTimeMs: json['processing_time_ms'] ?? 0,
      details: LivenessDetails.fromJson(json['details'] ?? {}),
      bbox: json['bbox'] != null
          ? List<double>.from(json['bbox'].map((e) => e.toDouble()))
          : null,
      frameSize: json['frame_size'] != null
          ? List<int>.from(json['frame_size'])
          : null,
      challengeResults: parsedChallenges,
      challengeScore: json['challenge_score'] != null ? (json['challenge_score'] as num).toDouble() : null,
      currentChallenge: json['action'],
      challengeTimeoutS: json['timeout_s'],
      challengeIndex: json['index'],
      challengeTotal: json['total'],
      messageType: json['type'],
    );
  }

  factory LivenessResult.empty() {
    return LivenessResult(
      verdict: 'Waiting...',
      confidence: 0.0,
      status: 'idle',
      processingTimeMs: 0,
      details: LivenessDetails.empty(),
    );
  }
}

class LivenessDetails {
  final double primaryLiveness;
  final double secondaryLiveness;
  final double combinedLiveness;
  final double behavioralScore;
  final double rppgScore;

  LivenessDetails({
    required this.primaryLiveness,
    required this.secondaryLiveness,
    required this.combinedLiveness,
    required this.behavioralScore,
    required this.rppgScore,
  });

  factory LivenessDetails.fromJson(Map<String, dynamic> json) {
    return LivenessDetails(
      primaryLiveness: (json['primary_liveness'] ?? json['antispoof'] ?? 0.0).toDouble(),
      secondaryLiveness: (json['secondary_liveness'] ?? json['challenge'] ?? 0.0).toDouble(),
      combinedLiveness: (json['combined_liveness'] ?? json['combined'] ?? 0.0).toDouble(),
      behavioralScore: (json['behavioral_score'] ?? json['blink'] ?? 0.0).toDouble(),
      rppgScore: (json['rppg_score'] ?? json['rppg'] ?? 0.0).toDouble(),
    );
  }

  factory LivenessDetails.empty() {
    return LivenessDetails(
      primaryLiveness: 0.0,
      secondaryLiveness: 0.0,
      combinedLiveness: 0.0,
      behavioralScore: 0.0,
      rppgScore: 0.0,
    );
  }
}
