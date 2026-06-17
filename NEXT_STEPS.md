# 🚀 NEXT STEPS - Frontend & Deployment (Day 3-4)

## ✅ COMPLETED: Day 2
- ✅ ML model trained (97.5% accuracy)
- ✅ FastAPI backend built (12 endpoints)
- ✅ Pushed to GitHub: https://github.com/nikhilesh-s/voc-triage
- ✅ Deployment report generated
- ✅ All tests passing (6/6)

---

## 📋 DAY 3 (TOMORROW): Frontend Skeleton

### Option A: Build from Scratch
```bash
# Create Next.js app
npx create-next-app@latest voc-triage-frontend --typescript --tailwind

# Install dependencies
cd voc-triage-frontend
npm install axios lucide-react recharts
```

### Option B: Use Template (Faster)
Clone a Next.js + Tailwind template and modify

### Pages to Build (5 pages)

#### 1. **Home Page** (`/`)
- Hero section with demo
- Try the API button
- Live prediction example
- Quick stats: 97.5% accuracy, 3 diseases, 71 VOCs

#### 2. **Disease Atlas** (`/diseases`)
- 3 disease cards (COPD, Asthma, Bronchiectasis)
- VOC signature heatmap
- Disease information
- Link to biomarker panel

#### 3. **Triage Dashboard** (`/triage`)
- **Main prediction interface** (most important)
- Input: VOC intensities (text, upload, or sliders)
- Output: Predicted disease + confidence + explanation
- Show top 5 contributing VOCs
- Show confounders list

#### 4. **Panel Builder** (`/builder`)
- Select disease
- Show recommended biomarkers
- Checkboxes to customize panel
- Export as JSON

#### 5. **VOC Specificity Checker** (`/checker`)
- Search for VOC
- Show:
  - Which diseases it marks
  - Importance score
  - Description
  - Source (bacterial, metabolic, etc.)

### Components to Build
- `Header` - Navigation bar
- `VocInput` - Input form for VOCs
- `PredictionResult` - Display prediction
- `DiseaseCard` - Disease info card
- `FeatureChart` - VOC importance bar chart
- `ConfidenceGauge` - Circular confidence display

### API Integration
```typescript
// Example: Call your backend
const response = await fetch('http://localhost:8000/api/triage/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sample_id: 'SAMPLE_001',
    voc_intensities: {
      'hydrogen sulfide': 35000,
      'dimethyl sulfide': 28000,
      'acetone': 15000
    }
  })
});

const prediction = await response.json();
```

---

## 📦 DAY 4: Deployment to Cloud

### Step 1: Deploy Backend (Railway or Render)

**Using Railway (recommended):**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
cd voc-triage
railway up
```

**Using Render:**
1. Go to https://render.com
2. Create new "Web Service"
3. Connect GitHub repo
4. Set runtime: Python 3.9
5. Build command: `pip install -r backend/requirements.txt`
6. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
7. Deploy

### Step 2: Deploy Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy frontend
cd voc-triage-frontend
vercel
```

**Or use GitHub integration:**
1. Go to https://vercel.com
2. Import from GitHub: `nikhilesh-s/voc-triage-frontend`
3. Set environment variable: `NEXT_PUBLIC_API_URL=<your-backend-url>`
4. Deploy

### Step 3: Update API URL in Frontend

In `.env.local`:
```
NEXT_PUBLIC_API_URL=https://voc-triage-backend.railway.app
```

---

## 🎬 Timeline (Days 3-8)

| Day | Task | Status |
|-----|------|--------|
| **Day 3 (Thu 6/18)** | Frontend skeleton (5 pages) | ⏳ Start |
| **Day 4 (Fri 6/19)** | Deploy backend + frontend | ⏳ Deploy |
| **Days 5-6 (Sat-Sun 6/20-21)** | Polish UI, add charts | ⏳ Polish |
| **Day 7 (Mon 6/22)** | Demo video (90 sec) | ⏳ Create |
| **Day 8 (Tue 6/23)** | Presentation prep | ⏳ Prepare |
| **Days 9-10 (Wed-Thu 6/24-25)** | Travel to UCSF | ⏳ Travel |
| **Hackathon (Fri-Sun 6/27-29)** | COMPETE! 🏆 | ⏳ Event |

