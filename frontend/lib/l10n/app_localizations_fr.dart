// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for French (`fr`).
class AppLocalizationsFr extends AppLocalizations {
  AppLocalizationsFr([String locale = 'fr']) : super(locale);

  @override
  String get shieldTitle => 'SHIELD';

  @override
  String get shieldSubtitle =>
      'Évaluation et Détection Sécurisée de l\'Identité Humaine et de la Vivacité';

  @override
  String get serverUrlLabel => 'URL du WebSocket du Serveur';

  @override
  String get failedConnect => 'Échec de connexion au serveur';

  @override
  String get passiveCheck => 'Vérification de Vivacité Passive';

  @override
  String get connectPassive => 'Connecter (Passif)';

  @override
  String get activeCheck => 'Vérification de Défi Actif';

  @override
  String get connectActive => 'Connecter (Défi Actif)';

  @override
  String get notConnected => 'Non connecté au serveur';

  @override
  String get retry => 'Réessayer';

  @override
  String get initCamera => 'Initialisation de la caméra...';

  @override
  String get challengeVerification => 'Vérification de Défi SHIELD';

  @override
  String get startVerification => 'Démarrer la Vérification';

  @override
  String get tryAgain => 'Réessayer';

  @override
  String get reCheckStatus => 'Revérifier le statut';

  @override
  String get actionBlink => 'Veuillez cligner des yeux';

  @override
  String get actionSmile => 'Veuillez sourire';

  @override
  String get actionTurnLeft => 'Tournez la tête à gauche';

  @override
  String get actionTurnRight => 'Tournez la tête à droite';

  @override
  String get actionNodUp => 'Hochez la tête vers le haut';

  @override
  String get actionNodDown => 'Hochez la tête vers le bas';

  @override
  String get actionNod => 'Hochez la tête de haut en bas';

  @override
  String get actionOpenMouth => 'Ouvrez grand la bouche';

  @override
  String get actionRaiseEyebrows => 'Levez les sourcils';

  @override
  String actionPerform(String action) {
    return 'Effectuer : $action';
  }

  @override
  String get noCameras => 'Aucune caméra trouvée sur cet appareil.';

  @override
  String cameraInitError(String error) {
    return 'Échec de l\'initialisation de la caméra : $error';
  }

  @override
  String get virtualCameraAlert =>
      'ALERTE SÉCURITÉ: Caméra virtuelle détectée. Utilisez une vraie caméra.';

  @override
  String get securityLock => 'VERROUILLAGE DE SÉCURITÉ';

  @override
  String get sebRequired =>
      'Cette vérification doit être effectuée dans le mode kiosque du Safe Exam Browser (SEB).';

  @override
  String get identityVerification => 'Vérification d\'Identité';

  @override
  String get prepSubtitle =>
      'Suivez ces étapes simples pour une vérification rapide et sécurisée.';

  @override
  String get goodLighting => 'Bonne Lumière';

  @override
  String get goodLightingDesc =>
      'Assurez-vous que votre visage est bien éclairé.';

  @override
  String get clearView => 'Vue Dégagée';

  @override
  String get clearViewDesc => 'Retirez vos lunettes, masques ou chapeaux.';

  @override
  String get positioning => 'Positionnement';

  @override
  String get positioningDesc => 'Tenez votre appareil à la hauteur des yeux.';

  @override
  String get imReady => 'Je Suis Prêt';

  @override
  String get verificationPassed => 'Vérification Réussie';

  @override
  String get verificationFailed => 'Échec de la Vérification';

  @override
  String score(String score) {
    return 'Score : $score%';
  }

  @override
  String get temporalOk => 'Temporel OK';

  @override
  String get temporalFailed => 'Échec Temporel';

  @override
  String get connecting => 'Connexion…';

  @override
  String get readyToStart => 'Prêt à commencer';

  @override
  String get allChallengesPassed => 'Tous les défis réussis !';

  @override
  String get challengeFailed => 'Échec du défi';

  @override
  String get anErrorOccurred => 'Une erreur s\'est produite';

  @override
  String get processing => 'Traitement…';

  @override
  String verdict(String verdict) {
    return 'Verdict : $verdict';
  }

  @override
  String confidence(String confidence) {
    return 'Confiance : $confidence%';
  }

  @override
  String latency(String latency) {
    return 'Latence : ${latency}ms';
  }

  @override
  String get primaryLiveness => 'Vivacité Primaire';

  @override
  String get behavioralScore => 'Score Comportemental';

  @override
  String get rppgScore => 'Score rPPG';

  @override
  String get connected => 'Connecté';

  @override
  String get disconnected => 'Déconnecté';
}
