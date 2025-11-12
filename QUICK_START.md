# Quick Start: Basic Pitch Service Deployment

## TL;DR - 5 Minute Setup

### 1. Deploy to Railway (2 minutes)
```bash
# Push code to GitHub
git add .
git commit -m "Add Basic Pitch service"
git push origin main
```

Then in Railway dashboard:
- New Project → Deploy from GitHub
- Select `AI-Videoke-Maker` repo
- Set root directory to `basic-pitch-service`
- Wait for deployment
- Copy the public URL (e.g., `https://basic-pitch-service-prod.railway.app`)

### 2. Configure Lovable App (2 minutes)
In your Supabase project:
- Go to Edge Functions settings
- Add environment variable:
  - `BASIC_PITCH_SERVICE_URL` = `https://your-service-url.railway.app`
- Deploy edge function: `supabase functions deploy extract-pitch`

### 3. Use in Your App (1 minute)
```typescript
import { usePitchExtraction } from "@/hooks/usePitchExtraction";

const { extractPitch, loading, result } = usePitchExtraction();

// Upload audio file
const pitchData = await extractPitch(audioFile);
```

## What Was Created

### Backend Service (`basic-pitch-service/`)
- **app.py** - Flask API with pitch extraction endpoints
- **Dockerfile** - Container configuration for Railway
- **requirements.txt** - Python dependencies
- **Procfile** - Process configuration
- **railway.json** - Railway deployment config

### Lovable Integration (`lovable-app/`)
- **supabase/functions/extract-pitch/index.ts** - Edge function that calls the service
- **src/hooks/usePitchExtraction.ts** - React hook for easy integration

## API Endpoints

### Single File
```bash
POST /api/pitch
Content-Type: multipart/form-data
Body: audio=[file]
```

### Batch Processing
```bash
POST /api/pitch/batch
Content-Type: multipart/form-data
Body: audio=[file1], audio=[file2], ...
```

### Health Check
```bash
GET /health
```

## Response Example
```json
{
  "success": true,
  "metadata": {
    "sample_rate": 22050,
    "duration_seconds": 10.5,
    "filename": "audio.wav"
  },
  "pitch_contour": {
    "times": [0.0, 0.032, ...],
    "frequencies": [0.0, 440.2, ...],
    "confidence": [0.0, 0.95, ...]
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

## Testing Locally

```bash
# Install dependencies
cd basic-pitch-service
pip install -r requirements.txt

# Run service
python app.py

# Test in another terminal
curl -X POST http://localhost:5000/api/pitch \
  -F "audio=@test-audio.wav"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Service won't start | Check Railway logs, ensure Python 3.11+ |
| Timeout errors | Increase Railway timeout to 120s |
| CORS errors | CORS is enabled, check browser console |
| Audio errors | Verify format (WAV, MP3, FLAC, OGG, M4A) |

## Next Steps

1. ✅ Deploy service to Railway
2. ✅ Configure edge function
3. Build UI for audio upload
4. Add pitch visualization
5. Integrate with karaoke features

## Full Documentation

See `DEPLOYMENT_GUIDE.md` for detailed setup and troubleshooting.

