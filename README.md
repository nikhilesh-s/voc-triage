# VOC-Triage 🫁

> AI-powered research platform for analyzing breath volatile organic compounds to identify disease-associated chemical signatures.

## 🎯 Overview

VOC-Triage helps biomedical researchers identify disease-associated body scent biomarkers and prioritize respiratory samples for clinical investigation. Using machine learning on breath VOC profiles, we predict COPD, Asthma, and Bronchiectasis with 97.5% accuracy.

**Use Cases:**
- 🔬 Research: Identify disease-specific VOC signatures
- 🏥 Clinical triage: Prioritize patients for further testing
- 📊 Biomarker discovery: Find discriminative compounds
- 🧪 Quality control: Validate breath sample collection

---

## 📊 Model Performance

| Metric | Performance |
|--------|-------------|
| **Accuracy** | 97.5% (±2.0%) |
| **Precision** | 97.9% (±1.7%) |
| **Recall** | 97.5% (±2.0%) |
| **F1 Score** | 97.5% (±2.0%) |
| **Validation** | 5-fold stratified CV |

**Dataset:** 121 breath samples
- COPD: 33 samples
- Asthma: 53 samples
- Bronchiectasis: 35 samples

**Model:** Random Forest Classifier (100 trees, max_depth=12)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/voc-triage.git
cd voc-triage

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Run the Backend

```bash
# Start the FastAPI server
uvicorn backend.main:app --reload

# Server will start at http://localhost:8000
```

### Test the API

**Visit the interactive API docs:**
```
http://localhost:8000/docs
```

**Try a prediction:**
Click **"Try it out"** on `POST /api/triage/predict` and paste:

```json
{
  "sample_id": "TEST_SAMPLE_001",
  "voc_intensities": {
    "hydrogen sulfide": 35000.0,
    "dimethyl sulfide": 28000.0,
    "acetone": 15000.0
  }
}
```

You'll get back:
```json
{
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
  "explanation": "Predicted disease: COPD (confidence: 95%)..."
}
```

---

## 📚 API Endpoints

### Main Prediction
- **POST** `/api/triage/predict` - Predict disease from VOC profile

### Reference Data
- **GET** `/api/diseases` - List supported diseases
- **GET** `/api/disease/{disease}` - Disease information (atlas)
- **GET** `/api/voc/{voc_name}` - VOC information (checker)
- **GET** `/api/panel/{disease}` - Biomarker panel (builder)

### Model Info
- **GET** `/api/feature-importance` - Top 15 VOC features
- **GET** `/api/model-info` - Model metadata

### Demo & Health
- **GET** `/api/demo/sample/{disease}` - Demo sample
- **GET** `/api/demo/prediction/{disease}` - Demo prediction
- **GET** `/health` - Health check
- **GET** `/docs` - Swagger UI

---

## 📁 Project Structure

```
voc-triage/
├── backend/
│   ├── main.py                 # FastAPI app (all endpoints)
│   ├── train_model.py          # ML model training script
│   ├── model.pkl               # Trained Random Forest model
│   ├── feature_importance.csv  # Top 15 VOC biomarkers
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React/Next.js (coming next)
├── docs/                       # Documentation
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── GITHUB_SETUP.md            # GitHub setup instructions
```

---

## 🧪 Model Training

### Retrain the Model

If you want to retrain the model with your own data:

```bash
# Prepare your data as CSV files:
# - data/COPD_peaks.csv
# - data/Asthma_peaks.csv
# - data/Bronchiectasis_peaks.csv

# Run training script
python backend/train_model.py

# This generates:
# - backend/model.pkl (trained model)
# - backend/feature_importance.csv (top VOCs)
```

### Training Data Format

Each CSV should have:
- Rows: Samples
- Columns: VOC names with intensity values

```
VOC_Name_1,VOC_Name_2,VOC_Name_3,...
25000,5000,3000,...
24500,4800,2900,...
```

---

## 🔬 Top Biomarkers

The model identified these as most discriminative for disease prediction:

| Rank | VOC | Importance | Primary Disease |
|------|-----|-----------|-----------------|
| 1 | Hydrogen Sulfide | 13.58% | COPD |
| 2 | Toluene | 12.33% | Asthma |
| 3 | Dimethyl Trisulfide | 11.93% | COPD |
| 4 | Xylene | 8.51% | Asthma |
| 5 | Limonene | 7.32% | Bronchiectasis |
| 6 | Dimethyl Sulfide | 7.14% | COPD/Bronchiectasis |
| 7 | Pinene | 4.61% | Bronchiectasis |
| 8 | Ethylbenzene | 3.09% | Asthma |
| 9 | Acetone | 2.25% | COPD |
| 10 | Trimethylpyrazine | 1.20% | - |

---

## 📖 Disease Profiles

### COPD
- **Description:** Chronic airflow limitation from destructive lung disease
- **Biomarkers:** Hydrogen sulfide, dimethyl sulfide, acetone
- **VOC Pattern:** Elevated sulfur compounds (bacterial dysbiosis)
- **Confounders:** Smoking, occupational exposure, air quality

### Asthma
- **Description:** Chronic inflammatory airway disease
- **Biomarkers:** Toluene, xylene, ethylbenzene
- **VOC Pattern:** Elevated aromatic compounds (airway inflammation)
- **Confounders:** Allergen exposure, exercise, stress, pollution

### Bronchiectasis
- **Description:** Permanent airway dilation with chronic infection
- **Biomarkers:** Limonene, pinene, dimethyl sulfide
- **VOC Pattern:** Elevated terpenes + sulfur (chronic infection)
- **Confounders:** Infection history, immune status, genetic factors

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Expand dataset to 1000+ samples
- [ ] Test with clinical breath collection device
- [ ] Add longitudinal tracking
- [ ] Implement SHAP explainability
- [ ] Build React frontend
- [ ] Deploy to cloud (Vercel/AWS)

---

## 📝 Citation

If you use VOC-Triage in research, please cite:

```
VOC-Triage: AI-Powered Breath Analysis for Respiratory Disease Prediction
QBI UCSF Hackathon 2026
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Team

Built for QBI UCSF Hackathon 2026

---

## 📧 Contact

Questions? Issues? Open a GitHub issue or reach out to the team.

---

## 🗺️ Roadmap

- ✅ **Day 1:** Data science strategy + model training
- ✅ **Day 2:** ML model trained (97.5% accuracy) + FastAPI backend
- ⏳ **Day 3:** React frontend skeleton
- ⏳ **Days 4-7:** Full feature integration
- ⏳ **Day 8:** Polish & deployment
- ⏳ **Days 9-11:** Presentation & competition

---

**Ready to help researchers find disease biomarkers?** 🚀
