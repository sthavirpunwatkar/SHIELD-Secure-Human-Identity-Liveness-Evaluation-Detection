class LivenessResult {
  final String verdict;
  final double confidence;
  final String status;
  final int processingTimeMs;
  final LivenessDetails details;
  final List<double>? bbox;
  final List<int>? frameSize;

  LivenessResult({
    required this.verdict,
    required this.confidence,
    required this.status,
    required this.processingTimeMs,
    required this.details,
    this.bbox,
    this.frameSize,
  });

  factory LivenessResult.fromJson(Map<String, dynamic> json) {
    return LivenessResult(
      verdict: json['verdict'] ?? 'Unknown',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      status: json['status'] ?? 'fail',
      processingTimeMs: json['processing_time_ms'] ?? 0,
      details: LivenessDetails.fromJson(json['details'] ?? {}),
      bbox: json['bbox'] != null ? List<double>.from(json['bbox'].map((e) => e.toDouble())) : null,
      frameSize: json['frame_size'] != null ? List<int>.from(json['frame_size']) : null,
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
      primaryLiveness: (json['primary_liveness'] ?? 0.0).toDouble(),
      secondaryLiveness: (json['secondary_liveness'] ?? 0.0).toDouble(),
      combinedLiveness: (json['combined_liveness'] ?? 0.0).toDouble(),
      behavioralScore: (json['behavioral_score'] ?? 0.0).toDouble(),
      rppgScore: (json['rppg_score'] ?? 0.0).toDouble(),
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
