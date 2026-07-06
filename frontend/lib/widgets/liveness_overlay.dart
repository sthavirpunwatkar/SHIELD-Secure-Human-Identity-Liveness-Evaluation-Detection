import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/liveness_provider.dart';
import 'package:shield_app/l10n/app_localizations.dart';

class LivenessOverlay extends StatelessWidget {
  const LivenessOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<LivenessProvider>(
      builder: (context, provider, child) {
        final l10n = AppLocalizations.of(context)!;
        final result = provider.currentResult;
        final isLive = result.verdict == 'Live';
        final isSpoof = result.verdict == 'Spoof';
        final color = isLive ? Colors.green : (isSpoof ? Colors.red : Colors.orange);

        return LayoutBuilder(
          builder: (context, constraints) {
            double scaleX = 1.0;
            double scaleY = 1.0;

            if (result.frameSize != null && result.frameSize!.length == 2) {
              scaleX = constraints.maxWidth / result.frameSize![0];
              scaleY = constraints.maxHeight / result.frameSize![1];
            }

            return Stack(
              children: [
                // Bounding Box (scaled)
                if (result.bbox != null && result.bbox!.length == 4)
                  Positioned(
                    left: result.bbox![0] * scaleX,
                    top: result.bbox![1] * scaleY,
                    width: (result.bbox![2] - result.bbox![0]) * scaleX,
                    height: (result.bbox![3] - result.bbox![1]) * scaleY,
                    child: Container(
                      decoration: BoxDecoration(
                        border: Border.all(color: color, width: 3),
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                if (result.bbox != null && result.bbox!.length == 4)
                  Positioned(
                    left: result.bbox![0] * scaleX,
                    top: (result.bbox![1] * scaleY) - 20,
                    child: Text(
                      'Score: ${(result.confidence * 100).toStringAsFixed(1)}%',
                      style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
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
                            l10n.verdict(result.verdict),
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
                                l10n.confidence((result.confidence * 100).toStringAsFixed(1)),
                                style: const TextStyle(color: Colors.white),
                              ),
                              Text(
                                l10n.latency(result.processingTimeMs.toString()),
                                style: const TextStyle(color: Colors.white),
                              ),
                            ],
                          ),
                          const Divider(color: Colors.white24),
                          _buildDetailRow(l10n.primaryLiveness, result.details.primaryLiveness),
                          _buildDetailRow(l10n.behavioralScore, result.details.behavioralScore),
                          _buildDetailRow(l10n.rppgScore, result.details.rppgScore),
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
                      provider.isConnected ? l10n.connected : l10n.disconnected,
                      style: const TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  ),
                ),
              ],
            );
          },
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
            '${(value * 100).toStringAsFixed(0)}%',
            style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
