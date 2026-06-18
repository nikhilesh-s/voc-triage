# 📚 VOC-Triage Development & Testing Guide

**For:** Running locally before deploying to Render

---

## 🎯 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### First Time Setup (5 minutes)

**Terminal 1: Backend**
```bash
cd /Users/niks/Desktop/voc-triage
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend/main:app --reload
```

**Terminal 2: Frontend**
```bash
cd /Users/niks/Desktop/voc-triage-frontend
npm install
npm run dev
```

**Terminal 3: Open Browser**
```
Frontend: http://localhost:3000
Backend Docs: http://localhost:8000/docs
```

---

## 🧪 Testing Checklist (Before Deploying to Render)

### Backend Tests

**1. Health Check**
```bash
curl http://localhost:8000/health
```
Expected:
```json
{"status": "healthy", "model_loaded": true, "vocs_available": 71}
```

**2. Get Diseases**
```bash
curl http://localhost:8000/api/diseases
```
Expected: List of 3 diseases (COPD, Asthma, Bronchiectasis)

**3. Try a Prediction**
```bash
curl -X POST http://localhost:8000/api/triage/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sample_id": "TEST_001",
    "voc_intensities": {
      "hydrogen sulfide": 35000,
      "dimethyl sulfide": 28000,
      "acetone": 15000
    }
  }'
```
Expected: Prediction object with disease, confidence, top_features

**4. View Swagger UI**
```
Visit: http://localhost:8000/docs
Try all endpoints here!
```

### Frontend Tests

**1. Home Page**
- [ ] Page loads
- [ ] See 4 feature cards
- [ ] Model performance stats show
- [ ] Buttons work

**2. Triage Dashboard** (`/triage`)
- [ ] Page loads
- [ ] 3 demo buttons appear (COPD, Asthma, Bronchiectasis)
- [ ] Click COPD → Loading appears
- [ ] Results show (disease, confidence, score)
- [ ] Chart displays top VOCs
- [ ] Interpretation text appears

**3. Disease Atlas** (`/disease-atlas`)
- [ ] Page loads
- [ ] 3 disease buttons appear
- [ ] Click each disease → Info updates
- [ ] Biomarkers list shows
- [ ] Confounders list shows

**4. Panel Builder** (`/panel-builder`)
- [ ] Page loads
- [ ] 3 disease buttons appear
- [ ] Click disease → Panel info updates
- [ ] VOCs list shows
- [ ] Validation strategy appears

**5. VOC Specificity** (`/voc-specificity`)
- [ ] Page loads
- [ ] Search box appears
- [ ] Try searching: "acetone"
- [ ] Results show (specificity score, diseases, confounders)

---

## 🔧 Common Local Development Commands

### Backend

**Restart backend:**
```bash
# Ctrl+C to stop, then:
uvicorn backend/main:app --reload
```

**View backend logs:**
```bash
# Logs show in terminal where uvicorn is running
```

**Change API port:**
```bash
uvicorn backend/main:app --reload --port 8001
# Then update frontend .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Frontend

**Restart frontend:**
```bash
# Ctrl+C to stop, then:
npm run dev
```

**View frontend logs:**
```bash
# Browser console: F12
# Terminal where npm run dev is running
```

**Change frontend port:**
```bash
npm run dev -- -p 3001
# Then visit: http://localhost:3001
```

---

## 📊 File Structure (For Reference)

```
voc-triage/
├── backend/
│   ├── main.py           ← FastAPI server
│   ├── model.pkl         ← Trained model
│   ├── train_model.py    ← Training script
│   └── requirements.txt   ← Dependencies
├── render.yaml           ← Render config
└── RENDER_DEPLOYMENT.md  ← This guide

voc-triage-frontend/
├── app/
│   ├── page.tsx          ← Home
│   ├── triage/page.tsx   ← Prediction
│   ├── disease-atlas/    ← Disease info
│   ├── panel-builder/    ← Panel design
│   └── voc-specificity/  ← VOC lookup
├── components/
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── Button.tsx
│   └── FeatureCard.tsx
├── lib/api.ts            ← API client
└── .env.local            ← Config
```

---

## 🐛 Debugging Tips

### Backend Issues

**Problem:** Backend won't start
```bash
# Check Python version
python3 --version

