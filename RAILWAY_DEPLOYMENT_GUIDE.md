# Railway Deployment Guide

## Prerequisites

- GitHub account with the repository pushed
- Railway account (https://railway.app)
- Railway CLI installed (optional, but recommended)

## Step 1: Connect Railway to GitHub

1. Go to https://railway.app
2. Sign in with your GitHub account
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your GitHub repository: `AI-Videoke-Maker`
5. Railway will automatically detect the Dockerfile in `basic-pitch-service/`

## Step 2: Configure the Service

### 2.1 Select the Service Directory
- Railway should auto-detect the `basic-pitch-service` directory
- If not, specify the root directory as `basic-pitch-service/`

### 2.2 Set Environment Variables
In the Railway dashboard:
1. Go to **Variables** tab
2. Add the following (optional, defaults are fine):
   - `FLASK_ENV`: `production` (optional)
   - `PORT`: `8080` (already set in Dockerfile)

### 2.3 Configure Port
1. Go to **Settings** tab
2. Under **Networking**, expose port **8080**
3. Railway will automatically assign a public URL

## Step 3: Deploy

1. Click **"Deploy"** button
2. Railway will:
   - Build the Docker image
   - Install dependencies from `requirements.txt`
   - Start the service on port 8080
3. Wait for deployment to complete (usually 2-5 minutes)

## Step 4: Verify Deployment

Once deployed, you'll see a public URL like: `https://your-service.railway.app`

Test the health endpoint:
```bash
curl https://your-service.railway.app/health
```

Expected response:
```json
{"status": "healthy", "service": "basic-pitch"}
```

## Step 5: Get Your Service URL

1. In Railway dashboard, find your service
2. Copy the public URL (e.g., `https://your-service.railway.app`)
3. Save this URL - you'll need it for the Lovable app configuration

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is in `basic-pitch-service/`
- Ensure all dependencies are compatible with Python 3.11
- Check Railway logs for specific errors

### Service Won't Start
- Verify port is set to 8080
- Check that `app.py` exists in `basic-pitch-service/`
- Review Railway logs for startup errors

### Health Check Fails
- Ensure the service is fully deployed (check Railway dashboard)
- Verify the public URL is correct
- Check that port 8080 is exposed

## Next Steps

1. Copy your Railway service URL
2. Configure the Lovable app with this URL
3. Test the integration

## Useful Commands (Railway CLI)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# View logs
railway logs

# View environment variables
railway variables

# Deploy
railway up
```

## Monitoring

In Railway dashboard:
- **Logs**: Real-time service logs
- **Metrics**: CPU, memory, network usage
- **Deployments**: Deployment history
- **Settings**: Configuration and scaling options

## Scaling

To handle more traffic:
1. Go to **Settings** → **Scaling**
2. Increase **Replicas** (number of instances)
3. Railway will load balance across instances

## Cost

Railway pricing:
- Free tier: $5/month credit
- Pay-as-you-go: $0.000463/hour per GB RAM
- See https://railway.app/pricing for details

