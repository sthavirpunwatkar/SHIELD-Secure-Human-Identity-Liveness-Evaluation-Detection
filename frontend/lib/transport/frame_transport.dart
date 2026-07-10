import 'dart:async';
import '../models/camera_frame.dart';

enum TransportConnectionState {
  disconnected,
  connecting,
  connected,
  error
}

abstract class FrameTransport {
  Future<void> connect(String url);
  Future<void> disconnect();
  Future<void> sendFrame(CameraFrame frame);
  Future<void> sendMessage(Map<String, dynamic> message);
  Future<void> reconnect();
  void dispose();
  
  TransportConnectionState get connectionState;
  Stream<TransportConnectionState> get connectionStateStream;
  
  /// The backend might send messages back (like challenge results)
  Stream<Map<String, dynamic>> get messageStream;
}
