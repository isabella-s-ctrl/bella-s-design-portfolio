#!/usr/bin/env python3
"""
Script to upload optimized media files to Supabase Storage
"""

import os
import sys
import requests
import json
from pathlib import Path

# Configuration - you'll need to replace these with your actual values
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY"

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
        return
    
    for item in dir_path.iterdir():
        if item.is_file():
            file_name = f"{base_path}/{item.name}" if base_path else item.name
            upload_file_to_supabase(item, bucket_name, file_name)
        elif item.is_dir():
            new_base = f"{base_path}/{item.name}" if base_path else item.name
            upload_directory(item, bucket_name, new_base)

def main():
    print("🚀 Starting upload to Supabase Storage...")
    
    # Check if optimized directory exists
    if not Path("optimized").exists():
        print("❌ Optimized directory not found. Run compression scripts first.")
        return
    
    # Upload optimized images
    print("📸 Uploading optimized images...")
    upload_directory("optimized/images", "portfolio-images")
    
    # Upload optimized project images
    print("📸 Uploading optimized project images...")
    upload_directory("optimized/project-images", "portfolio-images")
    
    # Upload optimized videos
    print("🎥 Uploading optimized videos...")
    upload_directory("optimized/videos", "portfolio-videos")
    
    print("✅ Upload complete!")

if __name__ == "__main__":
    main()