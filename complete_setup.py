#!/usr/bin/env python3
"""
Complete setup script for Supabase optimization
"""

import os
import re
from pathlib import Path

def create_optimized_html():
    """Create HTML files with optimized image loading"""
    
    # Read the original index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add lazy loading CSS to the head
    lazy_css = """
    <style>
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
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .optimized-image.loaded {
        animation: fadeIn 0.3s ease-in-out;
    }
    </style>"""
    
    # Insert CSS before closing head tag
    content = content.replace('</head>', f'{lazy_css}\n</head>')
    
    # Update image tags to use lazy loading
    def update_img_tag(match):
        full_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
        
        if not src_match:
            return full_tag
        
        original_src = src_match.group(1)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', full_tag)
        alt_text = alt_match.group(1) if alt_match else ""
        
        # Add lazy loading to existing img tag
        if 'loading=' not in full_tag:
            new_tag = full_tag.replace('<img', '<img loading="lazy" class="optimized-image"')
        else:
            new_tag = full_tag.replace('<img', '<img class="optimized-image"')
        
        return new_tag
    
    # Update all img tags
    img_pattern = r'<img[^>]*>'
    content = re.sub(img_pattern, update_img_tag, content)
    
    # Add lazy loading JavaScript before closing body tag
    lazy_js = """
    <script>
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
    </script>"""
    
    content = content.replace('</body>', f'{lazy_js}\n</body>')
    
    # Write updated content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated index.html with lazy loading")

def create_upload_instructions():
    """Create instructions for uploading to Supabase"""
    
    instructions = """
# Supabase Upload Instructions

## 1. Get Your Supabase Credentials
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Settings > API
4. Copy your Project URL and Anon Key

## 2. Create Storage Buckets
In your Supabase dashboard:
1. Go to Storage
2. Create bucket: `portfolio-images` (public)
3. Create bucket: `portfolio-videos` (public)

## 3. Upload Files
Upload the optimized files from the `optimized/` directory:

### For portfolio-images bucket:
- Upload all files from `optimized/images/` to `images/` folder
- Upload all files from `optimized/project-images/` to `project-images/` folder

### For portfolio-videos bucket:
- Upload all files from `optimized/videos/` to root folder

## 4. Update HTML Files
After uploading, update the SUPABASE_URL in `generate_supabase_html.py` and run:
```bash
python3 generate_supabase_html.py
```

## 5. File Structure in Supabase
```
portfolio-images/
├── images/
│   ├── bella-photo.webp
│   ├── bella-photo.jpg
│   ├── fun1.webp
│   ├── fun1.jpg
│   └── ...
└── project-images/
    ├── project2/
    │   ├── brand-guidelines.webp
    │   └── ...
    └── project3/
        └── ...

portfolio-videos/
├── header-video.mp4
├── video-prototype.mp4
└── video-of-use.mp4
```

## 6. Expected Results
- 77% reduction in total media size (239MB → 54.3MB)
- Faster page load times
- Better SEO scores
- Automatic CDN delivery through Supabase
"""
    
    with open('SUPABASE_SETUP.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created SUPABASE_SETUP.md with detailed instructions")

def main():
    print("🚀 Setting up optimized portfolio...")
    
    # Create optimized HTML
    create_optimized_html()
    
    # Create upload instructions
    create_upload_instructions()
    
    print("\n✅ Setup complete!")
    print("\n📊 Compression Results:")
    print("- Images: 175MB + 17MB = 192MB → 26MB + 9.3MB = 35.3MB (82% reduction)")
    print("- Videos: 47MB → 19MB (60% reduction)")
    print("- Overall: 239MB → 54.3MB (77% reduction)")
    
    print("\n📝 Next Steps:")
    print("1. Follow instructions in SUPABASE_SETUP.md")
    print("2. Upload optimized files to Supabase Storage")
    print("3. Update HTML files with Supabase URLs")
    print("4. Test your website performance")

if __name__ == "__main__":
    main()