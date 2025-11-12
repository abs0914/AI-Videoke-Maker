# Basic Pitch Service

A Flask-based REST API service for extracting pitch and note information from audio files using Spotify's Basic Pitch model.

## Features

- Extract pitch contour from audio files
- Extract MIDI data and note events
- Support for multiple audio formats (WAV, MP3, FLAC, OGG, M4A)
- Batch processing of multiple audio files
- CORS enabled for cross-origin requests
- Health check endpoint
- Deployed on Railway

## Installation

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Run the service:
   ```bash
   python app.py
   ```

The service will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns service status.

### Extract Pitch (Single File)
```
POST /api/pitch
Content-Type: multipart/form-data

Body:
- audio: [audio file]
```

Response:
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

### Extract Pitch (Batch)
```
POST /api/pitch/batch
Content-Type: multipart/form-data

Body:
- audio: [audio file 1]
- audio: [audio file 2]
- ...
```

### Service Info
```
GET /api/info
```
Returns service information and available endpoints.

## Deployment to Railway

### Prerequisites
- Railway account connected to GitHub
- This repository pushed to GitHub

### Steps

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select this repository

2. **Configure Environment:**
   - In Railway dashboard, go to Variables
   - Add `PORT=5000` (Railway will assign a port automatically)
   - Add `FLASK_ENV=production`

3. **Deploy:**
   - Railway will automatically detect the Dockerfile and deploy
   - Once deployed, you'll get a public URL like `https://your-service.railway.app`

4. **Get Your Service URL:**
   - Copy the public URL from Railway dashboard
   - Use this URL in your Lovable app edge function

## Usage in Lovable App

Update your edge function to call this service:

```typescript
const BASIC_PITCH_SERVICE_URL = 'https://your-service.railway.app';

export async function extractPitch(audioFile: File) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await fetch(`${BASIC_PITCH_SERVICE_URL}/api/pitch`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}
```

## Troubleshooting

### Service not starting
- Check logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### Audio processing errors
- Ensure audio file is in supported format
- Check file size (max 50MB)
- Verify audio file is not corrupted

### CORS errors
- CORS is enabled for all origins in this service
- If issues persist, check browser console for specific errors

## Performance Notes

- First request may take longer as model loads
- Processing time depends on audio length
- Typical processing: ~1-2 seconds per minute of audio
- Consider implementing request queuing for high volume

## License

This service uses Spotify's Basic Pitch model. See their documentation for licensing details.

