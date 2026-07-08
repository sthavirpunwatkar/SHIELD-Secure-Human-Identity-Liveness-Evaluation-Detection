import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:developer' as developer;
import '../models/liveness_result.dart';

class LivenessService {
  WebSocketChannel? _channel;
  final StreamController<LivenessResult> _resultController = StreamController<LivenessResult>.broadcast();
  final StreamController<Map<String, dynamic>> _messageController = StreamController<Map<String, dynamic>>.broadcast();
  bool _isConnected = false;

  Stream<LivenessResult> get resultStream => _resultController.stream;
  Stream<Map<String, dynamic>> get messageStream => _messageController.stream;
  bool get isConnected => _isConnected;

  Future<void> connect(String url) async {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      _isConnected = true;
      
      _channel!.stream.listen(
        (data) {
          final Map<String, dynamic> json = jsonDecode(data);
          _messageController.add(json);
          final result = LivenessResult.fromJson(json);
          _resultController.add(result);
        },
        onError: (error) {
          developer.log('WebSocket Error: $error');
          _isConnected = false;
        },
        onDone: () {
          developer.log('WebSocket Connection Closed');
          _isConnected = false;
        },
      );
    } catch (e) {
      developer.log('Connection Error: $e');
      _isConnected = false;
    }
  }

  void sendFrame(Uint8List frameData) {
    if (_isConnected && _channel != null) {
      try {
        _channel!.sink.add(frameData);
      } catch (e) {
        developer.log('Error sending frame: $e');
        _isConnected = false;
      }
    }
  }

  void sendMessage(Map<String, dynamic> jsonMsg) {
    if (_isConnected && _channel != null) {
      _channel!.sink.add(jsonEncode(jsonMsg));
    }
  }

  void dispose() {
    _channel?.sink.close();
    _resultController.close();
    _messageController.close();
  }
}
