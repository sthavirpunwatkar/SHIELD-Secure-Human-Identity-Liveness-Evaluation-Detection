import 'dart:io';
import 'package:flutter/foundation.dart';

class SecurityService {
  /// Checks for the presence of known virtual camera drivers at the OS level.
  /// Returns `true` if a virtual camera is detected, `false` otherwise.
  static Future<bool> hasVirtualCamera() async {
    if (kIsWeb) {
      // Web browsers abstract hardware. Cannot do OS-level check here.
      return false;
    }

    if (Platform.isLinux) {
      return _checkLinuxVirtualCamera();
    } else if (Platform.isWindows) {
      return _checkWindowsVirtualCamera();
    } else if (Platform.isMacOS) {
      return _checkMacOSVirtualCamera();
    }

    return false;
  }

  static Future<bool> _checkLinuxVirtualCamera() async {
    // v4l2loopback is the standard module for OBS Virtual Camera and others on Linux.
    final v4l2LoopbackDir = Directory('/sys/module/v4l2loopback');
    if (await v4l2LoopbackDir.exists()) {
      debugPrint('SECURITY ALERT: v4l2loopback module detected (Virtual Camera).');
      return true;
    }
    
    // Also check lsmod just in case sysfs is restricted but lsmod works
    try {
      final result = await Process.run('lsmod', []);
      if (result.stdout.toString().contains('v4l2loopback')) {
        debugPrint('SECURITY ALERT: v4l2loopback found in lsmod.');
        return true;
      }
    } catch (e) {
      debugPrint('Failed to run lsmod: $e');
    }

    return false;
  }

  static Future<bool> _checkWindowsVirtualCamera() async {
    try {
      // Querying the registry for DirectShow capture devices
      final result = await Process.run('reg', [
        'query',
        r'HKLM\SOFTWARE\Classes\CLSID\{860BB310-5D01-11d0-BD3B-00A0C911CE86}\Instance',
        '/s'
      ]);
      final output = result.stdout.toString().toLowerCase();
      
      final suspiciousNames = [
        'obs-camera',
        'obs virtual camera',
        'e2esoft',
        'splitcam',
        'manycam',
        'xsplit',
        'snap camera',
      ];
      
      for (final name in suspiciousNames) {
        if (output.contains(name)) {
          debugPrint('SECURITY ALERT: Virtual Camera found in registry ($name).');
          return true;
        }
      }
    } catch (e) {
      debugPrint('Failed to run reg query: $e');
    }
    return false;
  }

  static Future<bool> _checkMacOSVirtualCamera() async {
    final knownPlugins = [
      'obs-mac-virtualcam.plugin',
      'CamTwist.plugin',
      'ManyCamVideoDevicePlugin.plugin',
      'LogiCapture.plugin',
      'EpocCamPlugin.plugin',
      'XSplitCoreMediaIO.plugin',
      'SnapCamera.plugin',
    ];
    
    final dalDir = Directory('/Library/CoreMediaIO/Plug-Ins/DAL');
    if (await dalDir.exists()) {
      try {
        final entities = await dalDir.list().toList();
        for (final entity in entities) {
          final name = entity.path.split(Platform.pathSeparator).last;
          if (knownPlugins.contains(name)) {
            debugPrint('SECURITY ALERT: Virtual Camera plugin detected ($name).');
            return true;
          }
        }
      } catch (e) {
        debugPrint('Failed to list DAL directory: $e');
      }
    }
    
    // Also explicitly check the one from TODO
    final obsPlugin = Directory('/Library/CoreMediaIO/Plug-Ins/DAL/obs-mac-virtualcam.plugin');
    if (await obsPlugin.exists()) {
      debugPrint('SECURITY ALERT: obs-mac-virtualcam.plugin detected.');
      return true;
    }
    
    return false;
  }
}
