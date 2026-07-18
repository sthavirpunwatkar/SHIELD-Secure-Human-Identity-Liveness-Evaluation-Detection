import 'package:web/web.dart' as web;

Future<bool> isSafeExamBrowserActive() async {
  final userAgent = web.window.navigator.userAgent.toUpperCase();
  return userAgent.contains('SEB');
}
