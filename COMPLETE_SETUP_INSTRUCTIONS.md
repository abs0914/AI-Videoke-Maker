# Complete Setup Instructions

## 🎯 Overview

This document provides step-by-step instructions to deploy the Basic Pitch API service and integrate it with your Lovable app.

**Total Time: 30-45 minutes**

---

## ✅ Phase 1: Repository Setup (Already Complete)

All files are in place:
- ✅ `basic-pitch-service/app.py` - Flask API
- ✅ `basic-pitch-service/requirements.txt` - Dependencies
- ✅ `basic-pitch-service/Dockerfile` - Container config
- ✅ `lovable-app/supabase/functions/extract-pitch/index.ts` - Edge function
- ✅ `lovable-app/src/hooks/usePitchExtraction.ts` - React hook
- ✅ Repository pushed to GitHub

---

## 🚀 Phase 2: Deploy to Railway (10-15 minutes)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your GitHub account

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub"**
3. Select repository: **AI-Videoke-Maker**

### Step 3: Configure Service
1. Railway auto-detects `basic-pitch-service/Dockerfile`
2. Click **"Deploy"**
3. Wait for build to complete (2-5 minutes)

### Step 4: Get Service URL
1. In Railway dashboard, find your service
2. Click on the service
3. Go to **Settings** → **Networking**
4. Copy the public URL (e.g., `https://ai-videoke-maker-production.up.railway.app`)
5. **Save this URL** - you'll need it for Lovable

### Step 5: Verify Deployment
```bash
curl https://your-service.railway.app/health
# Expected: {"status": "healthy", "service": "basic-pitch"}
```

---

## 🔧 Phase 3: Configure Lovable App (10-15 minutes)

### Step 1: Set Environment Variables

Create or update `lovable-app/.env.local`:

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# Basic Pitch Service URL (from Railway)
VITE_BASIC_PITCH_API_URL=https://your-service.railway.app
```

**Where to find these values:**
- **Supabase URL & Key**: Supabase dashboard → Settings → API
- **Basic Pitch API URL**: Railway dashboard (your deployed service)

### Step 2: Deploy Supabase Edge Function

**Option A: Using Supabase CLI (Recommended)**

```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login

# Deploy the edge function
supabase functions deploy extract-pitch --project-id your-project-id
```

**Option B: Manual Deployment**

1. Go to Supabase dashboard
2. Navigate to **Edge Functions**
3. Create new function: `extract-pitch`
4. Copy content from `lovable-app/supabase/functions/extract-pitch/index.ts`
5. Deploy

### Step 3: Set Edge Function Environment Variable

1. Go to Supabase dashboard
2. Navigate to **Edge Functions** → **extract-pitch**
3. Click **Settings**
4. Add environment variable:
   - **Key:** `BASIC_PITCH_SERVICE_URL`
   - **Value:** `https://your-railway-service.railway.app`
5. Save

### Step 4: Test Lovable Integration

```bash
# Start Lovable dev server
npm run dev

# In your browser, test the audio upload feature
# Check browser console for results
```

---

## 📝 Phase 4: Verify Everything Works

### Test 1: Health Check
```bash
curl https://your-service.railway.app/health
```
Expected: `{"status": "healthy", "service": "basic-pitch"}`

### Test 2: Extract Pitch
```bash
curl -X POST \
  -F "audio=@sample.wav" \
  https://your-service.railway.app/api/pitch
```
Expected: JSON with pitch data

### Test 3: Lovable Integration
1. Open Lovable app in browser
2. Upload an audio file
3. Check that pitch data is returned
4. Verify no errors in console

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `RAILWAY_DEPLOYMENT_GUIDE.md` | Detailed Railway setup |
| `LOVABLE_INTEGRATION_GUIDE.md` | Detailed Lovable setup |
| `API_TESTING_GUIDE.md` | API testing procedures |
| `DEPLOYMENT_QUICK_REFERENCE.md` | Quick reference card |
| `DEPLOYMENT_CHECKLIST.md` | Task checklist |

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| GitHub Repo | https://github.com/abs0914/AI-Videoke-Maker |
| Railway Dashboard | https://railway.app |
| Supabase Dashboard | https://supabase.com |
| Lovable | https://lovable.dev |

---

## 🐛 Troubleshooting

### Railway Deployment Issues
- **Build fails**: Check `requirements.txt` is in `basic-pitch-service/`
- **Service won't start**: Verify port 8080 in Dockerfile
- **Health check fails**: Check Railway logs

### Lovable Integration Issues
- **Edge function 405**: Use POST method
- **"No audio file"**: Verify FormData key is "audio"
- **Timeout**: Check file size < 50MB

See `LOVABLE_INTEGRATION_GUIDE.md` for more troubleshooting.

---

## 📊 API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "service": "basic-pitch"}
```

### Extract Pitch (Single)
```
POST /api/pitch
Body: multipart/form-data with "audio" file
Response: {pitch_contour, note_events, metadata}
```

### Extract Pitch (Batch)
```
POST /api/pitch/batch
Body: multipart/form-data with multiple "audio" files
Response: {results: [...]}
```

### Service Info
```
GET /api/info
Response: {service, version, endpoints}
```

---

## ✨ Features

✅ Extract pitch from audio files
✅ Support for WAV, MP3, FLAC, OGG, M4A
✅ Get MIDI data and note events
✅ Batch processing capability
✅ Production-ready error handling
✅ CORS support
✅ Type-safe TypeScript integration

---

## 🎯 Next Steps

1. **Deploy to Railway** (10-15 min)
   - Create Railway account
   - Deploy service
   - Get service URL

2. **Configure Lovable** (10-15 min)
   - Set environment variables
   - Deploy edge function
   - Set edge function environment variables

3. **Test Integration** (5 min)
   - Test health endpoint
   - Test pitch extraction
   - Test Lovable UI

4. **Deploy Lovable** (5-10 min)
   - Deploy to production
   - Monitor logs

**Total: 30-45 minutes**

---

## 💡 Tips

- Keep your Railway service URL handy
- Test health endpoint first
- Check logs if something fails
- Use Postman for API testing
- Monitor Railway dashboard for performance

---

## 📞 Support

For issues, check:
1. `RAILWAY_DEPLOYMENT_GUIDE.md` - Railway-specific help
2. `LOVABLE_INTEGRATION_GUIDE.md` - Lovable-specific help
3. `API_TESTING_GUIDE.md` - API testing help
4. Railway logs - Service errors
5. Supabase logs - Edge function errors

