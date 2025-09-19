#!/usr/bin/env python3
"""
Generate updated HTML files with Supabase URLs and lazy loading
"""

import os
import re
from pathlib import Path

# Replace with your actual Supabase project URL
# You can find this in your Supabase dashboard under Settings > API
SUPABASE_URL = "https://rsmpxzzhelgzhkmungmd.supabase.co"

def create_supabase_url(local_path, bucket="portfolio-images"):
    """Convert local path to Supabase URL"""
    # Remove leading path components and normalize
    if local_path.startswith("images/"):
        supabase_path = f"images/{Path(local_path).name}"
    elif local_path.startswith("project-images/"):
        supabase_path = f"project-images/{Path(local_path).name}"
    elif local_path.startswith("videos/"):
        supabase_path = f"videos/{Path(local_path).name}"
        bucket = "portfolio-videos"
    else:
        supabase_path = Path(local_path).name
    
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{supabase_path}"

def update_image_tag(match):
    """Update img tag to use WebP with JPEG fallback and lazy loading"""
    full_tag = match.group(0)
    src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
    
    if not src_match:
        return full_tag
    
    original_src = src_match.group(1)
    
    # Skip if already a Supabase URL
    if "supabase.co" in original_src:
        return full_tag
    
    # Create WebP and JPEG URLs
    base_name = Path(original_src).stem
    webp_url = create_supabase_url(original_src).replace(Path(original_src).suffix, '.webp')
    jpg_url = create_supabase_url(original_src).replace(Path(original_src).suffix, '.jpg')
    
    # Extract alt text
    alt_match = re.search(r'alt=["\']([^"\']*)["\']', full_tag)
    alt_text = alt_match.group(1) if alt_match else ""
    
    # Create new picture element with lazy loading
    new_tag = f'''<picture>
                <source srcset="{webp_url}" type="image/webp">
                <img src="{jpg_url}" alt="{alt_text}" loading="lazy" class="optimized-image">
            </picture>'''
    
    return new_tag

def update_video_tag(match):
    """Update video tag to use Supabase URL"""
    full_tag = match.group(0)
    src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
    
    if not src_match:
        return full_tag
    
    original_src = src_match.group(1)
    
    # Skip if already a Supabase URL
    if "supabase.co" in original_src:
        return full_tag
    
    # Create Supabase URL
    supabase_url = create_supabase_url(original_src, "portfolio-videos")
    
    # Replace the src attribute
    new_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{supabase_url}"', full_tag)
    
    return new_tag

def update_html_file(file_path):
    """Update HTML file to use Supabase URLs"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update image tags
        img_pattern = r'<img[^>]*src=["\'][^"\']*\.(jpg|jpeg|png|JPG|JPEG|PNG)[^"\']*["\'][^>]*>'
        content = re.sub(img_pattern, update_image_tag, content, flags=re.IGNORECASE)
        
        # Update video tags
        video_pattern = r'<video[^>]*src=["\'][^"\']*\.(mp4|mov|MP4|MOV)[^"\']*["\'][^>]*>'
        content = re.sub(video_pattern, update_video_tag, content, flags=re.IGNORECASE)
        
        # Also handle source tags in video elements
        source_pattern = r'<source[^>]*src=["\'][^"\']*\.(mp4|mov|MP4|MOV)[^"\']*["\'][^>]*>'
        content = re.sub(source_pattern, update_video_tag, content, flags=re.IGNORECASE)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_lazy_loading_css():
    """Add CSS for lazy loading and optimized images"""
    css_content = """
/* Lazy loading and optimized image styles */
.optimized-image {
    transition: opacity 0.3s ease;
}

.optimized-image[loading="lazy"] {
    opacity: 0;
}

.optimized-image[loading="lazy"].loaded {
    opacity: 1;
}

/* Smooth loading animation */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.optimized-image.loaded {
    animation: fadeIn 0.3s ease-in-out;
}
"""
    
    # Add to style.css
    css_file = Path("css/style.css")
    if css_file.exists():
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write(css_content)
        print("✅ Added lazy loading CSS to style.css")

def add_lazy_loading_js():
    """Add JavaScript for lazy loading"""
    js_content = """
// Lazy loading for optimized images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.addEventListener('load', () => {
                    img.classList.add('loaded');
                });
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});
"""
    
    # Add to script.js
    js_file = Path("js/script.js")
    if js_file.exists():
        with open(js_file, 'a', encoding='utf-8') as f:
            f.write(js_content)
        print("✅ Added lazy loading JavaScript to script.js")

def main():
    print("🚀 Generating updated HTML files with Supabase URLs...")
    
    # Check if Supabase URL is set
    if SUPABASE_URL == "https://your-project-ref.supabase.co":
        print("❌ Please update SUPABASE_URL in this script with your actual Supabase project URL")
        return
    
    # HTML files to update
    html_files = [
        "index.html",
        "about.html", 
        "fun-stuff.html",
        "projects/project1.html",
        "projects/project2.html",
        "projects/project3.html"
    ]
    
    # Update HTML files
    updated_count = 0
    for html_file in html_files:
        if Path(html_file).exists():
            if update_html_file(html_file):
                updated_count += 1
    
    # Add lazy loading support
    add_lazy_loading_css()
    add_lazy_loading_js()
    
    print(f"✅ Updated {updated_count} HTML files")
    print("📝 Next steps:")
    print("1. Upload your optimized files to Supabase Storage")
    print("2. Update the SUPABASE_URL in this script with your actual URL")
    print("3. Test your website to ensure images load correctly")

if __name__ == "__main__":
    main()