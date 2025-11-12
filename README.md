# AI Videoke Maker - Basic Pitch Service

A complete, production-ready solution for deploying Spotify's Basic Pitch model as a microservice on Railway and integrating it with your Lovable app.

## 🚀 Quick Start

**New here?** Start with one of these:

1. **5-minute overview:** Read [`QUICK_START.md`](./QUICK_START.md)
2. **Complete guide:** Read [`SETUP_SUMMARY.md`](./SETUP_SUMMARY.md)
3. **Step-by-step:** Follow [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md)
4. **During deployment:** Use [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md)

## 📋 What's Included

### Backend Service
- ✅ Flask REST API for pitch extraction
- ✅ Docker configuration for Railway
- ✅ Support for multiple audio formats
- ✅ Batch processing capability
- ✅ Production-ready with error handling

### Frontend Integration
- ✅ Supabase edge function (proxy)
- ✅ React hook for easy integration
- ✅ Type-safe TypeScript code
- ✅ CORS support

### Documentation
- ✅ Complete deployment guide
- ✅ Architecture overview
- ✅ API documentation
- ✅ Troubleshooting guide
- ✅ Deployment checklist

## 📁 Project Structure

```
AI-Videoke-Maker/
├── README.md                    ← You are here
├── SETUP_SUMMARY.md            ← Start here!
├── QUICK_START.md              ← Quick reference
├── DEPLOYMENT_GUIDE.md         ← Detailed guide
├── DEPLOYMENT_CHECKLIST.md     ← Deployment tasks
├── ARCHITECTURE.md             ← System design
├── FILES_CREATED.md            ← File descriptions
│
├── basic-pitch-service/        ← Python service
│   ├── app.py                  ← Flask application
│   ├── requirements.txt        ← Dependencies
│   ├── Dockerfile              ← Container config
│   ├── Procfile                ← Process definition
│   ├── railway.json            ← Railway config
│   ├── .env.example            ← Environment template
│   ├── .gitignore              ← Git ignore rules
│   └── README.md               ← Service docs
│
└── lovable-app/                ← Lovable integration
    ├── .env.example            ← Environment template
    ├── supabase/
    │   └── functions/
    │       ├── extract-pitch/
    │       │   └── index.ts    ← Edge function
    │       └── _shared/
    │           └── cors.ts     ← CORS utility
    └── src/
        └── hooks/
            └── usePitchExtraction.ts ← React hook
```

## 🎯 Key Features

### Pitch Extraction
- Extract pitch contour from audio files
- Get MIDI data and note events
- Confidence scores for each pitch value
- Support for multiple audio formats

### Supported Formats
- WAV, MP3, FLAC, OGG, M4A
- Max file size: 50MB
- Sample rate: 22,050 Hz (auto-converted)

### API Endpoints
- `GET /health` - Health check
- `POST /api/pitch` - Single file processing
- `POST /api/pitch/batch` - Batch processing
- `GET /api/info` - Service information

## 🚀 Deployment

### 1. Deploy to Railway (5 minutes)
```bash
# Push to GitHub
git add .
git commit -m "Add Basic Pitch service"
git push origin main

# In Railway dashboard:
# - New Project → Deploy from GitHub
# - Select AI-Videoke-Maker repo
# - Set root directory to basic-pitch-service
# - Wait for deployment
# - Copy the public URL
```

### 2. Configure Lovable App (3 minutes)
```bash
# In Supabase project:
# - Add environment variable: BASIC_PITCH_SERVICE_URL
# - Deploy edge function: supabase functions deploy extract-pitch
```

### 3. Use in Your App (2 minutes)
```typescript
import { usePitchExtraction } from "@/hooks/usePitchExtraction";

const { extractPitch, loading, result } = usePitchExtraction();
const pitchData = await extractPitch(audioFile);
```

## 📊 API Response Example

```json
{
  "success": true,
  "metadata": {
    "sample_rate": 22050,
    "duration_seconds": 10.5,
    "filename": "audio.wav"
  },
  "pitch_contour": {
    "times": [0.0, 0.032, 0.064, ...],
    "frequencies": [0.0, 440.2, 442.1, ...],
    "confidence": [0.0, 0.95, 0.98, ...]
  },
  "note_events": [
    {
      "start_time": 0.5,
      "end_time": 1.2,
      "pitch_midi": 69,
      "velocity": 100
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

**Basic Pitch Service (Railway):**
```
PORT=5000
FLASK_ENV=production
```

**Lovable App (Supabase):**
```
BASIC_PITCH_SERVICE_URL=https://your-service.railway.app
```

**Lovable App (Frontend):**
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

## 📈 Performance

- **Cold Start:** 3-5 seconds (first request, model loading)
- **Warm Start:** 1-2 seconds (subsequent requests)
- **Processing:** ~1-2 seconds per minute of audio
- **Max File Size:** 50MB

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Service won't start | Check Railway logs, ensure Python 3.11+ |
| Timeout errors | Increase Railway timeout to 120+ seconds |
| CORS errors | CORS is enabled, check browser console |
| Audio errors | Verify format (WAV, MP3, FLAC, OGG, M4A) |

See [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

## 📚 Documentation

- **[SETUP_SUMMARY.md](./SETUP_SUMMARY.md)** - Complete overview and deployment steps
- **[QUICK_START.md](./QUICK_START.md)** - 5-minute quick reference
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Detailed step-by-step guide
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Deployment checklist
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture and design
- **[FILES_CREATED.md](./FILES_CREATED.md)** - Description of all files

## 🔗 Resources

- **Basic Pitch:** https://github.com/spotify/basic-pitch
- **Railway:** https://railway.app
- **Supabase:** https://supabase.com
- **Flask:** https://flask.palletsprojects.com

## 📝 Next Steps

1. ✅ Read [`SETUP_SUMMARY.md`](./SETUP_SUMMARY.md)
2. ✅ Follow [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md)
3. Deploy to Railway
4. Configure Lovable app
5. Test integration
6. Build UI components
7. Add pitch visualization

## 💡 Tips

- **First request slow?** That's normal - the model loads on first request
- **Want to speed up?** Implement periodic health checks to keep service warm
- **Need batch processing?** Use the `/api/pitch/batch` endpoint
- **Want to cache results?** Store pitch data by audio file hash

## 🎓 Learning Resources

- [Spotify Basic Pitch Documentation](https://github.com/spotify/basic-pitch)
- [Railway Deployment Guide](https://docs.railway.app)
- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Flask Web Development](https://flask.palletsprojects.com)

## ✨ Features

- ✅ Production-ready Flask service
- ✅ Docker containerization
- ✅ Railway deployment
- ✅ Supabase integration
- ✅ React hook for easy integration
- ✅ Type-safe TypeScript
- ✅ CORS support
- ✅ Error handling
- ✅ Batch processing
- ✅ Comprehensive documentation

## 🤝 Support

For issues or questions:
1. Check [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md) troubleshooting section
2. Review [`ARCHITECTURE.md`](./ARCHITECTURE.md) for system design
3. Check service logs in Railway dashboard
4. Check function logs in Supabase dashboard

## 📄 License

This project uses Spotify's Basic Pitch model. See their repository for licensing details.

---

**Status:** ✅ Ready for deployment

**Last Updated:** 2025-11-12

**Version:** 1.0.0

