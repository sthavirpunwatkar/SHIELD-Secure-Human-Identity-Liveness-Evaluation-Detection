import 'dart:typed_data';
import 'package:flutter/material.dart';
import '../models/liveness_result.dart';
import '../services/liveness_service.dart';
import '../services/challenge_service.dart';

class LivenessProvider with ChangeNotifier {
  final LivenessService _service = LivenessService();
  final ChallengeService _challengeService = ChallengeService();
  LivenessResult _currentResult = LivenessResult.empty();
  bool _isProcessing = false;
  String _serverUrl = 'ws://localhost:8000/ws/verify'; // Default URL
  String _challengeUrl = 'ws://localhost:8000/ws/challenge';

  LivenessResult get currentResult => _currentResult;
  bool get isProcessing => _isProcessing;
  bool get isConnected => _service.isConnected;
  String get serverUrl => _serverUrl;
  
  ChallengeService get challengeService => _challengeService;
  ChallengeState get challengeState => _challengeService.state;

  LivenessProvider() {
    _service.resultStream.listen((result) {
      _currentResult = result;
      _isProcessing = false;
      notifyListeners();
    });
    
    _service.messageStream.listen((jsonMessage) {
      _challengeService.handleServerMessage(jsonMessage);
      notifyListeners();
    });

    _challengeService.stateStream.listen((state) {
      notifyListeners();
    });
  }

  void setServerUrl(String url) {
    _serverUrl = url;
    if (url.endsWith('/ws/verify')) {
      _challengeUrl = url.replaceAll('/ws/verify', '/ws/challenge');
    } else {
      _challengeUrl = url; // Fallback
    }
    notifyListeners();
  }

  Future<void> connect({bool isChallenge = false}) async {
    final url = isChallenge ? _challengeUrl : _serverUrl;
    if (isChallenge) {
      _challengeService.setConnecting();
    }
    await _service.connect(url);
    if (isChallenge && _service.isConnected) {
      _challengeService.reset();
    }
    notifyListeners();
  }

  void sendFrame(Uint8List frameData) {
    if (_service.isConnected) {
      _isProcessing = true;
      _service.sendFrame(frameData);
      notifyListeners();
    }
  }

  void startChallengeSession() {
    if (_service.isConnected) {
      _service.sendMessage({"type": "start_challenge"});
      notifyListeners();
    }
  }

  void resetChallenge() {
    _challengeService.reset();
    _currentResult = LivenessResult.empty();
    notifyListeners();
  }

  @override
  void dispose() {
    _service.dispose();
    _challengeService.dispose();
    super.dispose();
  }
}
