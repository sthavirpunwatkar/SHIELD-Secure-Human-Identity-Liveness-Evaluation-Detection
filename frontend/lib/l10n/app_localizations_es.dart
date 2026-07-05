// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Spanish Castilian (`es`).
class AppLocalizationsEs extends AppLocalizations {
  AppLocalizationsEs([String locale = 'es']) : super(locale);

  @override
  String get shieldTitle => 'SHIELD';

  @override
  String get shieldSubtitle =>
      'Evaluación y Detección Segura de Identidad Humana y Vitalidad';

  @override
  String get serverUrlLabel => 'URL de WebSocket del Servidor';

  @override
  String get failedConnect => 'Error al conectar con el servidor';

  @override
  String get passiveCheck => 'Comprobación de Vitalidad Pasiva';

  @override
  String get connectPassive => 'Conectar (Pasivo)';

  @override
  String get activeCheck => 'Verificación de Desafío Activo';

  @override
  String get connectActive => 'Conectar (Desafío Activo)';

  @override
  String get notConnected => 'No conectado al servidor';

  @override
  String get retry => 'Reintentar';

  @override
  String get initCamera => 'Inicializando Cámara...';

  @override
  String get challengeVerification => 'Verificación de Desafío SHIELD';

  @override
  String get startVerification => 'Iniciar Verificación';

  @override
  String get tryAgain => 'Intentar de Nuevo';

  @override
  String get reCheckStatus => 'Volver a Comprobar el Estado';

  @override
  String get actionBlink => 'Por favor, parpadee';

  @override
  String get actionSmile => 'Por favor, sonría';

  @override
  String get actionTurnLeft => 'Gire la cabeza a la izquierda';

  @override
  String get actionTurnRight => 'Gire la cabeza a la derecha';

  @override
  String get actionNodUp => 'Asiente con la cabeza hacia arriba';

  @override
  String get actionNodDown => 'Asiente con la cabeza hacia abajo';

  @override
  String get actionNod => 'Asiente con la cabeza hacia arriba y hacia abajo';

  @override
  String get actionOpenMouth => 'Abra la boca';

  @override
  String get actionRaiseEyebrows => 'Levante las cejas';

  @override
  String actionPerform(String action) {
    return 'Realizar: $action';
  }

  @override
  String get noCameras => 'No se encontraron cámaras en este dispositivo.';

  @override
  String cameraInitError(String error) {
    return 'Error al inicializar la cámara: $error';
  }

  @override
  String get virtualCameraAlert =>
      'ALERTA DE SEGURIDAD: Cámara virtual detectada. Use una cámara real.';

  @override
  String get securityLock => 'BLOQUEO DE SEGURIDAD';

  @override
  String get sebRequired =>
      'Esta verificación debe completarse dentro del modo quiosco de Safe Exam Browser (SEB).';

  @override
  String get identityVerification => 'Verificación de Identidad';

  @override
  String get prepSubtitle =>
      'Siga estos sencillos pasos para una verificación rápida y segura.';

  @override
  String get goodLighting => 'Buena Iluminación';

  @override
  String get goodLightingDesc =>
      'Asegúrese de que su rostro esté iluminado uniformemente.';

  @override
  String get clearView => 'Vista Clara';

  @override
  String get clearViewDesc => 'Quítese cualquier gafa, máscara o sombrero.';

  @override
  String get positioning => 'Posicionamiento';

  @override
  String get positioningDesc =>
      'Mantenga el dispositivo a la altura de los ojos y dentro de la guía.';

  @override
  String get imReady => 'Estoy Listo';

  @override
  String get verificationPassed => 'Verificación Aprobada';

  @override
  String get verificationFailed => 'Verificación Fallida';

  @override
  String score(String score) {
    return 'Puntuación: $score%';
  }

  @override
  String get temporalOk => 'Temporal OK';

  @override
  String get temporalFailed => 'Fallo Temporal';

  @override
  String get connecting => 'Conectando…';

  @override
  String get readyToStart => 'Listo para comenzar';

  @override
  String get allChallengesPassed => '¡Todos los desafíos superados!';

  @override
  String get challengeFailed => 'Desafío fallido';

  @override
  String get anErrorOccurred => 'Ocurrió un error';

  @override
  String get processing => 'Procesando…';

  @override
  String verdict(String verdict) {
    return 'Veredicto: $verdict';
  }

  @override
  String confidence(String confidence) {
    return 'Confianza: $confidence%';
  }

  @override
  String latency(String latency) {
    return 'Latencia: ${latency}ms';
  }

  @override
  String get primaryLiveness => 'Vitalidad Primaria';

  @override
  String get behavioralScore => 'Puntuación de Comportamiento';

  @override
  String get rppgScore => 'Puntuación rPPG';

  @override
  String get connected => 'Conectado';

  @override
  String get disconnected => 'Desconectado';
}
