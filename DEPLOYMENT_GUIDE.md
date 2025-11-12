# Basic Pitch Service Deployment Guide

This guide walks you through deploying the Basic Pitch Python service to Railway and integrating it with your Lovable app.

## Architecture Overview

```
Lovable App (Frontend)
    ↓
Supabase Edge Function (extract-pitch)
    ↓
Basic Pitch Service (Railway)
    ↓
Audio Processing & Pitch Extraction
```

## Step 1: Deploy Basic Pitch Service to Railway

### Prerequisites
- Railway account (already connected to GitHub)
- This repository pushed to GitHub

### Deployment Steps

1. **Push the code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Basic Pitch service and Lovable integration"
   git push origin main
   ```

2. **In Railway Dashboard:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Search for and select `AI-Videoke-Maker` repository
   - Select the `basic-pitch-service` directory as the root directory

3. **Configure the Service:**
   - Railway will automatically detect the Dockerfile
   - In the Railway dashboard, go to the project settings
   - Set the following environment variables:
     - `PORT`: 5000 (or leave empty for Railway to assign)
     - `FLASK_ENV`: production

4. **Wait for Deployment:**
   - Railway will build and deploy the service
   - Once complete, you'll see a public URL (e.g., `https://basic-pitch-service-prod.railway.app`)
   - Copy this URL - you'll need it in the next step

### Verify Deployment

Test the service with:
```bash
curl https://your-service-url.railway.app/health
```

Expected response:
```json
{"status": "healthy", "service": "basic-pitch"}
```

## Step 2: Update Lovable App Edge Function

### Configure Environment Variable

1. **In your Lovable app's Supabase project:**
   - Go to Project Settings → Edge Functions
   - Add environment variable:
     - Key: `BASIC_PITCH_SERVICE_URL`
     - Value: `https://your-service-url.railway.app` (from Step 1)

2. **Deploy the edge function:**
   ```bash
   supabase functions deploy extract-pitch
   ```

### Test the Edge Function

```bash
curl -X POST https://your-project.supabase.co/functions/v1/extract-pitch \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -F "audio=@test-audio.wav"
```

## Step 3: Use in Your Lovable App

### Using the Hook

```typescript
import { usePitchExtraction } from "@/hooks/usePitchExtraction";

export function AudioUploader() {
  const { extractPitch, loading, error, result } = usePitchExtraction();

  const handleFileUpload = async (file: File) => {
    const pitchData = await extractPitch(file);
    if (pitchData) {
      console.log("Pitch extracted:", pitchData);
      // Use the pitch data in your app
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFileUpload(file);
        }}
        disabled={loading}
      />
      {loading && <p>Extracting pitch...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <div>
          <p>Duration: {result.metadata.duration_seconds}s</p>
          <p>Notes detected: {result.note_events.length}</p>
        </div>
      )}
    </div>
  );
}
```

### Direct API Call

```typescript
const response = await fetch(
  `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/extract-pitch`,
  {
    method: "POST",
    body: formData,
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
    },
  }
);

const pitchData = await response.json();
```

## API Response Format

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
  ],
  "midi_data": [...]
}
```

## Troubleshooting

### Service Not Starting on Railway
- Check Railway logs: Dashboard → Project → Deployments → View Logs
- Common issues:
  - Missing system dependencies (libsndfile1, ffmpeg)
  - Python version mismatch
  - Memory constraints (increase in Railway settings)

### Edge Function Timeout
- Basic Pitch model loading takes time on first request
- Increase timeout in Railway: Settings → Timeout (set to 120+ seconds)
- Consider warming up the service with periodic health checks

### CORS Errors
- CORS is enabled in the Flask service
- If issues persist, check browser console for specific errors
- Verify edge function is properly forwarding requests

### Audio Processing Errors
- Ensure audio file is in supported format (WAV, MP3, FLAC, OGG, M4A)
- Check file size (max 50MB)
- Verify audio file is not corrupted

## Performance Optimization

### Cold Start
- First request loads the model (~2-3 seconds)
- Subsequent requests are faster
- Consider implementing a warmup request on app startup

### Batch Processing
For multiple files, use the batch endpoint:
```typescript
const formData = new FormData();
formData.append("audio", file1);
formData.append("audio", file2);

const response = await fetch(
  `${BASIC_PITCH_SERVICE_URL}/api/pitch/batch`,
  {
    method: "POST",
    body: formData,
  }
);
```

### Caching
- Cache results by audio file hash to avoid reprocessing
- Store pitch data in Supabase for future reference

## Monitoring

### Railway Dashboard
- Monitor CPU, memory, and network usage
- Check deployment logs for errors
- Set up alerts for service failures

### Health Checks
Periodically call the health endpoint:
```bash
curl https://your-service-url.railway.app/health
```

## Scaling

If you need to handle more requests:
1. In Railway dashboard, increase number of replicas
2. Consider implementing request queuing
3. Add caching layer (Redis)
4. Optimize model loading with model caching

## Next Steps

1. ✅ Deploy Basic Pitch service to Railway
2. ✅ Configure edge function with service URL
3. ✅ Test the integration
4. Implement UI components for audio upload
5. Add pitch visualization
6. Integrate with karaoke/videoke features

## Support

For issues with:
- **Basic Pitch model**: See [Spotify Basic Pitch docs](https://github.com/spotify/basic-pitch)
- **Railway deployment**: See [Railway docs](https://docs.railway.app)
- **Supabase Edge Functions**: See [Supabase docs](https://supabase.com/docs/guides/functions)

