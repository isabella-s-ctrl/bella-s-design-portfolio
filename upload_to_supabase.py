#!/usr/bin/env python3
"""
Upload optimized media files to Supabase Storage
"""

import os
import requests
import json
from pathlib import Path

# Supabase configuration
SUPABASE_URL = "https://rsmpxzzhelgzhkmungmd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJzbXB4enpoZWxnemhrbXVuZ21kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyOTYzOTYsImV4cCI6MjA3Mzg3MjM5Nn0._WV1O5EjUnRF39bwkb8crrmbqAxFIyMPdRpXIPM6ryU"

def upload_file(file_path, bucket_name, file_name):
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
            if upload_file(item, bucket_name, file_name):
                uploaded_files.append((str(item), file_name))
        elif item.is_dir():
            new_base = f"{base_path}/{item.name}" if base_path else item.name
            uploaded_files.extend(upload_directory(item, bucket_name, new_base))
    
    return uploaded_files

def main():
    print("🚀 Starting upload to Supabase Storage...")
    
    # Check if optimized directory exists
    if not Path("optimized").exists():
        print("❌ Optimized directory not found. Run compression scripts first.")
        return
    
    # Upload optimized images
    print("📸 Uploading optimized images...")
    image_files = upload_directory("optimized/images", "portfolio-images", "images")
    
    # Upload optimized project images
    print("📸 Uploading optimized project images...")
    project_files = upload_directory("optimized/project-images", "portfolio-images", "project-images")
    
    # Upload optimized videos
    print("🎥 Uploading optimized videos...")
    video_files = upload_directory("optimized/videos", "portfolio-videos", "videos")
    
    # Combine all uploaded files
    all_files = image_files + project_files + video_files
    
    print(f"\n✅ Upload complete! Uploaded {len(all_files)} files to Supabase Storage")
    print("\n📊 Your optimized media is now available at:")
    print(f"Images: {SUPABASE_URL}/storage/v1/object/public/portfolio-images/")
    print(f"Videos: {SUPABASE_URL}/storage/v1/object/public/portfolio-videos/")

if __name__ == "__main__":
    main()