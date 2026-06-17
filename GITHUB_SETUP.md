# GitHub Setup Instructions

Complete step-by-step guide to push VOC-Triage to GitHub.

## 📋 Prerequisites

- GitHub account (free at https://github.com)
- Git installed locally (`git --version`)
- This repository cloned or created

---

## ✅ Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `voc-triage`
3. **Description:** `AI-powered breath analysis for respiratory disease prediction`
4. **Visibility:** Public (for hackathon visibility)
5. **Skip initialization** (we'll push our code)
6. **Click "Create repository"**

GitHub will show you the commands. We'll use them below.

---

## 🔧 Step 2: Initialize Git Locally

```bash
cd voc-triage

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: VOC-Triage MVP - 97.5% accuracy FastAPI backend"

# Set your username (if not set)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## 🚀 Step 3: Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/voc-triage.git
git branch -M main
git push -u origin main
```

**You might be asked for authentication:**
- GitHub username
- Personal access token (https://github.com/settings/tokens)

---

## 🔑 If Authentication Fails

### Create Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `admin:repo_hook`
4. Copy the token
5. When git asks for password, paste the token

### OR Use SSH (Recommended)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add key to SSH agent
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub: https://github.com/settings/keys
cat ~/.ssh/id_ed25519.pub

# Use SSH URL instead
git remote set-url origin git@github.com:YOUR_USERNAME/voc-triage.git
```

---

## ✅ Step 4: Verify Push

```bash
# Check git status
git status

# Should show: On branch main, nothing to commit

# View remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/voc-triage.git (fetch)
# origin  https://github.com/YOUR_USERNAME/voc-triage.git (push)
```

Visit your GitHub repo to confirm everything is there:
```
https://github.com/YOUR_USERNAME/voc-triage
```

---

## 🧪 Step 5: Test Backend Locally

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the backend
uvicorn backend.main:app --reload

# Server should start at http://localhost:8000
```

---

## 📚 Step 6: Test API

### Option A: Interactive Docs

Visit: http://localhost:8000/docs

This is the **Swagger UI** where you can test all endpoints interactively.

### Option B: Command Line

```bash
# Get health status
curl http://localhost:8000/health

# Get list of diseases
curl http://localhost:8000/api/diseases

# Make a prediction
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

# Get demo prediction
curl http://localhost:8000/api/demo/prediction/COPD
```

### Option C: Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/api/triage/predict",
    json={
        "sample_id": "TEST_001",
        "voc_intensities": {
            "hydrogen sulfide": 35000,
            "dimethyl sulfide": 28000,
            "acetone": 15000
        }
    }
)

print(response.json())
```

---

## 🎯 Expected Results

If everything works, you should see:

```json
{
  "sample_id": "TEST_001",
  "predicted_disease": "COPD",
  "confidence": 0.95,
  "triage_score": 95,
  "triage_flag": "elevated_priority",
  "top_features": [
    {
      "voc": "hydrogen sulfide",
      "intensity": 35000.0,
      "importance": 0.1358
    }
  ],
  "explanation": "Predicted disease: COPD (confidence: 95%). Key biomarkers detected: hydrogen sulfide, dimethyl sulfide, acetone. Pattern consistent with COPD: elevated sulfur compounds indicating bacterial dysbiosis in airways.",
  "confounders": [
    "smoking history",
    "occupational exposure",
    "air quality"
  ]
}
```

✅ **Backend is working!**

---

## 📝 Commit Message Guide

When committing changes, use clear messages:

```bash
# Feature
git commit -m "Add new VOC: limonene detection"

# Bug fix
git commit -m "Fix: handle missing VOCs in prediction"

# Documentation
git commit -m "Docs: update API endpoints"

# Refactoring
git commit -m "Refactor: extract disease logic to helper"
```

---

## 🔄 Common Git Commands

```bash
# Check status
git status

# Add specific files
git add backend/main.py

# View changes
git diff
git diff --cached

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest from GitHub
git pull origin main

# View commit history
git log --oneline
```

---

## 🚀 Next Steps

Once backend is tested:

1. **Push any test changes:**
   ```bash
   git add .
   git commit -m "Test: backend working locally"
   git push origin main
   ```

2. **Build frontend:**
   - Follow the frontend setup instructions
   - Build React/Next.js components
   - Connect to this API

3. **Deploy:**
   - Use Vercel for frontend
   - Use Railway/Render for backend
   - Configure environment variables

---

## 🆘 Troubleshooting

### Git says "branch already exists"
```bash
git branch -D main  # Delete local main
git checkout -b main  # Create new main
```

### Permission denied (publickey)
```bash
# SSH key issues - use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/voc-triage.git
```

### "Could not read from remote repository"
```bash
# Check network
ping github.com

# Verify SSH key is added to GitHub (for SSH method)
# OR use HTTPS with personal access token
```

### Model file too large
```bash
# Don't commit large files (>100MB)
# Use Git LFS for large files:
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

---

## ✨ You're Done!

Your VOC-Triage backend is:
- ✅ Trained (97.5% accuracy)
- ✅ On GitHub
- ✅ Tested locally
- ✅ Ready for frontend integration

**Next:** Build the React frontend!

---

## 📚 Resources

- GitHub Docs: https://docs.github.com
- Git Guide: https://git-scm.com/doc
- FastAPI Docs: https://fastapi.tiangolo.com
- Uvicorn: https://www.uvicorn.org

---

**Questions? Check the README.md or open a GitHub issue!**