# Check venv activated
which python  # Should show venv path

# Reinstall dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Problem:** Port 8000 already in use
```bash
# Use different port
uvicorn backend/main:app --reload --port 8001
```

**Problem:** Model not found
```bash
# Make sure model.pkl exists
ls -la backend/model.pkl

# Check file size (should be ~234KB)
```

### Frontend Issues

**Problem:** Frontend won't start
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Problem:** API calls failing
```bash
# Check .env.local has correct URL
cat .env.local

# Check backend is running
curl http://localhost:8000/health
```

**Problem:** Next.js build errors
```bash
# Clear cache
rm -rf .next
npm run dev
```

---

## 🚀 Before Deploying to Render

### Final Checklist

- [ ] Backend starts without errors
- [ ] All 5 frontend pages load
- [ ] Click "Try COPD" shows prediction
- [ ] No console errors (check F12)
- [ ] All API endpoints working (test in Swagger UI)
- [ ] Model loads successfully
- [ ] Images/assets load
- [ ] Mobile responsive (test on phone or resize browser)

### Commit Before Deploy

```bash
cd /Users/niks/Desktop/voc-triage
git add .
git commit -m "Final local testing complete - ready for Render"
git push origin main
```

---

## 📱 Testing on Mobile

### Local Mobile Testing

**Find your computer's IP:**
```bash
ifconfig | grep inet
# Look for 192.168.x.x address
```

**On your phone browser:**
```
http://192.168.x.x:3000
```

This lets you test responsive design on actual mobile device!

---

## 🔍 Key Endpoints Reference

### Backend API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/triage/predict` | POST | Main prediction |
| `/api/diseases` | GET | List diseases |
| `/api/disease/{name}` | GET | Disease info |
| `/api/voc/{name}` | GET | VOC info |
| `/api/panel/{disease}` | GET | Biomarker panel |
| `/api/feature-importance` | GET | Top VOCs |
| `/docs` | GET | Swagger UI |

### Frontend Routes

| Path | Component | Purpose |
|------|-----------|---------|
| `/` | Home | Overview |
| `/triage` | Triage | Prediction |
| `/disease-atlas` | Atlas | Disease info |
| `/panel-builder` | Builder | Panel design |
| `/voc-specificity` | Checker | VOC lookup |

---

## 💡 Pro Development Tips

1. **Use Swagger UI for backend testing** - Much easier than curl
   - Visit: http://localhost:8000/docs
   - Click "Try it out" on any endpoint

2. **Use browser DevTools** - Press F12
   - Console tab shows JavaScript errors
   - Network tab shows API calls
   - Mobile view shows responsive design

3. **Hot reload working** - Save files, see changes instantly
   - Backend: uvicorn --reload watches for changes
   - Frontend: npm run dev watches for changes

4. **Keep terminals organized**
   - Terminal 1: Backend (blue background suggestion)
   - Terminal 2: Frontend (green background suggestion)
   - Terminal 3: Git/misc commands

5. **Test demo buttons first**
   - COPD: High sulfur compounds
   - Asthma: High aromatic compounds
   - Bronchiectasis: High terpenes

---

## 🎯 Development Workflow

1. **Make code changes**
2. **Save files** - Hot reload kicks in
3. **Test in browser** - Changes appear immediately
4. **Check console** - F12 for errors
5. **Test different pages** - All 5 routes
6. **Verify API calls** - Check Network tab
7. **When happy** - Commit and push to GitHub
8. **Render auto-redeploys** - From GitHub

---

## ✨ Ready to Deploy?

When all tests pass locally:

1. Commit to GitHub
2. Create Render account
3. Deploy from GitHub (follow RENDER_DEPLOYMENT.md)
4. Get live URL
5. Update frontend with live URL
6. Redeploy frontend to Vercel
7. Share URLs with team!

---

**Happy developing!** 🚀
