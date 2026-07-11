import 'package:flutter/material.dart';
import 'challenge_screen.dart';

import '../services/security_service.dart';
import 'package:shield_app/l10n/app_localizations.dart';

class PreVerificationScreen extends StatefulWidget {
  const PreVerificationScreen({super.key});

  @override
  State<PreVerificationScreen> createState() => _PreVerificationScreenState();
}

class _PreVerificationScreenState extends State<PreVerificationScreen> {
  bool _isChecking = true;
  bool _isSebActive = false;

  @override
  void initState() {
    super.initState();
    _checkSebStatus();
  }

  Future<void> _checkSebStatus() async {
    final isActive = await SecurityService.isSafeExamBrowserActive();
    // For local testing, you might want to bypass this by setting it to true manually.
    // We'll enforce the strict check here as per requirements.
    if (mounted) {
      setState(() {
        _isSebActive = isActive;
        _isChecking = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isChecking) {
      return const Scaffold(
        backgroundColor: Color(0xFF0F172A),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (!_isSebActive) {
      return Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.lock_person, color: Colors.redAccent, size: 80),
                const SizedBox(height: 24),
                Text(
                  AppLocalizations.of(context)!.securityLock,
                  style: const TextStyle(
                    color: Colors.redAccent,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  "Please enter into safe browser hence closing any other apps.",
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white70, fontSize: 16),
                ),
                const SizedBox(height: 32),
                ElevatedButton(
                  onPressed: _checkSebStatus,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                  child: Text(AppLocalizations.of(context)!.reCheckStatus),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // Slate 900
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverFillRemaining(
              hasScrollBody: false,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Spacer(),
                  // Header
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          AppLocalizations.of(context)!.identityVerification,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            letterSpacing: -0.5,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          AppLocalizations.of(context)!.prepSubtitle,
                          style: const TextStyle(
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
                    title: AppLocalizations.of(context)!.goodLighting,
                    subtitle: AppLocalizations.of(context)!.goodLightingDesc,
                  ),
                  _buildPrepCard(
                    icon: Icons.face_retouching_natural,
                    title: AppLocalizations.of(context)!.clearView,
                    subtitle: AppLocalizations.of(context)!.clearViewDesc,
                  ),
                  _buildPrepCard(
                    icon: Icons.center_focus_strong_outlined,
                    title: AppLocalizations.of(context)!.positioning,
                    subtitle: AppLocalizations.of(context)!.positioningDesc,
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
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            AppLocalizations.of(context)!.imReady,
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(width: 8),
                          const Icon(Icons.arrow_forward),
                        ],
                      ),
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
