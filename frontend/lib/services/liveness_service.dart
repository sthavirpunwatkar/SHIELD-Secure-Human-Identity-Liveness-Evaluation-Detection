import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/liveness_result.dart';

class LivenessService {
  WebSocketChannel? _channel;
  final StreamController<LivenessResult> _resultController = StreamController<LivenessResult>.broadcast();
  bool _isConnected = false;

  Stream<LivenessResult> get resultStream => _resultController.stream;
  bool get isConnected => _isConnected;

  Future<void> connect(String url) async {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      _isConnected = true;
      
      _channel!.stream.listen(
        (data) {
          final Map<String, dynamic> json = jsonDecode(data);
          final result = LivenessResult.fromJson(json);
          _resultController.add(result);
        },
        onError: (error) {
          print('WebSocket Error: $error');
          _isConnected = false;
        },
        onDone: () {
          print('WebSocket Connection Closed');
          _isConnected = false;
        },
      );
    } catch (e) {
      print('Connection Error: $e');
      _isConnected = false;
    }
  }

  void sendFrame(Uint8List frameData) {
    if (_isConnected && _channel != null) {
      _channel!.sink.add(frameData);
    }
  }

  void dispose() {
    _channel?.sink.close();
    _resultController.close();
  }
}
