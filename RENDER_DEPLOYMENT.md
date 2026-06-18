# 🚀 VOC-Triage Render Deployment Guide

**Status:** Ready to deploy  
**Estimated time:** 5 minutes  
**Cost:** Free tier (no credit card needed)

---

## ✅ What You Have Ready

- ✅ Backend code in GitHub: https://github.com/nikhilesh-s/voc-triage
- ✅ ML model trained (97.5% accuracy)
- ✅ render.yaml configuration file
- ✅ requirements.txt with all dependencies
- ✅ Frontend ready to connect

---

## 🎯 DEPLOY IN 5 MINUTES

### Step 1: Create Render Account (2 min)

1. Go to **https://render.com**
2. Click **"Sign Up"**
3. **Choose:** "GitHub" (easiest)
4. **Authorize** Render to access your GitHub
5. **Done!** You're logged in

---

### Step 2: Create Web Service (2 min)

1. Click **"New +"** → **"Web Service"**
2. **Connect repository:**
   - Select: `nikhilesh-s/voc-triage`
   - Click **"Connect"**
3. **Configure:**
   - **Name:** `voc-triage-backend` (or whatever you want)
   - **Region:** Oregon (closest/cheapest)
   - **Branch:** main
   - **Runtime:** Python 3.9
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:** (optional for now)
   - Leave empty, not needed for this app

5. **Plan:** Make sure **"Free"** is selected

6. Click **"Create Web Service"** → **Wait 2-3 minutes for build**

---

### Step 3: Get Your Live URL (1 min)

When deployment finishes:
1. You'll see a **green checkmark** ✅
2. Your **live URL** appears at top:
   ```
   https://voc-triage-backend.onrender.com
   ```
3. **Copy this URL** - you'll need it for the frontend!

---

## ✅ Verify It's Working

**Test 1: Health Check**
```bash
curl https://voc-triage-backend.onrender.com/health

# You should see:
# {"status": "healthy", "model_loaded": true, "vocs_available": 71}
```

**Test 2: Get Diseases**
```bash
curl https://voc-triage-backend.onrender.com/api/diseases

# You should see list of diseases
```

**Test 3: View API Docs**
```
Visit: https://voc-triage-backend.onrender.com/docs

# Should show Swagger UI with all 12 endpoints
```

---

## 🔗 Connect Frontend to Render Backend

### Update Frontend Environment

In `/Users/niks/Desktop/voc-triage-frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=https://voc-triage-backend.onrender.com
```

(Replace with your actual Render URL from Step 3)

### Redeploy Frontend to Vercel

```bash
cd /Users/niks/Desktop/voc-triage-frontend

# Option 1: If already deployed to Vercel
vercel --prod

# Option 2: If not yet deployed
vercel
```

---

## 📊 Expected Results After Deployment

### Backend (Render)
```
✅ Status: Active
✅ URL: https://voc-triage-backend.onrender.com
✅ /health endpoint responds
✅ /docs shows Swagger UI
✅ /api/triage/predict accepts VOC data
✅ Model loaded and ready
```

### Frontend (Vercel)
```
✅ Status: Deployed
✅ URL: https://voc-triage-frontend.vercel.app
✅ Home page loads
✅ Click "Try Demo" → Goes to Triage
✅ Click "Try COPD" → Calls Render backend
✅ Shows prediction with confidence
```

---

## ⚠️ Important Notes About Render Free Tier

### How Long URLs Last
- **Free tier web services:** Spin down after **15 minutes of inactivity**
- **When accessed:** Wake up automatically (takes ~30 seconds first request)
- **Perfect for:** Hackathon demos, testing, development

### What This Means
- ✅ You can demo to judges anytime
- ✅ First click takes 30 sec to load (Render waking up)
- ✅ Subsequent requests are instant
- ✅ URL stays the same forever
- ✅ No credit card needed

### For Permanent Always-On Deployment
If you want it always active (after hackathon):
- Upgrade to **Render Pro** ($5/month)
- OR use **Fly.io** free credits ($5/month included)

---

## 🎯 After Frontend Redeploy

### Test Full Integration

1. Open: **https://voc-triage-frontend.vercel.app**
2. See home page with features
3. Click **"Try Demo"** button
4. Directed to `/triage` page
5. Click **"Try COPD"** button
6. **Wait ~30 seconds** (first time Render wakes up)
7. See prediction result from backend! ✅

---

## 🚨 Troubleshooting

### Backend URL shows error or 504
- **Cause:** Render is booting for first time
- **Fix:** Wait 30 seconds and refresh

### Frontend shows "Failed to get prediction"
- **Cause:** Wrong NEXT_PUBLIC_API_URL
- **Fix:** 
  1. Check Render URL is correct
  2. Update `.env.local`
  3. Redeploy Vercel: `vercel --prod`

### Model not found error
- **Cause:** `backend/model.pkl` not in repo
- **Fix:** Make sure model.pkl is in GitHub repo

### Build fails on Render
- **Check logs in Render dashboard**
- **Common issues:**
  - Missing `requirements.txt`
  - Wrong Python version
  - Typo in build command

---

## 📋 Complete Deployment Checklist

- [ ] Create Render account at render.com
- [ ] Create new Web Service
- [ ] Select GitHub repo: nikhilesh-s/voc-triage
- [ ] Set build command: `pip install -r backend/requirements.txt`
- [ ] Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Choose Free plan
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (green checkmark)
- [ ] Copy live URL
- [ ] Test /health endpoint
- [ ] Update frontend .env.local with Render URL
- [ ] Redeploy frontend to Vercel: `vercel --prod`
- [ ] Test full integration (frontend → backend → prediction)
- [ ] Share live URLs with team! 🎉

---

## 🎬 Live URLs After Deployment

**Backend:** `https://voc-triage-backend.onrender.com`  
**Frontend:** `https://voc-triage-frontend.vercel.app`  
**API Docs:** `https://voc-triage-backend.onrender.com/docs`

---

## 💡 Pro Tips

1. **Render dashboard:** You can see logs, restart, etc. at https://dashboard.render.com
2. **Environment variables:** If you need to add later, go to Service → Environment
3. **Monitoring:** Green checkmark = healthy, spinning wheel = building/deploying
4. **Redeployment:** If you push new code to GitHub, Render auto-redeploys

---

## 🚀 You're Ready!

Everything is configured. Just:
1. Create Render account
2. Deploy from GitHub
3. Copy URL
4. Update frontend
5. Done! 🎉

**Total time: 5 minutes**

---

**Need help?** Check Render logs in dashboard or ask!
