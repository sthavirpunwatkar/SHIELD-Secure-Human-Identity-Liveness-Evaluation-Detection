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
            const bytes = new Uint8Array(buffer);
            
            if (chunkCallback) {
                chunkCallback(bytes, chunk.timestamp);
            }
        },
        error: (e) => {
            console.error("[WebCodecs] VideoEncoder error: ", e);
        }
    });

    encoder.configure(config);
};

window.encodeVideoFrame = function(videoFrame) {
    if (!encoder) {
        videoFrame.close();
        return;
    }
    
    try {
        // Keyframe every 30 frames
        const keyFrame = (frameCount % 30 === 0);
        
        encoder.encode(videoFrame, { keyFrame });
        frameCount++;
    } catch (e) {
        console.error("[WebCodecs] Error encoding video frame:", e);
    } finally {
        videoFrame.close();
    }
};
