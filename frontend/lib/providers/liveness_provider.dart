import 'dart:typed_data';
import 'package:flutter/material.dart';
import '../models/liveness_result.dart';
import '../services/liveness_service.dart';

class LivenessProvider with ChangeNotifier {
  final LivenessService _service = LivenessService();
  LivenessResult _currentResult = LivenessResult.empty();
  bool _isProcessing = false;
  String _serverUrl = 'ws://localhost:8000/ws/verify'; // Default URL

  LivenessResult get currentResult => _currentResult;
  bool get isProcessing => _isProcessing;
  bool get isConnected => _service.isConnected;
  String get serverUrl => _serverUrl;

  LivenessProvider() {
    _service.resultStream.listen((result) {
      _currentResult = result;
      _isProcessing = false;
      notifyListeners();
    });
  }

  void setServerUrl(String url) {
    _serverUrl = url;
    notifyListeners();
  }

  Future<void> connect() async {
    await _service.connect(_serverUrl);
    notifyListeners();
  }

  void sendFrame(Uint8List frameData) {
    if (_service.isConnected) {
      _isProcessing = true;
      _service.sendFrame(frameData);
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _service.dispose();
    super.dispose();
  }
}
