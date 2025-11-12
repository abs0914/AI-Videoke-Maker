# API Testing Guide

## Prerequisites

- Deployed service URL (from Railway)
- `curl` or Postman installed
- Sample audio file (WAV, MP3, FLAC, OGG, or M4A)

## Test 1: Health Check

**Purpose:** Verify the service is running

**Command:**
```bash
curl https://your-service.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "basic-pitch"
}
```

**Status Code:** 200

---

## Test 2: Service Info

**Purpose:** Get service information and available endpoints

**Command:**
```bash
curl https://your-service.railway.app/api/info
```

**Expected Response:**
```json
{
  "service": "Basic Pitch Service",
  "version": "1.0.0",
  "endpoints": {
    "/health": "Health check",
    "/api/pitch": "Extract pitch from single audio file",
    "/api/pitch/batch": "Extract pitch from multiple audio files",
    "/api/info": "Service information"
  }
}
```

**Status Code:** 200

---

## Test 3: Extract Pitch (Single File)

**Purpose:** Extract pitch from a single audio file

**Command:**
```bash
curl -X POST \
  -F "audio=@/path/to/audio.wav" \
  https://your-service.railway.app/api/pitch
```

**Expected Response:**
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
  "midi_data": [...],
  "note_events": [
    {
      "start_time": 0.1,
      "end_time": 0.5,
      "pitch_midi": 69,
      "velocity": 100
    }
  ]
}
```

**Status Code:** 200

---

## Test 4: Extract Pitch (Batch)

**Purpose:** Extract pitch from multiple audio files

**Command:**
```bash
curl -X POST \
  -F "audio=@/path/to/audio1.wav" \
  -F "audio=@/path/to/audio2.wav" \
  https://your-service.railway.app/api/pitch/batch
```

**Expected Response:**
```json
{
  "results": [
    {
      "filename": "audio1.wav",
      "success": true,
      "metadata": {...},
      "pitch_contour": {...},
      "note_events": [...]
    },
    {
      "filename": "audio2.wav",
      "success": true,
      "metadata": {...},
      "pitch_contour": {...},
      "note_events": [...]
    }
  ]
}
```

**Status Code:** 200

---

## Test 5: Error Handling

### 5.1 Missing File

**Command:**
```bash
curl -X POST https://your-service.railway.app/api/pitch
```

**Expected Response:**
```json
{
  "error": "No audio file provided"
}
```

**Status Code:** 400

### 5.2 Invalid File Type

**Command:**
```bash
curl -X POST \
  -F "audio=@/path/to/file.txt" \
  https://your-service.railway.app/api/pitch
```

**Expected Response:**
```json
{
  "error": "File type not allowed. Allowed types: wav, mp3, flac, ogg, m4a"
}
```

**Status Code:** 400

### 5.3 File Too Large

**Command:**
```bash
# Create a file larger than 50MB
curl -X POST \
  -F "audio=@/path/to/large-file.wav" \
  https://your-service.railway.app/api/pitch
```

**Expected Response:**
```json
{
  "error": "File too large. Maximum size: 50.0MB"
}
```

**Status Code:** 400

### 5.4 Invalid Endpoint

**Command:**
```bash
curl https://your-service.railway.app/invalid
```

**Expected Response:**
```json
{
  "error": "Endpoint not found"
}
```

**Status Code:** 404

---

## Test 6: Using Postman

### 6.1 Create Request

1. Open Postman
2. Create new POST request
3. URL: `https://your-service.railway.app/api/pitch`
4. Go to **Body** tab
5. Select **form-data**
6. Add key: `audio`, type: **File**
7. Select your audio file
8. Click **Send**

### 6.2 View Response

- Response body shows JSON with pitch data
- Status code should be 200
- Check **Headers** tab for response headers

---

## Test 7: Using Python

```python
import requests

# Test health check
response = requests.get('https://your-service.railway.app/health')
print(response.json())

# Test pitch extraction
with open('audio.wav', 'rb') as f:
    files = {'audio': f}
    response = requests.post(
        'https://your-service.railway.app/api/pitch',
        files=files
    )
    print(response.json())
```

---

## Test 8: Using JavaScript/Node.js

```javascript
// Test health check
fetch('https://your-service.railway.app/health')
  .then(r => r.json())
  .then(data => console.log(data));

// Test pitch extraction
const formData = new FormData();
formData.append('audio', audioFile);

fetch('https://your-service.railway.app/api/pitch', {
  method: 'POST',
  body: formData
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## Performance Benchmarks

| Test | Expected Time | Notes |
|------|----------------|-------|
| Health check | < 100ms | Simple endpoint |
| Service info | < 100ms | Simple endpoint |
| Pitch extraction (5s audio) | 2-5 seconds | Depends on CPU |
| Pitch extraction (30s audio) | 5-15 seconds | Longer processing |
| Batch (2 files) | 5-10 seconds | Sequential processing |

---

## Troubleshooting

### Connection Refused
- Service may not be deployed
- Check Railway dashboard
- Verify URL is correct

### 500 Internal Server Error
- Check service logs in Railway
- Verify audio file is valid
- Check system resources

### Timeout
- Audio file may be too large
- Service may be overloaded
- Increase timeout value

### CORS Errors
- CORS is enabled in Flask app
- Check browser console for details
- Verify origin is allowed

---

## Next Steps

1. ✅ Test health endpoint
2. ✅ Test service info
3. ✅ Test pitch extraction
4. ✅ Test error handling
5. Configure Lovable app
6. Test Lovable integration
7. Deploy Lovable app