---

## 🧠 Code Structure (Frontend)

```
voc-triage-frontend/
├── app/
│   ├── page.tsx              (Home)
│   ├── diseases/
│   │   └── page.tsx          (Disease Atlas)
│   ├── triage/
│   │   └── page.tsx          (Prediction Dashboard)
│   ├── builder/
│   │   └── page.tsx          (Panel Builder)
│   └── checker/
│       └── page.tsx          (VOC Checker)
├── components/
│   ├── Header.tsx
│   ├── VocInput.tsx
│   ├── PredictionResult.tsx
│   ├── DiseaseCard.tsx
│   ├── FeatureChart.tsx
│   └── ConfidenceGauge.tsx
├── lib/
│   ├── api.ts                (Backend API calls)
│   └── types.ts              (TypeScript interfaces)
└── styles/
    └── globals.css
```

---

## 💡 Quick Wins (Easy Wins to Start)

1. **Home Page** - Just copy design from README
2. **Health Check** - Call `/health` endpoint to verify API works
3. **Demo Prediction** - Use `/api/demo/prediction/COPD` to show working example
4. **Disease Info** - Call `/api/diseases` and display as cards
5. **Feature List** - Call `/api/feature-importance` and show top 15

---

## 🎯 Minimum Viable Frontend (MVP)

To have something working by Day 3 EOD:

1. Home page with hero + one demo button
2. Single prediction page that:
   - Takes VOC input
   - Calls backend
   - Shows result
3. Navigation to pages (don't need to build all 5 yet)

You can polish the other 4 pages on Days 4-6.

---

## 🚀 Backend API Reference (for frontend devs)

Your backend is at:
- **Local:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs (use this!)
- **API calls:** Exactly like shown above

### Main endpoint your frontend will use:
```
POST /api/triage/predict
Input: { sample_id, voc_intensities }
Output: { predicted_disease, confidence, triage_score, top_features, explanation, confounders }
```

All other endpoints are for reference data.

---

## ✨ Things That Will Impress Judges

1. **Working demo** - Live prediction on home page
2. **Explanation** - Show which VOCs matter (top_features)
3. **Confidence bars** - Visual representation of certainty
4. **Disease education** - Info about each condition
5. **Biomarker panel** - Let users customize which VOCs to measure
6. **Professional design** - Clean, modern UI

---

## 🎬 Your Commands Tomorrow (Day 3)

```bash
# Create frontend
npx create-next-app@latest voc-triage-frontend --typescript --tailwind

# Install extra deps
npm install axios lucide-react recharts

# Start dev server
npm run dev

# Visit http://localhost:3000
```

---

## 💬 Questions to Ask Yourself

- **If home page demo doesn't work:** Check backend is running (`uvicorn backend/main:app --reload` in terminal)
- **If API calls fail:** Check CORS - it's enabled on backend, should be fine
- **If you need more time:** Drop one of the 5 pages (builder or checker), focus on core 3: Home, Atlas, Triage
- **If stuck on design:** Use Shadcn/ui components, they're beautiful and fast

---

## 🏆 Remember

You already have:
- ✅ 97.5% accurate ML model
- ✅ Production-ready backend
- ✅ Full API documentation
- ✅ GitHub repo ready

**You just need to build a pretty face for it.** That's the easy part! 

The hard ML part is DONE. 🎉

---

## 📞 Resources

- **Next.js:** https://nextjs.org/docs
- **Tailwind:** https://tailwindcss.com/docs
- **Shadcn/ui:** https://ui.shadcn.com
- **Recharts:** https://recharts.org
- **Your API:** http://localhost:8000/docs

---

**Good luck! You've got this!** 🚀

Next step: Reply when frontend is started, and I can help wire it to the backend!
