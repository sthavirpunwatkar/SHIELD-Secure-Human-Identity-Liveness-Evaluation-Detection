import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_es.dart';
import 'app_localizations_fr.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('es'),
    Locale('fr'),
  ];

  /// No description provided for @shieldTitle.
  ///
  /// In en, this message translates to:
  /// **'SHIELD'**
  String get shieldTitle;

  /// No description provided for @shieldSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Secure Human Identity & Liveness Evaluation Detection'**
  String get shieldSubtitle;

  /// No description provided for @serverUrlLabel.
  ///
  /// In en, this message translates to:
  /// **'Server WebSocket URL'**
  String get serverUrlLabel;

  /// No description provided for @failedConnect.
  ///
  /// In en, this message translates to:
  /// **'Failed to connect to backend'**
  String get failedConnect;

  /// No description provided for @passiveCheck.
  ///
  /// In en, this message translates to:
  /// **'Passive Liveness Check'**
  String get passiveCheck;

  /// No description provided for @connectPassive.
  ///
  /// In en, this message translates to:
  /// **'Connect (Passive)'**
  String get connectPassive;

  /// No description provided for @activeCheck.
  ///
  /// In en, this message translates to:
  /// **'Active Challenge Verification'**
  String get activeCheck;

  /// No description provided for @connectActive.
  ///
  /// In en, this message translates to:
  /// **'Connect (Active Challenge)'**
  String get connectActive;

  /// No description provided for @notConnected.
  ///
  /// In en, this message translates to:
  /// **'Not connected to server'**
  String get notConnected;

  /// No description provided for @retry.
  ///
  /// In en, this message translates to:
  /// **'Retry'**
  String get retry;

  /// No description provided for @initCamera.
  ///
  /// In en, this message translates to:
  /// **'Initializing Camera...'**
  String get initCamera;

  /// No description provided for @challengeVerification.
  ///
  /// In en, this message translates to:
  /// **'SHIELD Challenge Verification'**
  String get challengeVerification;

  /// No description provided for @startVerification.
  ///
  /// In en, this message translates to:
  /// **'Start Verification'**
  String get startVerification;

  /// No description provided for @tryAgain.
  ///
  /// In en, this message translates to:
  /// **'Try Again'**
  String get tryAgain;

  /// No description provided for @reCheckStatus.
  ///
  /// In en, this message translates to:
  /// **'Re-check Status'**
  String get reCheckStatus;

  /// No description provided for @actionBlink.
  ///
  /// In en, this message translates to:
  /// **'Please blink your eyes'**
  String get actionBlink;

  /// No description provided for @actionSmile.
  ///
  /// In en, this message translates to:
  /// **'Please smile'**
  String get actionSmile;

  /// No description provided for @actionTurnLeft.
  ///
  /// In en, this message translates to:
  /// **'Turn your head left'**
  String get actionTurnLeft;

  /// No description provided for @actionTurnRight.
  ///
  /// In en, this message translates to:
  /// **'Turn your head right'**
  String get actionTurnRight;

  /// No description provided for @actionNodUp.
  ///
  /// In en, this message translates to:
  /// **'Nod your head up'**
  String get actionNodUp;

  /// No description provided for @actionNodDown.
  ///
  /// In en, this message translates to:
  /// **'Nod your head down'**
  String get actionNodDown;

  /// No description provided for @actionNod.
  ///
  /// In en, this message translates to:
  /// **'Nod your head up and down'**
  String get actionNod;

  /// No description provided for @actionOpenMouth.
  ///
  /// In en, this message translates to:
  /// **'Open your mouth wide'**
  String get actionOpenMouth;

  /// No description provided for @actionRaiseEyebrows.
  ///
  /// In en, this message translates to:
  /// **'Raise your eyebrows'**
  String get actionRaiseEyebrows;

  /// No description provided for @actionPerform.
  ///
  /// In en, this message translates to:
  /// **'Perform: {action}'**
  String actionPerform(String action);

  /// No description provided for @noCameras.
  ///
  /// In en, this message translates to:
  /// **'No cameras found on this device.'**
  String get noCameras;

  /// No description provided for @cameraInitError.
  ///
  /// In en, this message translates to:
  /// **'Failed to initialize camera: {error}'**
  String cameraInitError(String error);

  /// No description provided for @virtualCameraAlert.
  ///
  /// In en, this message translates to:
  /// **'SECURITY ALERT: Virtual Camera (OBS) detected. Please use real hardware camera.'**
  String get virtualCameraAlert;

  /// No description provided for @securityLock.
  ///
  /// In en, this message translates to:
  /// **'SECURITY LOCK'**
  String get securityLock;

  /// No description provided for @sebRequired.
  ///
  /// In en, this message translates to:
  /// **'This verification must be completed inside the Safe Exam Browser (SEB) kiosk mode.'**
  String get sebRequired;

  /// No description provided for @identityVerification.
  ///
  /// In en, this message translates to:
  /// **'Identity Verification'**
  String get identityVerification;

  /// No description provided for @prepSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Follow these simple steps for a fast and secure liveness check.'**
  String get prepSubtitle;

  /// No description provided for @goodLighting.
  ///
  /// In en, this message translates to:
  /// **'Good Lighting'**
  String get goodLighting;

  /// No description provided for @goodLightingDesc.
  ///
  /// In en, this message translates to:
  /// **'Ensure your face is evenly lit without harsh shadows.'**
  String get goodLightingDesc;

  /// No description provided for @clearView.
  ///
  /// In en, this message translates to:
  /// **'Clear View'**
  String get clearView;

  /// No description provided for @clearViewDesc.
  ///
  /// In en, this message translates to:
  /// **'Remove any glasses, masks, or hats that obscure your face.'**
  String get clearViewDesc;

  /// No description provided for @positioning.
  ///
  /// In en, this message translates to:
  /// **'Positioning'**
  String get positioning;

  /// No description provided for @positioningDesc.
  ///
  /// In en, this message translates to:
  /// **'Hold your device at eye level and stay within the guide.'**
  String get positioningDesc;

  /// No description provided for @imReady.
  ///
  /// In en, this message translates to:
  /// **'I\'m Ready'**
  String get imReady;

  /// No description provided for @verificationPassed.
  ///
  /// In en, this message translates to:
  /// **'Verification Passed'**
  String get verificationPassed;

  /// No description provided for @verificationFailed.
  ///
  /// In en, this message translates to:
  /// **'Verification Failed'**
  String get verificationFailed;

  /// No description provided for @score.
  ///
  /// In en, this message translates to:
  /// **'Score: {score}%'**
  String score(String score);

  /// No description provided for @temporalOk.
  ///
  /// In en, this message translates to:
  /// **'Temporal OK'**
  String get temporalOk;

  /// No description provided for @temporalFailed.
  ///
  /// In en, this message translates to:
  /// **'Temporal Failed'**
  String get temporalFailed;

  /// No description provided for @connecting.
  ///
  /// In en, this message translates to:
  /// **'Connecting…'**
  String get connecting;

  /// No description provided for @readyToStart.
  ///
  /// In en, this message translates to:
  /// **'Ready to start'**
  String get readyToStart;

  /// No description provided for @allChallengesPassed.
  ///
  /// In en, this message translates to:
  /// **'All Challenges Passed!'**
  String get allChallengesPassed;

  /// No description provided for @challengeFailed.
  ///
  /// In en, this message translates to:
  /// **'Challenge Failed'**
  String get challengeFailed;

  /// No description provided for @anErrorOccurred.
  ///
  /// In en, this message translates to:
  /// **'An error occurred'**
  String get anErrorOccurred;

  /// No description provided for @processing.
  ///
  /// In en, this message translates to:
  /// **'Processing…'**
  String get processing;

  /// No description provided for @verdict.
  ///
  /// In en, this message translates to:
  /// **'Verdict: {verdict}'**
  String verdict(String verdict);

  /// No description provided for @confidence.
  ///
  /// In en, this message translates to:
  /// **'Confidence: {confidence}%'**
  String confidence(String confidence);

  /// No description provided for @latency.
  ///
  /// In en, this message translates to:
  /// **'Latency: {latency}ms'**
  String latency(String latency);

  /// No description provided for @primaryLiveness.
  ///
  /// In en, this message translates to:
  /// **'Primary Liveness'**
  String get primaryLiveness;

  /// No description provided for @behavioralScore.
  ///
  /// In en, this message translates to:
  /// **'Behavioral Score'**
  String get behavioralScore;

  /// No description provided for @rppgScore.
  ///
  /// In en, this message translates to:
  /// **'rPPG Score'**
  String get rppgScore;

  /// No description provided for @connected.
  ///
  /// In en, this message translates to:
  /// **'Connected'**
  String get connected;

  /// No description provided for @disconnected.
  ///
  /// In en, this message translates to:
  /// **'Disconnected'**
  String get disconnected;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'es', 'fr'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'es':
      return AppLocalizationsEs();
    case 'fr':
      return AppLocalizationsFr();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
