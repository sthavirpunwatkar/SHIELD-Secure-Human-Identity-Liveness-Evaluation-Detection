import 'dart:js_interop';
import 'dart:js_interop_unsafe';
import 'dart:developer' as developer;
import 'package:flutter/widgets.dart';
import 'dart:ui_web' as ui_web;
import 'package:web/web.dart' as web;
import '../models/camera_frame.dart';

@JS('navigator.mediaDevices.getUserMedia')
external JSPromise _getUserMedia(JSObject constraints);

@JS('MediaStreamTrackProcessor')
extension type MediaStreamTrackProcessor._(JSObject _) implements JSObject {
  external factory MediaStreamTrackProcessor(JSObject options);
  external JSObject get readable;
}

@JS()
extension type ReadableStreamDefaultReader(JSObject _) implements JSObject {
  external JSPromise read();
}

@JS()
extension type ReadableStreamReadResult(JSObject _) implements JSObject {
  external JSBoolean get done;
  external JSObject get value;
}

@JS()
extension type VideoFrame(JSObject _) implements JSObject {
  external JSNumber get codedWidth;
  external JSNumber get codedHeight;
  external JSNumber get timestamp;
  external void close();
}

class WebCaptureService {
  JSObject? _mediaStream;
  JSObject? _videoTrack;
  bool _isStreaming = false;
  int _frameCount = 0;

  Future<void> initialize() async {
    final constraints = {'video': true, 'audio': false}.jsify() as JSObject;
    final promise = _getUserMedia(constraints);
    _mediaStream = (await promise.toDart) as JSObject?;
  }

  void startStreaming(Function(CameraFrame<dynamic>) onFrame) {
    if (_mediaStream == null || _isStreaming) return;
    _isStreaming = true;
    _frameCount = 0;

    final tracks = _mediaStream!.callMethod('getVideoTracks'.toJS) as JSArray;
    if (tracks.length == 0) return;
    _videoTrack = tracks.getProperty(0.toJS) as JSObject;

    final processor = MediaStreamTrackProcessor({'track': _videoTrack}.jsify() as JSObject);
    final readable = processor.readable;
    final reader = readable.callMethod('getReader'.toJS) as JSObject;

    _readLoop(reader, onFrame);
  }

  Future<void> _readLoop(JSObject reader, Function(CameraFrame<dynamic>) onFrame) async {
    while (_isStreaming) {
      try {
        final resultPromise = (reader as ReadableStreamDefaultReader).read();
        final result = await resultPromise.toDart as ReadableStreamReadResult;
        
        final done = result.done.toDart;
        if (done) break;

        final videoFrame = result.value as VideoFrame;
        final width = videoFrame.codedWidth.toDartInt;
        final height = videoFrame.codedHeight.toDartInt;
        final mediaTimestamp = videoFrame.timestamp.toDartDouble.toInt();

        final frame = CameraFrame<JSObject>(
          payload: videoFrame as JSObject,
          timestamp: DateTime.now(),
          frameNumber: _frameCount++,
          width: width,
          height: height,
          imageFormat: FrameFormat.videoFrame,
          mediaTimestamp: mediaTimestamp,
        );

        onFrame(frame);

        // NOTE: In a real implementation, we would call videoFrame.close() 
        // after it is encoded, but since encoding isn't implemented here, 
        // we leave it to be garbage collected or closed by the encoder later.
      } catch (e) {
        developer.log('Error reading frame: $e');
        break;
      }
    }
  }

  void stopStreaming() {
    _isStreaming = false;
    if (_videoTrack != null) {
      _videoTrack!.callMethod('stop'.toJS);
      _videoTrack = null;
    }
  }

  void dispose() {
    stopStreaming();
  }

  bool _viewRegistered = false;
  Widget? _cachedPreview;

  Widget buildPreview() {
    if (_mediaStream == null) return const SizedBox();

    if (_cachedPreview != null) return _cachedPreview!;

    final viewType = 'web-camera-preview';

    if (!_viewRegistered) {
      ui_web.platformViewRegistry.registerViewFactory(viewType, (int viewId) {
        final video = web.HTMLVideoElement()
          ..autoplay = true
          ..muted = true
          ..playsInline = true;
        
        (video as JSObject).setProperty('srcObject'.toJS, _mediaStream!);
        
        video.style
          ..objectFit = 'cover'
          ..width = '100%'
          ..height = '100%';
          
        return video;
      });
      _viewRegistered = true;
    }

    _cachedPreview = HtmlElementView(viewType: viewType);
    return _cachedPreview!;
  }
}
