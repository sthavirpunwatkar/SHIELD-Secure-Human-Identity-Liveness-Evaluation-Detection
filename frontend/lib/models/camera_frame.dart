enum FrameFormat {
  yuv420,
  bgra8888,
  rgba,
  videoFrame,
  unknown
}

String frameFormatToString(FrameFormat format) {
  switch (format) {
    case FrameFormat.yuv420: return 'yuv420';
    case FrameFormat.bgra8888: return 'bgra8888';
    case FrameFormat.rgba: return 'rgba';
    case FrameFormat.videoFrame: return 'videoFrame';
    case FrameFormat.unknown: return 'unknown';
  }
}

class CameraFrame<T> {
  final T payload;
  final DateTime timestamp;
  final int frameNumber;
  final int width;
  final int height;
  final FrameFormat imageFormat;
  final int? mediaTimestamp;
  final void Function()? onDispose;

  CameraFrame({
    required this.payload,
    required this.timestamp,
    required this.frameNumber,
    required this.width,
    required this.height,
    required this.imageFormat,
    this.mediaTimestamp,
    this.onDispose,
  });

  void dispose() {
    onDispose?.call();
  }
}
