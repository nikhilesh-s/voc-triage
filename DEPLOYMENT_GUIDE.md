# 🚀 VOC-Triage Production Deployment Guide

## Step 1: Deploy Backend (Railway)

### Option A: Railway Web UI (Easiest)

1. **Go to:** https://railway.app
2. **Create account** (free tier available)
3. **Create new project** → "Deploy from GitHub"
4. **Select repo:** `nikhilesh-s/voc-triage`
5. **Configure:**
   - Root directory: `.` (empty or project root)
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. **Deploy** → Wait ~2 minutes
7. **Get URL** from deployment (looks like `https://voc-triage-production.railway.app`)

### Option B: Railway CLI

```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Deploy backend
cd /Users/niks/Desktop/voc-triage
railway up

# Get URL
railway open
```

---

## Step 2: Deploy Frontend (Vercel)

### Using Vercel Web UI

1. **Go to:** https://vercel.com
2. **Import project** → "Import Git Repository"
3. **Select repo:** `nikhilesh-s/voc-triage-frontend`
4. **Configure:**
   - Framework: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`
   - Install command: `npm install`
5. **Environment Variables:**
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-railway-url` (from Step 1)
6. **Deploy** → Wait ~3 minutes
7. **Get URL** (looks like `https://voc-triage-frontend.vercel.app`)

### Using Vercel CLI

```bash
# Install
npm install -g vercel

# Login
vercel login

# Deploy from frontend directory
cd /Users/niks/Desktop/voc-triage-frontend
vercel

# When prompted:
# - Set up and deploy? Yes
# - Which scope? Your personal account
# - Link to existing project? No
# - Project name: voc-triage-frontend
# - Detected framework: Next.js
# - Build & output directory: Accept defaults

# Add environment variable
vercel env add NEXT_PUBLIC_API_URL

# Redeploy with env var
vercel --prod
```

---

## Step 3: Test Live Deployment

```bash
# Test backend health
curl https://your-railway-url/health

# Test backend API
curl https://your-railway-url/api/diseases

# Open frontend in browser
https://your-frontend-url
```

### Test Flows in Frontend

1. **Home page** → Features overview
2. **Triage** → Click "Try COPD" → See live prediction from backend
3. **Disease Atlas** → Browse diseases
4. **Panel Builder** → Select disease
5. **VOC Specificity** → Search "acetone"

---

## Step 4: Update Prod URLs

### In frontend `.env.production`:

```
NEXT_PUBLIC_API_URL=https://your-railway-backend-url
```

### Redeploy frontend if needed:

```bash
cd /Users/niks/Desktop/voc-triage-frontend
vercel --prod
```

---

## ✅ Deployment Checklist

- [ ] Backend deployed to Railway/Render
- [ ] Backend URL working (test /health endpoint)
- [ ] Frontend deployed to Vercel
- [ ] NEXT_PUBLIC_API_URL environment variable set
- [ ] Frontend loads at https://...vercel.app
- [ ] Click "Try Demo" on home → Triage page works
- [ ] Click "Try COPD" → Prediction appears
- [ ] Disease Atlas loads
- [ ] VOC Specificity search works

---

## URLs After Deployment

**Frontend:** https://voc-triage-frontend.vercel.app  
**Backend:** https://voc-triage-production.railway.app  
**API Docs:** https://voc-triage-production.railway.app/docs  

---

## Troubleshooting

### Backend says "Model not found"
- Make sure `backend/model.pkl` is in the repo
- Check Railway build logs

### Frontend shows "Failed to get prediction"
- Verify `NEXT_PUBLIC_API_URL` environment variable is set
- Check that backend URL is correct
- Test `https://backend-url/health` in browser

### CORS errors
- CORS is enabled on backend
- Make sure frontend is calling correct API URL
- Check browser console for exact error

---

## Next Steps

1. **Deploy** following steps above
2. **Test** all flows on production
3. **Share** URLs with team
4. **Days 5-7:** Polish UI and create demo video
5. **Day 8:** Present at hackathon!

---

**Happy deploying!** 🚀
