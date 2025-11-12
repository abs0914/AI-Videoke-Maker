# Deployment Checklist

## Pre-Deployment

- [ ] All code committed to GitHub
- [ ] Railway account connected to GitHub
- [ ] Supabase project created and configured
- [ ] Test audio files available for testing

## Step 1: Deploy Basic Pitch Service to Railway

### Preparation
- [ ] Push code to GitHub:
  ```bash
  git add .
  git commit -m "Add Basic Pitch service and Lovable integration"
  git push origin main
  ```

### Railway Deployment
- [ ] Go to https://railway.app
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Select `AI-Videoke-Maker` repository
- [ ] **Set root directory to `basic-pitch-service`**
- [ ] Wait for build to complete
- [ ] Verify deployment status shows "Running"
- [ ] Copy the public URL (e.g., `https://basic-pitch-service-prod.railway.app`)

### Verification
- [ ] Test health endpoint:
  ```bash
  curl https://your-service-url.railway.app/health
  ```
  Expected: `{"status": "healthy", "service": "basic-pitch"}`

- [ ] Test with sample audio:
  ```bash
  curl -X POST https://your-service-url.railway.app/api/pitch \
    -F "audio=@test-audio.wav"
  ```

## Step 2: Configure Lovable App

### Environment Variables
- [ ] Go to Supabase project dashboard
- [ ] Navigate to Edge Functions settings
- [ ] Add environment variable:
  - Key: `BASIC_PITCH_SERVICE_URL`
  - Value: `https://your-service-url.railway.app`

### Deploy Edge Function
- [ ] In terminal, run:
  ```bash
  supabase functions deploy extract-pitch
  ```
- [ ] Verify deployment succeeded

### Test Edge Function
- [ ] Get your Supabase URL and anon key
- [ ] Test with curl:
  ```bash
  curl -X POST https://your-project.supabase.co/functions/v1/extract-pitch \
    -H "Authorization: Bearer YOUR_ANON_KEY" \
    -F "audio=@test-audio.wav"
  ```

## Step 3: Integrate with Lovable App

### Frontend Setup
- [ ] Copy `.env.example` to `.env.local`
- [ ] Fill in Supabase credentials:
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`

### Component Integration
- [ ] Import `usePitchExtraction` hook in your component
- [ ] Implement audio upload UI
- [ ] Test pitch extraction in browser
- [ ] Verify response data is received correctly

### Testing
- [ ] [ ] Upload single audio file
- [ ] [ ] Verify pitch data is returned
- [ ] [ ] Check pitch contour visualization (if implemented)
- [ ] [ ] Test with different audio formats
- [ ] [ ] Test error handling (invalid file, too large, etc.)

## Step 4: Production Verification

### Service Health
- [ ] [ ] Check Railway dashboard for resource usage
- [ ] [ ] Verify no errors in Railway logs
- [ ] [ ] Test service with multiple concurrent requests
- [ ] [ ] Monitor response times

### Edge Function
- [ ] [ ] Check Supabase function logs
- [ ] [ ] Verify CORS headers are correct
- [ ] [ ] Test from different origins

### Frontend
- [ ] [ ] Test on different browsers
- [ ] [ ] Test on mobile devices
- [ ] [ ] Verify error messages display correctly
- [ ] [ ] Test loading states

## Step 5: Optimization & Monitoring

### Performance
- [ ] [ ] Implement request caching
- [ ] [ ] Add loading indicators
- [ ] [ ] Consider batch processing for multiple files
- [ ] [ ] Monitor cold start times

### Monitoring
- [ ] [ ] Set up Railway alerts
- [ ] [ ] Monitor Supabase function usage
- [ ] [ ] Track error rates
- [ ] [ ] Monitor response times

### Documentation
- [ ] [ ] Update README with deployment info
- [ ] [ ] Document API usage
- [ ] [ ] Create troubleshooting guide
- [ ] [ ] Document performance characteristics

## Troubleshooting Checklist

If deployment fails, check:

### Railway Issues
- [ ] Dockerfile is valid
- [ ] requirements.txt has all dependencies
- [ ] Python version is 3.11+
- [ ] Port is correctly set to 5000
- [ ] Check Railway logs for specific errors

### Edge Function Issues
- [ ] Function is deployed: `supabase functions list`
- [ ] Environment variable is set correctly
- [ ] CORS headers are included
- [ ] Check Supabase function logs

### Frontend Issues
- [ ] Environment variables are set
- [ ] Supabase credentials are correct
- [ ] Edge function URL is correct
- [ ] Check browser console for errors

## Rollback Plan

If something goes wrong:

1. **Service Down:**
   - [ ] Check Railway dashboard
   - [ ] Redeploy from Railway dashboard
   - [ ] Check logs for errors

2. **Edge Function Error:**
   - [ ] Redeploy: `supabase functions deploy extract-pitch`
   - [ ] Check environment variables
   - [ ] Verify service URL is correct

3. **Frontend Issues:**
   - [ ] Clear browser cache
   - [ ] Check environment variables
   - [ ] Restart development server

## Post-Deployment

- [ ] [ ] Document the deployed service URL
- [ ] [ ] Share deployment info with team
- [ ] [ ] Set up monitoring and alerts
- [ ] [ ] Plan for scaling if needed
- [ ] [ ] Schedule regular backups
- [ ] [ ] Document any custom configurations

## Success Criteria

✅ All items checked means:
- Basic Pitch service is running on Railway
- Edge function is deployed and working
- Lovable app can successfully extract pitch from audio
- All error cases are handled gracefully
- Performance is acceptable
- Monitoring is in place

---

**Deployment Date:** _______________

**Deployed By:** _______________

**Service URL:** _______________

**Notes:** 

