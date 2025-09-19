# Supabase Storage Setup Guide

## Step 1: Get Your Supabase Credentials

1. Go to your Supabase dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to Settings > API
4. Copy your:
   - Project URL
   - Anon (public) key

## Step 2: Create Storage Buckets

In your Supabase dashboard:

1. Go to Storage
2. Create these buckets:
   - `portfolio-images` (for images)
   - `portfolio-videos` (for videos)

## Step 3: Set Bucket Policies

For each bucket, set the following policies:

### For `portfolio-images`:
```sql
-- Allow public read access
CREATE POLICY "Public read access" ON storage.objects
FOR SELECT USING (bucket_id = 'portfolio-images');

-- Allow authenticated users to upload
CREATE POLICY "Authenticated users can upload" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'portfolio-images' AND auth.role() = 'authenticated');
```

### For `portfolio-videos`:
```sql
-- Allow public read access
CREATE POLICY "Public read access" ON storage.objects
FOR SELECT USING (bucket_id = 'portfolio-videos');

-- Allow authenticated users to upload
CREATE POLICY "Authenticated users can upload" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'portfolio-videos' AND auth.role() = 'authenticated');
```

## Step 4: Upload Files

You can upload the optimized files from the `optimized/` directory using:

1. **Supabase Dashboard**: Drag and drop files in the Storage section
2. **Supabase CLI**: Use the CLI to upload files
3. **Custom Script**: Use the provided upload scripts

## Step 5: File Structure

Upload files maintaining this structure:

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
    │   ├── brand-guidelines.jpg
    │   └── ...
    └── project3/
        ├── main.webp
        ├── main.jpg
        └── ...

portfolio-videos/
├── header-video.mp4
├── video-prototype.mp4
└── video-of-use.mp4
```

## Step 6: Get Public URLs

After uploading, you can get public URLs like:
- `https://your-project.supabase.co/storage/v1/object/public/portfolio-images/images/bella-photo.webp`
- `https://your-project.supabase.co/storage/v1/object/public/portfolio-videos/header-video.mp4`