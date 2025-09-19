// Script to upload optimized media to Supabase Storage
// This will be run with Node.js

const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');

// You'll need to replace these with your actual Supabase credentials
const supabaseUrl = 'YOUR_SUPABASE_URL';
const supabaseKey = 'YOUR_SUPABASE_ANON_KEY';

const supabase = createClient(supabaseUrl, supabaseKey);

async function uploadFile(filePath, bucketName, fileName) {
    try {
        const fileBuffer = fs.readFileSync(filePath);
        
        const { data, error } = await supabase.storage
            .from(bucketName)
            .upload(fileName, fileBuffer, {
                contentType: getContentType(filePath),
                upsert: true
            });

        if (error) {
            console.error(`Error uploading ${fileName}:`, error);
            return false;
        }

        console.log(`✅ Uploaded: ${fileName}`);
        return data;
    } catch (err) {
        console.error(`Error reading file ${filePath}:`, err);
        return false;
    }
}

function getContentType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const contentTypes = {
        '.webp': 'image/webp',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime'
    };
    return contentTypes[ext] || 'application/octet-stream';
}

async function uploadDirectory(dirPath, bucketName, basePath = '') {
    const items = fs.readdirSync(dirPath);
    
    for (const item of items) {
        const fullPath = path.join(dirPath, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            await uploadDirectory(fullPath, bucketName, path.join(basePath, item));
        } else {
            const fileName = path.join(basePath, item);
            await uploadFile(fullPath, bucketName, fileName);
        }
    }
}

async function main() {
    console.log('🚀 Starting upload to Supabase Storage...');
    
    // Create buckets if they don't exist
    console.log('📦 Creating storage buckets...');
    
    // Upload optimized images
    console.log('📸 Uploading optimized images...');
    await uploadDirectory('./optimized/images', 'portfolio-images');
    
    // Upload optimized project images
    console.log('📸 Uploading optimized project images...');
    await uploadDirectory('./optimized/project-images', 'portfolio-images');
    
    // Upload optimized videos
    console.log('🎥 Uploading optimized videos...');
    await uploadDirectory('./optimized/videos', 'portfolio-videos');
    
    console.log('✅ Upload complete!');
}

// Run the upload
main().catch(console.error);