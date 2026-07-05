import 'dart:html' as html;

Future<bool> isSafeExamBrowserActive() async {
  final userAgent = html.window.navigator.userAgent.toUpperCase();
  return userAgent.contains('SEB');
}
