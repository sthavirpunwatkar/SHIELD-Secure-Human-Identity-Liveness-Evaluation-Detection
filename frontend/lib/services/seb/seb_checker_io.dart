import 'dart:io';

Future<bool> isSafeExamBrowserActive() async {
  if (Platform.isWindows) {
    try {
      final result = await Process.run('tasklist', []);
      return result.stdout.toString().toLowerCase().contains('safeexambrowser');
    } catch (_) {}
  } else if (Platform.isMacOS) {
    try {
      final result = await Process.run('ps', ['-ax']);
      return result.stdout.toString().toLowerCase().contains('safe exam browser');
    } catch (_) {}
  }
  return false;
}
