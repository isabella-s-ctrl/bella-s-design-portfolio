#!/usr/bin/env python3
"""
Script to upload optimized media to Supabase and update HTML files
"""

import os
import sys
import requests
import json
import re
from pathlib import Path

# You'll need to replace these with your actual Supabase credentials
SUPABASE_URL = "YOUR_SUPABASE_URL"  # Replace with your actual URL
SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY"  # Replace with your actual key

def upload_file_to_supabase(file_path, bucket_name, file_name):
    """Upload a single file to Supabase Storage"""
    try:
        url = f"{SUPABASE_URL}/storage/v1/object/{bucket_name}/{file_name}"
        
        headers = {
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": get_content_type(file_path)
        }
        
        with open(file_path, 'rb') as f:
            response = requests.post(url, headers=headers, data=f)
        
        if response.status_code in [200, 201]:
            print(f"✅ Uploaded: {file_name}")
            return True
        else:
            print(f"❌ Failed to upload {file_name}: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading {file_name}: {e}")
        return False

def get_content_type(file_path):
    """Get content type based on file extension"""
    ext = Path(file_path).suffix.lower()
    content_types = {
        '.webp': 'image/webp',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime'
    }
    return content_types.get(ext, 'application/octet-stream')

def upload_directory(dir_path, bucket_name, base_path=""):
    """Upload all files in a directory recursively"""
    dir_path = Path(dir_path)
    
    if not dir_path.exists():
        print(f"❌ Directory not found: {dir_path}")
        return []
    
    uploaded_files = []
    
    for item in dir_path.iterdir():
        if item.is_file():
            file_name = f"{base_path}/{item.name}" if base_path else item.name
            if upload_file_to_supabase(item, bucket_name, file_name):
                uploaded_files.append((str(item), file_name))
        elif item.is_dir():
            new_base = f"{base_path}/{item.name}" if base_path else item.name
            uploaded_files.extend(upload_directory(item, bucket_name, new_base))
    
    return uploaded_files

def update_html_file(file_path, file_mappings):
    """Update HTML file to use Supabase URLs with lazy loading"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a mapping of local paths to Supabase URLs
        url_mapping = {}
        for local_path, supabase_path in file_mappings:
            # Convert local path to relative path used in HTML
            if 'optimized/images/' in local_path:
                relative_path = local_path.replace('optimized/images/', 'images/')
                bucket = 'portfolio-images'
            elif 'optimized/project-images/' in local_path:
                relative_path = local_path.replace('optimized/project-images/', 'project-images/')
                bucket = 'portfolio-images'
            elif 'optimized/videos/' in local_path:
                relative_path = local_path.replace('optimized/videos/', 'videos/')
                bucket = 'portfolio-videos'
            else:
                continue
            
            # Create Supabase URL
            supabase_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{supabase_path}"
            url_mapping[relative_path] = supabase_url
        
        # Update image sources
        for local_path, supabase_url in url_mapping.items():
            # Handle different image formats
            base_name = Path(local_path).stem
            ext = Path(local_path).suffix.lower()
            
            # Try to find WebP version first, then fallback to JPEG
            webp_url = supabase_url.replace(ext, '.webp')
            jpg_url = supabase_url.replace(ext, '.jpg')
            
            # Create responsive image with lazy loading
            new_img_tag = f'''<picture>
                <source srcset="{webp_url}" type="image/webp">
                <img src="{jpg_url}" alt="" loading="lazy" class="optimized-image">
            </picture>'''
            
            # Replace img tags
            img_pattern = rf'<img[^>]*src=["\']?{re.escape(local_path)}["\']?[^>]*>'
            content = re.sub(img_pattern, new_img_tag, content, flags=re.IGNORECASE)
        
        # Update video sources
        for local_path, supabase_url in url_mapping.items():
            if local_path.endswith(('.mp4', '.mov')):
                # Replace video sources
                video_pattern = rf'src=["\']?{re.escape(local_path)}["\']?'
                content = re.sub(video_pattern, f'src="{supabase_url}"', content, flags=re.IGNORECASE)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    print("🚀 Starting Supabase upload and HTML update...")
    
    # Check if optimized directory exists
    if not Path("optimized").exists():
        print("❌ Optimized directory not found. Run compression scripts first.")
        return
    
    # Check if credentials are set
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_ANON_KEY == "YOUR_SUPABASE_ANON_KEY":
        print("❌ Please update SUPABASE_URL and SUPABASE_ANON_KEY in this script")
        return
    
    # Upload files
    print("📸 Uploading optimized images...")
    image_files = upload_directory("optimized/images", "portfolio-images")
    
    print("📸 Uploading optimized project images...")
    project_files = upload_directory("optimized/project-images", "portfolio-images")
    
    print("🎥 Uploading optimized videos...")
    video_files = upload_directory("optimized/videos", "portfolio-videos")
    
    # Combine all uploaded files
    all_files = image_files + project_files + video_files
    
    if not all_files:
        print("❌ No files were uploaded successfully")
        return
    
    # Update HTML files
    print("📝 Updating HTML files...")
    html_files = ["index.html", "about.html", "fun-stuff.html", "projects/project1.html", "projects/project2.html", "projects/project3.html"]
    
    for html_file in html_files:
        if Path(html_file).exists():
            update_html_file(html_file, all_files)
    
    print("✅ Upload and update complete!")
    print(f"📊 Uploaded {len(all_files)} files to Supabase Storage")

if __name__ == "__main__":
    main()