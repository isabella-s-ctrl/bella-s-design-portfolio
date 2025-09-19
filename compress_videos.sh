#!/bin/bash

# Video compression script for portfolio optimization
# Creates optimized MP4 versions of all videos

echo "Starting video compression..."

# Create output directory
mkdir -p optimized/videos

# Function to compress a single video
compress_video() {
    local input_file="$1"
    local filename=$(basename "$input_file")
    local name="${filename%.*}"
    local ext="${filename##*.}"
    
    echo "Processing: $input_file"
    
    # Get video info
    local duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$input_file")
    local width=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width -of csv=s=x:p=0 "$input_file")
    local height=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=height -of csv=s=x:p=0 "$input_file")
    
    echo "  Original: ${width}x${height}, ${duration}s"
    
    # Determine target resolution and bitrate based on content
    local target_width=$width
    local target_height=$height
    local target_bitrate="1000k"
    
    # Resize if too large (max 1080p for web)
    if [ "$height" -gt 1080 ]; then
        target_height=1080
        target_width=$((width * 1080 / height))
        # Ensure width is even for proper encoding
        target_width=$((target_width - target_width % 2))
    fi
    
    # Adjust bitrate based on resolution
    if [ "$target_height" -le 720 ]; then
        target_bitrate="800k"
    elif [ "$target_height" -le 1080 ]; then
        target_bitrate="1500k"
    fi
    
    echo "  Target: ${target_width}x${target_height}, ${target_bitrate}"
    
    # Compress video with H.264 codec, optimized for web
    ffmpeg -i "$input_file" \
        -c:v libx264 \
        -preset medium \
        -crf 23 \
        -maxrate "$target_bitrate" \
        -bufsize "$(echo $target_bitrate | sed 's/k/000/')" \
        -vf "scale=${target_width}:${target_height}" \
        -c:a aac \
        -b:a 128k \
        -movflags +faststart \
        -y \
        "optimized/videos/${name}.mp4"
    
    # Show compression results
    local original_size=$(stat -f%z "$input_file")
    local compressed_size=$(stat -f%z "optimized/videos/${name}.mp4")
    
    echo "  Original: $(numfmt --to=iec $original_size)"
    echo "  Compressed: $(numfmt --to=iec $compressed_size) ($(echo "scale=1; $compressed_size * 100 / $original_size" | bc)% of original)"
    echo ""
}

# Compress videos
for file in videos/*.{mp4,mov,MOV,MP4}; do
    if [ -f "$file" ]; then
        compress_video "$file"
    fi
done

# Also check for videos in images directory (like video-of-use.mov)
for file in images/*.{mp4,mov,MOV,MP4}; do
    if [ -f "$file" ]; then
        compress_video "$file"
    fi
done

echo "Video compression complete!"
echo "Total size reduction:"
du -sh videos/ images/*.{mp4,mov,MOV,MP4} 2>/dev/null || du -sh videos/
du -sh optimized/videos/