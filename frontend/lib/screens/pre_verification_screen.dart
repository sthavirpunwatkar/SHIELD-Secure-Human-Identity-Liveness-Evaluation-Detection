import 'package:flutter/material.dart';
import 'challenge_screen.dart';

class PreVerificationScreen extends StatelessWidget {
  const PreVerificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // Slate 900
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Spacer(),
            // Header
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Identity Verification',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      letterSpacing: -0.5,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Follow these simple steps for a fast and secure liveness check.',
                    style: TextStyle(
                      color: Color(0xFF94A3B8), // Slate 400
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 48),

            // Preparation Cards
            _buildPrepCard(
              icon: Icons.lightbulb_outline,
              title: 'Good Lighting',
              subtitle: 'Ensure your face is evenly lit without harsh shadows.',
            ),
            _buildPrepCard(
              icon: Icons.face_retouching_natural,
              title: 'Clear View',
              subtitle: 'Remove any glasses, masks, or hats that obscure your face.',
            ),
            _buildPrepCard(
              icon: Icons.center_focus_strong_outlined,
              title: 'Positioning',
              subtitle: 'Hold your device at eye level and stay within the guide.',
            ),

            const Spacer(flex: 2),

            // Action Button
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const ChallengeScreen()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF3B82F6), // Blue 500
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  elevation: 0,
                ),
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'I\'m Ready',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(width: 8),
                    Icon(Icons.arrow_forward),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPrepCard({
    required IconData icon,
    required String title,
    required String subtitle,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 8.0),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: const Color(0xFF1E293B), // Slate 800
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.white.withOpacity(0.05)),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF3B82F6).withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, color: const Color(0xFF3B82F6), size: 28),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: const TextStyle(
                      color: Color(0xFF94A3B8),
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
