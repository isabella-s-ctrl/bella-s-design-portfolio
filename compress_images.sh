#!/bin/bash

# Image compression script for portfolio optimization
# Creates WebP and optimized JPEG versions of all images

echo "Starting image compression..."

# Create output directories
mkdir -p optimized/images
mkdir -p optimized/project-images

# Function to compress a single image
compress_image() {
    local input_file="$1"
    local output_dir="$2"
    local filename=$(basename "$input_file")
    local name="${filename%.*}"
    local ext="${filename##*.}"
    
    echo "Processing: $input_file"
    
    # Get image dimensions
    local dimensions=$(identify -format "%wx%h" "$input_file")
    local width=$(echo $dimensions | cut -d'x' -f1)
    local height=$(echo $dimensions | cut -d'x' -f2)
    
    # Determine max width based on image type
    local max_width=1920
    if [[ "$filename" == *"fun"* ]]; then
        max_width=1200  # Fun gallery images can be smaller
    elif [[ "$filename" == *"about-me"* ]]; then
        max_width=800   # About me images can be smaller
    fi
    
    # Resize if too large
    if [ "$width" -gt "$max_width" ]; then
        local new_height=$((height * max_width / width))
        local resize_cmd="-resize ${max_width}x${new_height}>"
    else
        local resize_cmd=""
    fi
    
    # Create WebP version (modern format, 80% quality)
    convert "$input_file" $resize_cmd -quality 80 -strip "optimized/$output_dir/${name}.webp"
    
    # Create optimized JPEG version (fallback, 85% quality, progressive)
    convert "$input_file" $resize_cmd -quality 85 -strip -interlace Plane "optimized/$output_dir/${name}.jpg"
    
    # Show compression results
    local original_size=$(stat -f%z "$input_file")
    local webp_size=$(stat -f%z "optimized/$output_dir/${name}.webp")
    local jpg_size=$(stat -f%z "optimized/$output_dir/${name}.jpg")
    
    echo "  Original: $(numfmt --to=iec $original_size)"
    echo "  WebP: $(numfmt --to=iec $webp_size) ($(echo "scale=1; $webp_size * 100 / $original_size" | bc)% of original)"
    echo "  JPEG: $(numfmt --to=iec $jpg_size) ($(echo "scale=1; $jpg_size * 100 / $original_size" | bc)% of original)"
    echo ""
}

# Compress main images directory
echo "Compressing main images..."
for file in images/*.{jpg,jpeg,JPG,JPEG,png,PNG}; do
    if [ -f "$file" ]; then
        compress_image "$file" "images"
    fi
done

# Compress project images
echo "Compressing project images..."
for file in project-images/**/*.{jpg,jpeg,JPG,JPEG,png,PNG}; do
    if [ -f "$file" ]; then
        # Get relative path from project-images
        local rel_path=$(echo "$file" | sed 's|project-images/||')
        local dir_path=$(dirname "$rel_path")
        mkdir -p "optimized/project-images/$dir_path"
        compress_image "$file" "project-images/$rel_path"
    fi
done

echo "Image compression complete!"
echo "Total size reduction:"
du -sh images/ project-images/
du -sh optimized/images/ optimized/project-images/