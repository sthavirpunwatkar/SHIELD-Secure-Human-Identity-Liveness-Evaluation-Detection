import 'dart:convert';
import 'package:crypto/crypto.dart';

class SebSigner {
  static const String _configKey = 'shield-seb-secure-config-key-2026';
  static const String _configKeyHash = 'mock-config-key-hash';

  /// Signs the WebSocket URL with SEB query parameters for environments that don't support custom headers (like Flutter Web)
  static String signUrl(String baseUrl) {
    // Generate the request hash exactly like SEB would
    final input = baseUrl + _configKey;
    final bytes = utf8.encode(input);
    final requestHash = sha256.convert(bytes).toString();

    // Append to URL
    final separator = baseUrl.contains('?') ? '&' : '?';
    return '$baseUrl${separator}seb_requesthash=$requestHash&seb_configkeyhash=$_configKeyHash';
  }
}
