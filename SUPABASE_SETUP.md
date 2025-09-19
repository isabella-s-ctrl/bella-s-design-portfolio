
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
