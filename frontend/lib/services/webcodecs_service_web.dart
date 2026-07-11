import 'dart:js_interop';
import 'dart:typed_data';
import '../models/camera_frame.dart';
import '../transport/frame_encoder.dart';

@JS('initWebCodecsEncoder')
external void _initWebCodecsEncoder(JSFunction onChunk);

@JS('encodeVideoFrame')
external void _encodeVideoFrame(JSObject videoFrame);


class WebCodecsService implements FrameEncoder {
  bool _isInitialized = false;
  Function(Uint8List, [CameraFrame?])? onChunkEncoded;
  final Map<int, CameraFrame> _frameMap = {};

  @override
  void initialize(Function(Uint8List, [CameraFrame?]) onChunk) {
    if (_isInitialized) return;
    onChunkEncoded = onChunk;
    
    // Create a JSFunction from our Dart callback
    final jsCallback = (JSUint8Array chunk, JSNumber jsTimestamp) {
      final dartList = chunk.toDart;
      final mediaTimestamp = jsTimestamp.toDartDouble.toInt();
      final frame = _frameMap.remove(mediaTimestamp);
      
      if (onChunkEncoded != null) {
        onChunkEncoded!(dartList, frame);
      }
    }.toJS;

    _initWebCodecsEncoder(jsCallback);
    _isInitialized = true;
  }

  @override
  Future<void> encodeFrame(CameraFrame frame) async {
    if (!_isInitialized) return;
    
    if (frame.imageFormat == FrameFormat.videoFrame) {
      final videoFrame = frame.payload as JSObject;
      final ts = frame.mediaTimestamp;
      if (ts != null) {
        _frameMap[ts] = frame;
        
        // Cleanup strategy: keep map from leaking on dropped frames
        if (_frameMap.length > 30) {
          final sortedKeys = _frameMap.keys.toList()..sort();
          while (_frameMap.length > 30) {
            _frameMap.remove(sortedKeys.removeAt(0));
          }
        }
      }
      _encodeVideoFrame(videoFrame);
    } else {
      throw UnsupportedError('WebCodecsService only supports VideoFrame payload on the web.');
    }
  }
}
