# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lovable App (Frontend)                    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  React Component                                         │   │
│  │  - Audio Upload UI                                       │   │
│  │  - usePitchExtraction Hook                              │   │
│  │  - Pitch Visualization                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Supabase Client                                         │   │
│  │  - Authentication                                        │   │
│  │  - API calls                                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    HTTPS Request (FormData)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase Edge Functions                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  extract-pitch Function (Deno)                           │   │
│  │  - Validates request                                     │   │
│  │  - Handles CORS                                          │   │
│  │  - Forwards to Basic Pitch Service                       │   │
│  │  - Returns response to frontend                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    HTTPS Request (FormData)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Basic Pitch Service (Railway)                    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Flask Application (Python)                              │   │
│  │                                                           │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Endpoints:                                        │  │   │
│  │  │  - GET /health                                     │  │   │
│  │  │  - POST /api/pitch                                 │  │   │
│  │  │  - POST /api/pitch/batch                           │  │   │
│  │  │  - GET /api/info                                   │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                      ↓                                    │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Audio Processing Pipeline:                        │  │   │
│  │  │  1. Receive audio file                             │  │   │
│  │  │  2. Validate format & size                         │  │   │
│  │  │  3. Load with librosa                              │  │   │
│  │  │  4. Extract pitch with Basic Pitch model           │  │   │
│  │  │  5. Return results (pitch, MIDI, notes)            │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Dependencies:                                           │   │
│  │  - Flask (Web framework)                                 │   │
│  │  - basic-pitch (Spotify's model)                         │   │
│  │  - librosa (Audio processing)                            │   │
│  │  - gunicorn (Production server)                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Uploads Audio File

```
User selects audio file
        ↓
React component receives file
        ↓
usePitchExtraction hook called
        ↓
FormData created with audio file
        ↓
Request sent to Supabase edge function
```

### 2. Edge Function Processes Request

```
Edge function receives request
        ↓
Validates request (CORS, method, file)
        ↓
Extracts audio file from FormData
        ↓
Creates new FormData with audio
        ↓
Forwards to Basic Pitch Service
        ↓
Waits for response
        ↓
Returns response to frontend
```

### 3. Basic Pitch Service Processes Audio

```
Service receives audio file
        ↓
Validates file format & size
        ↓
Loads audio with librosa
        ↓
Runs Basic Pitch model
        ↓
Extracts:
  - Pitch contour (times, frequencies, confidence)
  - MIDI data
  - Note events (start, end, pitch, velocity)
        ↓
Returns JSON response
```

### 4. Frontend Receives Results

```
Edge function returns response
        ↓
usePitchExtraction hook updates state
        ↓
Component receives result
        ↓
Display pitch data to user
```

---

## API Response Structure

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

---

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    Lovable App                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AudioUploader Component                             │  │
│  │  - File input                                        │  │
│  │  - Upload button                                     │  │
│  │  - Loading indicator                                │  │
│  │  - Error display                                    │  │
│  │  - Results display                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│           ↓                                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  usePitchExtraction Hook                             │  │
│  │  - State: loading, error, result                     │  │
│  │  - Function: extractPitch(file)                      │  │
│  │  - Calls: Supabase edge function                     │  │
│  └──────────────────────────────────────────────────────┘  │
│           ↓                                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Supabase Client                                     │  │
│  │  - Handles authentication                            │  │
│  │  - Makes HTTP requests                               │  │
│  │  - Manages session                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Repository                       │
│                                                             │
│  ├── basic-pitch-service/                                  │
│  │   ├── app.py                                            │
│  │   ├── requirements.txt                                  │
│  │   ├── Dockerfile                                        │
│  │   └── ...                                               │
│  │                                                         │
│  └── lovable-app/                                          │
│      ├── supabase/functions/extract-pitch/                │
│      ├── src/hooks/usePitchExtraction.ts                  │
│      └── ...                                               │
└─────────────────────────────────────────────────────────────┘
         ↓                                    ↓
    ┌─────────────┐              ┌──────────────────────┐
    │   Railway   │              │  Supabase Project    │
    │             │              │                      │
    │ Basic Pitch │              │  Edge Functions      │
    │  Service    │              │  - extract-pitch     │
    │             │              │                      │
    │ Running on  │              │  Database            │
    │ Docker      │              │  Auth                │
    └─────────────┘              └──────────────────────┘
         ↑                                    ↑
         └────────────────────┬───────────────┘
                              │
                    ┌─────────────────┐
                    │  Lovable App    │
                    │  (Frontend)     │
                    │                 │
                    │  React + Vite   │
                    └─────────────────┘
```

---

## Error Handling Flow

```
Request received
        ↓
    ┌───────────────────────────────────────┐
    │  Validation Checks                    │
    │  - File exists?                       │
    │  - File format valid?                 │
    │  - File size OK?                      │
    └───────────────────────────────────────┘
        ↓                           ↓
    Valid                       Invalid
        ↓                           ↓
    Process                    Return Error
        ↓                           ↓
    ┌───────────────────────────────────────┐
    │  Processing                           │
    │  - Load audio                         │
    │  - Extract pitch                      │
    │  - Generate response                  │
    └───────────────────────────────────────┘
        ↓                           ↓
    Success                     Error
        ↓                           ↓
    Return Results              Return Error
        ↓                           ↓
    Frontend displays           Frontend shows
    pitch data                  error message
```

---

## Performance Considerations

### Cold Start (First Request)
```
Request arrives
        ↓
Load Flask app (~0.5s)
        ↓
Load Basic Pitch model (~2-3s)
        ↓
Process audio (~1-2s per minute)
        ↓
Return results
        ↓
Total: ~3-5 seconds
```

### Warm Start (Subsequent Requests)
```
Request arrives
        ↓
Model already loaded
        ↓
Process audio (~1-2s per minute)
        ↓
Return results
        ↓
Total: ~1-2 seconds
```

### Optimization Strategies
1. **Caching:** Cache results by audio file hash
2. **Batch Processing:** Process multiple files in one request
3. **Warming:** Periodic health checks to keep service warm
4. **Scaling:** Increase Railway replicas for high load

---

## Security Considerations

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
│                                                             │
│  1. CORS Headers                                            │
│     - Restrict cross-origin requests                        │
│     - Validate origin                                       │
│                                                             │
│  2. Input Validation                                        │
│     - File format validation                                │
│     - File size limits (50MB)                               │
│     - Filename validation                                   │
│                                                             │
│  3. Authentication                                          │
│     - Supabase auth token required                          │
│     - Edge function validates token                         │
│                                                             │
│  4. Error Handling                                          │
│     - No sensitive info in errors                           │
│     - Proper HTTP status codes                              │
│     - Logging for debugging                                 │
│                                                             │
│  5. Rate Limiting                                           │
│     - Consider implementing in future                       │
│     - Prevent abuse                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Scaling Strategy

### Current Setup
- Single Railway instance
- Single Supabase project
- Suitable for: Development, testing, small production

### Scaling Options
1. **Horizontal Scaling (Railway)**
   - Increase replicas
   - Load balancing
   - Auto-scaling based on CPU/memory

2. **Caching Layer**
   - Redis for result caching
   - Reduce redundant processing

3. **Queue System**
   - Bull/RabbitMQ for job queuing
   - Handle burst traffic

4. **Database**
   - Store processed results
   - Track usage metrics

---

## Monitoring & Observability

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Stack                         │
│                                                             │
│  Railway Dashboard                                          │
│  - CPU usage                                                │
│  - Memory usage                                             │
│  - Network I/O                                              │
│  - Deployment logs                                          │
│                                                             │
│  Supabase Dashboard                                         │
│  - Function invocations                                     │
│  - Error rates                                              │
│  - Response times                                           │
│  - Function logs                                            │
│                                                             │
│  Browser Console                                            │
│  - Frontend errors                                          │
│  - Network requests                                         │
│  - Performance metrics                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Future Enhancements

1. **Real-time Processing**
   - WebSocket support for streaming audio
   - Live pitch visualization

2. **Advanced Features**
   - Vibrato detection
   - Formant analysis
   - Polyphonic pitch detection

3. **Integration**
   - Karaoke scoring
   - Pitch correction
   - Music generation

4. **Performance**
   - GPU acceleration
   - Model optimization
   - Caching strategies

5. **Analytics**
   - Usage tracking
   - Performance metrics
   - Error monitoring

