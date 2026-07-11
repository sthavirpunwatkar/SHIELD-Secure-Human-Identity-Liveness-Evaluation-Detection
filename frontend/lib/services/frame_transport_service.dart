import 'dart:async';
import '../models/camera_frame.dart';
import 'camera_capture_service.dart';
import '../transport/frame_transport.dart';

class FrameTransportService {
  final CameraCaptureService _cameraService;
  final FrameTransport _transport;
  
  StreamSubscription<CameraFrame>? _frameSubscription;
  StreamSubscription<TransportConnectionState>? _stateSubscription;
  
  // Bounded send queue (Task 6)
  static const int _maxQueueSize = 30;
  final List<CameraFrame> _queue = [];
  bool _isProcessingQueue = false;

  // Metrics (Task 7)
  int framesProduced = 0;
  int framesSent = 0;
  int framesDropped = 0;
  double averageSendLatency = 0.0;
  int maximumQueueDepth = 0;
  int bandwidthEstimate = 0; // Bytes sent, can be divided by time for bps
  
  // Expose backend messages directly
  Stream<Map<String, dynamic>> get messageStream => _transport.messageStream;
  
  // Expose transport for messages and connection state
  FrameTransport get transport => _transport;

  Timer? _reconnectTimer;

  FrameTransportService(this._cameraService, this._transport) {
    _stateSubscription = _transport.connectionStateStream.listen((state) {
      if (state == TransportConnectionState.disconnected || 
          state == TransportConnectionState.error) {
        _queue.clear(); // Drop frames if disconnected
        _scheduleReconnect();
      } else if (state == TransportConnectionState.connected) {
        _reconnectTimer?.cancel();
        _reconnectTimer = null;
      }
    });
  }

  void _scheduleReconnect() {
    if (_reconnectTimer != null && _reconnectTimer!.isActive) return;
    _reconnectTimer = Timer(const Duration(seconds: 3), () {
      if (_transport.connectionState != TransportConnectionState.connected && 
          _transport.connectionState != TransportConnectionState.connecting) {
        _transport.reconnect();
      }
    });
  }

  void start() {
    if (_frameSubscription != null) return;
    _frameSubscription = _cameraService.frameStream.listen(_onFrameReceived);
  }
  
  void stop() {
    _frameSubscription?.cancel();
    _frameSubscription = null;
    _queue.clear();
  }

  void _onFrameReceived(CameraFrame frame) {
    framesProduced++;
    
    if (_queue.length >= _maxQueueSize) {
      final droppedFrame = _queue.removeAt(0); // Drop oldest frame
      droppedFrame.dispose();
      framesDropped++;
    }
    
    _queue.add(frame);
    
    if (_queue.length > maximumQueueDepth) {
      maximumQueueDepth = _queue.length;
    }
    
    _processQueue();
  }

  Future<void> _processQueue() async {
    if (_isProcessingQueue || _queue.isEmpty) return;
    _isProcessingQueue = true;

    while (_queue.isNotEmpty) {
      if (_transport.connectionState != TransportConnectionState.connected) {
        break; // Wait for connection to re-establish
      }
      
      final frame = _queue.removeAt(0);
      final startTime = DateTime.now();
      
      try {
        await _transport.sendFrame(frame);
        
        final latency = DateTime.now().difference(startTime).inMilliseconds;
        averageSendLatency = (averageSendLatency * framesSent + latency) / (framesSent + 1);
        framesSent++;
      } catch (e) {
        framesDropped++;
      }
    }
    
    _isProcessingQueue = false;
  }
  
  Future<void> connect(String url) async {
    await _transport.connect(url);
  }
  
  Future<void> disconnect() async {
    await _transport.disconnect();
    stop();
  }

  void dispose() {
    stop();
    _reconnectTimer?.cancel();
    _stateSubscription?.cancel();
    _transport.dispose();
  }
}
