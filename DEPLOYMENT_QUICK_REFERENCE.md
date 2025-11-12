# Deployment Quick Reference

## 🚀 Complete Setup in 30 Minutes

### Phase 1: Repository (Already Done ✅)
- ✅ Basic Pitch API (`basic-pitch-service/app.py`)
- ✅ Docker configuration (`Dockerfile`)
- ✅ Requirements (`requirements.txt`)
- ✅ Supabase edge function (`lovable-app/supabase/functions/extract-pitch/index.ts`)
- ✅ React hook (`lovable-app/src/hooks/usePitchExtraction.ts`)
- ✅ Repository pushed to GitHub

### Phase 2: Railway Deployment (5-10 minutes)

**Step 1:** Go to https://railway.app

**Step 2:** Click "New Project" → "Deploy from GitHub"

**Step 3:** Select `AI-Videoke-Maker` repository

**Step 4:** Railway auto-detects Dockerfile in `basic-pitch-service/`

**Step 5:** Click "Deploy"

**Step 6:** Wait for deployment (2-5 minutes)

**Step 7:** Copy your public URL from Railway dashboard
```
Example: https://ai-videoke-maker-production.up.railway.app
```

**Step 8:** Test health endpoint
```bash
curl https://your-service.railway.app/health
# Expected: {"status": "healthy", "service": "basic-pitch"}
```

### Phase 3: Lovable Configuration (5-10 minutes)

**Step 1:** Update `.env.local` in Lovable app:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_BASIC_PITCH_API_URL=https://your-railway-service.railway.app
```

**Step 2:** Deploy Supabase edge function:
```bash
supabase functions deploy extract-pitch --project-id your-project-id
```

**Step 3:** Set edge function environment variable:
- Go to Supabase dashboard
- Edge Functions → extract-pitch → Settings
- Add: `BASIC_PITCH_SERVICE_URL` = `https://your-railway-service.railway.app`

**Step 4:** Test in Lovable app:
```typescript
import { usePitchExtraction } from "@/hooks/usePitchExtraction";

const { extractPitch, loading, result } = usePitchExtraction();
await extractPitch(audioFile);
```

## 📋 Checklist

### Before Deployment
- [ ] Repository pushed to GitHub
- [ ] All files in place:
  - [ ] `basic-pitch-service/app.py`
  - [ ] `basic-pitch-service/requirements.txt`
  - [ ] `basic-pitch-service/Dockerfile`
  - [ ] `lovable-app/supabase/functions/extract-pitch/index.ts`
  - [ ] `lovable-app/src/hooks/usePitchExtraction.ts`

### Railway Deployment
- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] Service deployed successfully
- [ ] Health endpoint returns 200
- [ ] Public URL copied

### Lovable Integration
- [ ] Supabase project created
- [ ] Environment variables set
- [ ] Edge function deployed
- [ ] Edge function environment variables set
- [ ] React hook imported in components
- [ ] Audio upload tested

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| GitHub | https://github.com/abs0914/AI-Videoke-Maker |
| Railway | https://railway.app |
| Supabase | https://supabase.com |
| Lovable | https://lovable.dev |

## 📞 Support Resources

### Documentation
- [`RAILWAY_DEPLOYMENT_GUIDE.md`](./RAILWAY_DEPLOYMENT_GUIDE.md) - Detailed Railway setup
- [`LOVABLE_INTEGRATION_GUIDE.md`](./LOVABLE_INTEGRATION_GUIDE.md) - Detailed Lovable setup
- [`SETUP_SUMMARY.md`](./SETUP_SUMMARY.md) - Complete overview
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) - System design

### API Endpoints

**Health Check:**
```
GET /health
Response: {"status": "healthy", "service": "basic-pitch"}
```

**Extract Pitch (Single File):**
```
POST /api/pitch
Content-Type: multipart/form-data
Body: audio file

Response: {
  "success": true,
  "metadata": {...},
  "pitch_contour": {...},
  "note_events": [...]
}
```

**Extract Pitch (Batch):**
```
POST /api/pitch/batch
Content-Type: multipart/form-data
Body: multiple audio files

Response: {
  "results": [...]
}
```

**Service Info:**
```
GET /api/info
Response: {
  "service": "Basic Pitch Service",
  "version": "1.0.0",
  "endpoints": {...}
}
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Build fails on Railway | Check `requirements.txt` is in `basic-pitch-service/` |
| Service won't start | Verify port 8080 is exposed in Dockerfile |
| Health check fails | Ensure service is fully deployed, check logs |
| Edge function 405 | Use POST method, check CORS headers |
| "No audio file" error | Verify file sent in FormData with key "audio" |
| Timeout errors | Check file size < 50MB, increase timeout if needed |

## 📊 Performance

- **Typical processing time**: 2-10 seconds per audio file
- **Max file size**: 50MB
- **Supported formats**: WAV, MP3, FLAC, OGG, M4A
- **Sample rate**: Auto-converted to 22,050 Hz

## 💰 Costs

- **Railway**: $5/month free tier, then $0.000463/hour per GB RAM
- **Supabase**: Free tier includes edge functions
- **Lovable**: Depends on your plan

## 🎯 Next Steps

1. Deploy to Railway (5-10 min)
2. Configure Lovable app (5-10 min)
3. Test integration (5 min)
4. Deploy Lovable app (5-10 min)
5. Monitor and scale as needed

**Total time: 25-45 minutes**

