import 'dart:js_interop';
import 'dart:typed_data';

@JS('initWebCodecsEncoder')
external void _initWebCodecsEncoder(JSFunction onChunk);

@JS('encodeFrameFromJpegBytes')
external JSPromise _encodeFrameFromJpegBytes(JSUint8Array bytes);

class WebCodecsService {
  bool _isInitialized = false;
  Function(Uint8List)? onChunkEncoded;

  void initialize(Function(Uint8List) onChunk) {
    if (_isInitialized) return;
    onChunkEncoded = onChunk;
    
    // Create a JSFunction from our Dart callback
    final jsCallback = (JSUint8Array chunk) {
      final dartList = chunk.toDart;
      if (onChunkEncoded != null) {
        onChunkEncoded!(dartList);
      }
    }.toJS;

    _initWebCodecsEncoder(jsCallback);
    _isInitialized = true;
  }

  Future<void> encodeFrame(Uint8List jpegBytes) async {
    if (!_isInitialized) return;
    // Pass the bytes to JS for WebCodecs encoding
    await _encodeFrameFromJpegBytes(jpegBytes.toJS).toDart;
  }
}
