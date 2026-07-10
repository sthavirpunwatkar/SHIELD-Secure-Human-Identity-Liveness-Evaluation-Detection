import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:developer' as developer;

import 'frame_transport.dart';
import '../models/camera_frame.dart';
import 'frame_encoder.dart';

class CurrentWebSocketTransport implements FrameTransport {
  WebSocketChannel? _channel;
  TransportConnectionState _state = TransportConnectionState.disconnected;
  final StreamController<TransportConnectionState> _stateController = StreamController<TransportConnectionState>.broadcast();
  final StreamController<Map<String, dynamic>> _messageController = StreamController<Map<String, dynamic>>.broadcast();
  
  String? _lastUrl;
  final FrameEncoder _encoder;
  
  // Temporary storage for metadata to send along with the next chunk
  Map<String, dynamic>? _pendingMetadata;

  CurrentWebSocketTransport(this._encoder) {
    _encoder.initialize((chunkData) {
      if (_state == TransportConnectionState.connected && _channel != null) {
        try {
          if (_pendingMetadata != null) {
            _pendingMetadata!['payloadSize'] = chunkData.length;
            _channel!.sink.add(jsonEncode(_pendingMetadata));
            _pendingMetadata = null;
          }
          _channel!.sink.add(chunkData);
        } catch (e) {
          developer.log('Error sending frame data: $e');
          _updateState(TransportConnectionState.error);
        }
      }
    });
  }

  @override
  TransportConnectionState get connectionState => _state;

  @override
  Stream<TransportConnectionState> get connectionStateStream => _stateController.stream;

  @override
  Stream<Map<String, dynamic>> get messageStream => _messageController.stream;

  void _updateState(TransportConnectionState newState) {
    if (_state != newState) {
      _state = newState;
      _stateController.add(newState);
    }
  }

  @override
  Future<void> connect(String url) async {
    _lastUrl = url;
    _updateState(TransportConnectionState.connecting);
    
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      _updateState(TransportConnectionState.connected);
      
      _channel!.stream.listen(
        (data) {
          try {
            final Map<String, dynamic> json = jsonDecode(data);
            _messageController.add(json);
          } catch (e) {
            // Ignore non-JSON messages
          }
        },
        onError: (error) {
          developer.log('WebSocket Error: $error');
          _updateState(TransportConnectionState.error);
        },
        onDone: () {
          developer.log('WebSocket Connection Closed');
          _updateState(TransportConnectionState.disconnected);
        },
      );
    } catch (e) {
      developer.log('Connection Error: $e');
      _updateState(TransportConnectionState.error);
    }
  }

  @override
  Future<void> disconnect() async {
    await _channel?.sink.close();
    _channel = null;
    _updateState(TransportConnectionState.disconnected);
  }

  @override
  Future<void> reconnect() async {
    if (_lastUrl != null) {
      await disconnect();
      await connect(_lastUrl!);
    }
  }

  @override
  Future<void> sendFrame(CameraFrame frame) async {
    if (_state != TransportConnectionState.connected) return;

    // Task 4: Metadata
    _pendingMetadata = {
      'frameNumber': frame.frameNumber,
      'timestamp': frame.timestamp.toIso8601String(),
      'captureTime': DateTime.now().toIso8601String(),
      'resolution': '${frame.image.width}x${frame.image.height}',
      'width': frame.image.width,
      'height': frame.image.height,
      'imageFormat': frame.image.format.group.name,
      'compressionType': 'h264',
      'payloadSize': 0, // Will be updated when chunk is produced
    };

    // Convert frames to the current backend payload (trigger WebCodecs)
    // Here we pass a dummy Uint8List to simulate conversion, since full Dart conversion
    // from YUV420 to JPEG is complex and beyond the pure architectural scope of this PR.
    // In production, CameraImage to JPEG conversion would happen before this.
    final dummyJpegBytes = Uint8List(0);
    _encoder.encodeFrame(dummyJpegBytes);
  }

  @override
  Future<void> sendMessage(Map<String, dynamic> message) async {
    if (_state != TransportConnectionState.connected || _channel == null) return;
    _channel!.sink.add(jsonEncode(message));
  }

  @override
  void dispose() {
    disconnect();
    _stateController.close();
    _messageController.close();
  }
}
