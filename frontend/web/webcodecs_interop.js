let encoder = null;
let chunkCallback = null;
let frameCount = 0;

window.initWebCodecsEncoder = function(onChunk) {
    if (encoder) {
        try { encoder.close(); } catch (e) {}
    }
    
    chunkCallback = onChunk;
    const config = {
        codec: 'avc1.42001E', // H.264 Baseline Profile level 3.0
        width: 640,
        height: 480,
        bitrate: 1000000, // 1 Mbps
        framerate: 30,
        avc: { format: 'annexb' } // Important for backend PyAV parser
    };

    encoder = new VideoEncoder({
        output: (chunk, metadata) => {
            const buffer = new ArrayBuffer(chunk.byteLength);
            chunk.copyTo(buffer);
            if (chunkCallback) {
                // Pass back to Dart
                chunkCallback(new Uint8Array(buffer));
            }
        },
        error: (e) => {
            console.error("WebCodecs VideoEncoder error: ", e);
        }
    });

    encoder.configure(config);
};

window.encodeFrameFromJpegBytes = async function(bytesUint8Array) {
    if (!encoder) return;
    
    let bitmap = null;
    let frame = null;
    try {
        const blob = new Blob([bytesUint8Array], { type: 'image/jpeg' });
        // Resize to match encoder config
        bitmap = await createImageBitmap(blob, { resizeWidth: 640, resizeHeight: 480 });
        
        frame = new VideoFrame(bitmap, { timestamp: frameCount * 33333 }); // ~30fps
        frameCount++;
        
        // Keyframe every 30 frames
        const keyFrame = (frameCount % 30 === 0);
        encoder.encode(frame, { keyFrame });
    } catch (e) {
        console.error("Error encoding frame:", e);
    } finally {
        if (frame) frame.close();
        if (bitmap && bitmap.close) bitmap.close();
    }
};
