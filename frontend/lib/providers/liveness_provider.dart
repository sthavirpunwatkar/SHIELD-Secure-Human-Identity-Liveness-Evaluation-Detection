import 'package:flutter/material.dart';
import '../models/liveness_result.dart';
import '../services/challenge_service.dart';
import '../services/seb/seb_signer.dart';
import '../services/frame_transport_service.dart';
import '../transport/frame_transport.dart';

class LivenessProvider with ChangeNotifier {
  final FrameTransportService _transportService;
  final ChallengeService _challengeService = ChallengeService();
  
  LivenessResult _currentResult = LivenessResult.empty();
  bool _isProcessing = false;
  String _serverUrl = 'ws://127.0.0.1:8000/ws/verify'; // Default URL
  String _challengeUrl = 'ws://127.0.0.1:8000/ws/challenge';

  LivenessResult get currentResult => _currentResult;
  bool get isProcessing => _isProcessing;
  bool get isConnected => _isConnected;
  String get serverUrl => _serverUrl;
  
  bool _isConnected = false;

  ChallengeService get challengeService => _challengeService;
  ChallengeState get challengeState => _challengeService.state;

  LivenessProvider(this._transportService) {
    _transportService.messageStream.listen((jsonMessage) {
      if (jsonMessage.containsKey('verdict') || jsonMessage.containsKey('temporal_valid')) {
        _currentResult = LivenessResult.fromJson(jsonMessage);
        _isProcessing = false;
      }
      _challengeService.handleServerMessage(jsonMessage);
      notifyListeners();
    });

    _transportService.transport.connectionStateStream.listen((state) {
      final wasConnected = _isConnected;
      _isConnected = (state == TransportConnectionState.connected);
      if (wasConnected != _isConnected) {
        notifyListeners();
      }
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
    final rawUrl = isChallenge ? _challengeUrl : _serverUrl;
    final signedUrl = SebSigner.signUrl(rawUrl);

    if (isChallenge) {
      _challengeService.setConnecting();
    }
    await _transportService.connect(signedUrl);
    if (isChallenge && _isConnected) {
      _challengeService.reset();
    }
    
    // Start streaming frames if connected
    if (_isConnected) {
      _transportService.start();
    }
    notifyListeners();
  }

  void startChallengeSession() {
    if (_isConnected) {
      _transportService.transport.sendMessage({"type": "start_challenge"});
      notifyListeners();
    }
  }

  void resetChallenge() {
    _challengeService.reset();
    _currentResult = LivenessResult.empty();
    notifyListeners();
  }
  
  void disconnect() {
    _transportService.disconnect();
    notifyListeners();
  }

  @override
  void dispose() {
    _challengeService.dispose();
    _transportService.dispose();
    super.dispose();
  }
}
