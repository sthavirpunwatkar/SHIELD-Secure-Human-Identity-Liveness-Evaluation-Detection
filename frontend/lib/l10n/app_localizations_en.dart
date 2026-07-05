// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get shieldTitle => 'SHIELD';

  @override
  String get shieldSubtitle =>
      'Secure Human Identity & Liveness Evaluation Detection';

  @override
  String get serverUrlLabel => 'Server WebSocket URL';

  @override
  String get failedConnect => 'Failed to connect to backend';

  @override
  String get passiveCheck => 'Passive Liveness Check';

  @override
  String get connectPassive => 'Connect (Passive)';

  @override
  String get activeCheck => 'Active Challenge Verification';

  @override
  String get connectActive => 'Connect (Active Challenge)';

  @override
  String get notConnected => 'Not connected to server';

  @override
  String get retry => 'Retry';

  @override
  String get initCamera => 'Initializing Camera...';

  @override
  String get challengeVerification => 'SHIELD Challenge Verification';

  @override
  String get startVerification => 'Start Verification';

  @override
  String get tryAgain => 'Try Again';

  @override
  String get reCheckStatus => 'Re-check Status';

  @override
  String get actionBlink => 'Please blink your eyes';

  @override
  String get actionSmile => 'Please smile';

  @override
  String get actionTurnLeft => 'Turn your head left';

  @override
  String get actionTurnRight => 'Turn your head right';

  @override
  String get actionNodUp => 'Nod your head up';

  @override
  String get actionNodDown => 'Nod your head down';

  @override
  String get actionNod => 'Nod your head up and down';

  @override
  String get actionOpenMouth => 'Open your mouth wide';

  @override
  String get actionRaiseEyebrows => 'Raise your eyebrows';

  @override
  String actionPerform(String action) {
    return 'Perform: $action';
  }

  @override
  String get noCameras => 'No cameras found on this device.';

  @override
  String cameraInitError(String error) {
    return 'Failed to initialize camera: $error';
  }

  @override
  String get virtualCameraAlert =>
      'SECURITY ALERT: Virtual Camera (OBS) detected. Please use real hardware camera.';

  @override
  String get securityLock => 'SECURITY LOCK';

  @override
  String get sebRequired =>
      'This verification must be completed inside the Safe Exam Browser (SEB) kiosk mode.';

  @override
  String get identityVerification => 'Identity Verification';

  @override
  String get prepSubtitle =>
      'Follow these simple steps for a fast and secure liveness check.';

  @override
  String get goodLighting => 'Good Lighting';

  @override
  String get goodLightingDesc =>
      'Ensure your face is evenly lit without harsh shadows.';

  @override
  String get clearView => 'Clear View';

  @override
  String get clearViewDesc =>
      'Remove any glasses, masks, or hats that obscure your face.';

  @override
  String get positioning => 'Positioning';

  @override
  String get positioningDesc =>
      'Hold your device at eye level and stay within the guide.';

  @override
  String get imReady => 'I\'m Ready';

  @override
  String get verificationPassed => 'Verification Passed';

  @override
  String get verificationFailed => 'Verification Failed';

  @override
  String score(String score) {
    return 'Score: $score%';
  }

  @override
  String get temporalOk => 'Temporal OK';

  @override
  String get temporalFailed => 'Temporal Failed';

  @override
  String get connecting => 'Connecting…';

  @override
  String get readyToStart => 'Ready to start';

  @override
  String get allChallengesPassed => 'All Challenges Passed!';

  @override
  String get challengeFailed => 'Challenge Failed';

  @override
  String get anErrorOccurred => 'An error occurred';

  @override
  String get processing => 'Processing…';

  @override
  String verdict(String verdict) {
    return 'Verdict: $verdict';
  }

  @override
  String confidence(String confidence) {
    return 'Confidence: $confidence%';
  }

  @override
  String latency(String latency) {
    return 'Latency: ${latency}ms';
  }

  @override
  String get primaryLiveness => 'Primary Liveness';

  @override
  String get behavioralScore => 'Behavioral Score';

  @override
  String get rppgScore => 'rPPG Score';

  @override
  String get connected => 'Connected';

  @override
  String get disconnected => 'Disconnected';
}
