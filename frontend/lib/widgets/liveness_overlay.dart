import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';

class LivenessOverlay extends StatelessWidget {
  const LivenessOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<LivenessProvider>(
      builder: (context, provider, child) {
        final result = provider.currentResult;
        final isLive = result.verdict == 'Live';
        final isSpoof = result.verdict == 'Spoof';
        final color = isLive ? Colors.green : (isSpoof ? Colors.red : Colors.orange);

        return Stack(
          children: [
            // Bounding Box (if available)
            if (result.bbox != null && result.bbox!.length == 4)
              Positioned(
                left: result.bbox![0],
                top: result.bbox![1],
                width: result.bbox![2] - result.bbox![0],
                height: result.bbox![3] - result.bbox![1],
                child: Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: color, width: 3),
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),

            // Status Panel
            Positioned(
              bottom: 40,
              left: 20,
              right: 20,
              child: Card(
                color: Colors.black54,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'Verdict: ${result.verdict}',
                        style: TextStyle(
                          color: color,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      LinearProgressIndicator(
                        value: result.confidence,
                        backgroundColor: Colors.white24,
                        color: color,
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Confidence: ${(result.confidence * 100).toStringAsFixed(1)}%',
                            style: const TextStyle(color: Colors.white),
                          ),
                          Text(
                            'Latency: ${result.processingTimeMs}ms',
                            style: const TextStyle(color: Colors.white),
                          ),
                        ],
                      ),
                      const Divider(color: Colors.white24),
                      _buildDetailRow('Primary Liveness', result.details.primaryLiveness),
                      _buildDetailRow('Behavioral Score', result.details.behavioralScore),
                      _buildDetailRow('rPPG Score', result.details.rppgScore),
                    ],
                  ),
                ),
              ),
            ),

            // Connection Status
            Positioned(
              top: 10,
              right: 10,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: provider.isConnected ? Colors.green : Colors.red,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  provider.isConnected ? 'Connected' : 'Disconnected',
                  style: const TextStyle(color: Colors.white, fontSize: 12),
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDetailRow(String label, double value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
          Text(
            (value * 100).toStringAsFixed(0) + '%',
            style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
