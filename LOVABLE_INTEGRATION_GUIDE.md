# Lovable Integration Guide

## Overview

The Lovable app integrates with the Basic Pitch service through:
1. **Supabase Edge Function** - Proxy that forwards requests to the Python API
2. **React Hook** - `usePitchExtraction` for easy integration in components

## Architecture

```
Lovable App (React)
    ↓
usePitchExtraction Hook
    ↓
Supabase Edge Function (/functions/extract-pitch)
    ↓
Basic Pitch Service (Railway)
    ↓
Returns: Pitch data, MIDI, note events
```

## Step 1: Configure Environment Variables

### 1.1 In Lovable App

Create or update `.env.local`:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_BASIC_PITCH_API_URL=https://your-service.railway.app
```

Get these values from:
- **Supabase URL & Key**: Supabase dashboard → Settings → API
- **Basic Pitch API URL**: Railway dashboard (your deployed service URL)

### 1.2 In Supabase Edge Function

The edge function reads the API URL from environment variables:

```typescript
const BASIC_PITCH_SERVICE_URL = Deno.env.get("BASIC_PITCH_SERVICE_URL") || 
  "https://basic-pitch-service.railway.app";
```

Set this in Supabase:
1. Go to Supabase dashboard
2. Navigate to **Edge Functions** → **extract-pitch**
3. Click **Settings**
4. Add environment variable:
   - Key: `BASIC_PITCH_SERVICE_URL`
   - Value: `https://your-railway-service.railway.app`

## Step 2: Deploy Edge Function

### 2.1 Using Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login

# Deploy the edge function
supabase functions deploy extract-pitch --project-id your-project-id
```

### 2.2 Manual Deployment

1. Go to Supabase dashboard
2. Navigate to **Edge Functions**
3. Create new function: `extract-pitch`
4. Copy content from `lovable-app/supabase/functions/extract-pitch/index.ts`
5. Deploy

## Step 3: Use in React Components

### 3.1 Basic Usage

```typescript
import { usePitchExtraction } from "@/hooks/usePitchExtraction";

export function AudioUploader() {
  const { extractPitch, loading, error, result } = usePitchExtraction();

  const handleFileUpload = async (file: File) => {
    const pitchData = await extractPitch(file);
    if (pitchData) {
      console.log("Pitch extracted:", pitchData);
    }
  };

  return (
    <div>
      <input 
        type="file" 
        accept="audio/*"
        onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
        disabled={loading}
      />
      {loading && <p>Processing...</p>}
      {error && <p>Error: {error}</p>}
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

### 3.2 Advanced Usage

```typescript
// Access pitch contour data
const { pitch_contour, note_events } = result;

// Pitch contour
pitch_contour.times;        // Array of timestamps
pitch_contour.frequencies;  // Array of frequencies (Hz)
pitch_contour.confidence;   // Array of confidence scores (0-1)

// Note events
note_events.forEach(note => {
  console.log(`Note: ${note.pitch_midi}, Start: ${note.start_time}s, End: ${note.end_time}s`);
});
```

## Step 4: Test the Integration

### 4.1 Local Testing

```bash
# Start Lovable dev server
npm run dev

# Upload an audio file through the UI
# Check browser console for results
```

### 4.2 Check Logs

**Supabase Edge Function Logs:**
1. Go to Supabase dashboard
2. Navigate to **Edge Functions** → **extract-pitch**
3. Click **Logs** tab

**Basic Pitch Service Logs:**
1. Go to Railway dashboard
2. Select your service
3. Click **Logs** tab

## Supported Audio Formats

- WAV
- MP3
- FLAC
- OGG
- M4A

Maximum file size: **50MB**

## API Response Format

```json
{
  "success": true,
  "metadata": {
    "sample_rate": 22050,
    "duration_seconds": 5.5,
    "filename": "audio.wav"
  },
  "pitch_contour": {
    "times": [0, 0.01, 0.02, ...],
    "frequencies": [0, 440, 442, ...],
    "confidence": [0, 0.95, 0.92, ...]
  },
  "note_events": [
    {
      "start_time": 0.1,
      "end_time": 0.5,
      "pitch_midi": 69,
      "velocity": 100
    }
  ],
  "midi_data": [...]
}
```

## Troubleshooting

### Edge Function Returns 405
- Ensure you're using POST method
- Check CORS headers are correct

### "No audio file provided"
- Verify file is being sent in FormData with key "audio"
- Check file is not empty

### Service Returns 500
- Check Railway service is running
- Verify API URL is correct
- Check service logs for errors

### Timeout Errors
- Audio file may be too large
- Service may be processing
- Increase timeout in edge function if needed

## Performance Tips

1. **Compress audio** before uploading
2. **Use appropriate sample rate** (22050 Hz is optimal)
3. **Batch processing** for multiple files
4. **Cache results** to avoid reprocessing

## Next Steps

1. Test with sample audio files
2. Integrate pitch visualization
3. Add MIDI export functionality
4. Implement batch processing UI

