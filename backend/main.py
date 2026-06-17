#!/usr/bin/env python3
"""
VOC-TRIAGE FASTAPI BACKEND
============================
Production-ready FastAPI backend for VOC disease prediction.

This API:
- Predicts respiratory disease from VOC profiles
- Provides disease/VOC/biomarker information
- Returns explainable predictions with top contributing VOCs
- Includes demo samples for testing

Run: uvicorn main:app --reload
Visit: http://localhost:8000/docs for interactive API docs
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# INITIALIZE FASTAPI APP
# ============================================================================
app = FastAPI(
    title="VOC-Triage API",
    description="AI-powered VOC analysis for respiratory disease prediction",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# LOAD TRAINED MODEL
# ============================================================================
model_path = Path(__file__).parent / "model.pkl"

try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)

    rf_model = model_data['model']
    scaler = model_data['scaler']
    voc_names = model_data['voc_names']
    disease_map = model_data['disease_map']

    print(f"✓ Model loaded successfully: {model_path}")
    print(f"  - Model type: {type(rf_model).__name__}")
    print(f"  - VOCs: {len(voc_names)}")
    print(f"  - Classes: {list(disease_map.values())}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    raise

# ============================================================================
# LOAD FEATURE IMPORTANCE
# ============================================================================
importance_path = Path(__file__).parent / "feature_importance.csv"

try:
    feature_importance_df = pd.read_csv(importance_path)
    top_vocs = dict(zip(
        feature_importance_df['VOC'].head(15),
        feature_importance_df['Importance'].head(15)
    ))
    print(f"✓ Feature importance loaded: {importance_path}")
except Exception as e:
    print(f"✗ Error loading feature importance: {e}")
    top_vocs = {}

# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class VOCProfile(BaseModel):
    """Input: VOC intensities for a single breath sample"""
    sample_id: str = Field(..., description="Unique identifier for this sample")
    voc_intensities: Dict[str, float] = Field(
        ...,
        description="Dictionary mapping VOC names to intensity values"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "sample_id": "SAMPLE_001",
                "voc_intensities": {
                    "hexadecane": 25000.0,
                    "2-pentylfuran": 5000.0,
                    "ethylbenzene": 3000.0
                }
            }
        }


class PredictionResponse(BaseModel):
    """Output: Disease prediction with confidence and explanation"""
    sample_id: str
    predicted_disease: str
    confidence: float = Field(..., description="Confidence (0-1)")
    triage_score: int = Field(..., description="Score 0-100")
    triage_flag: str = Field(..., description="priority_level")
    top_features: List[Dict] = Field(
        ...,
        description="Top VOCs contributing to prediction"
    )
    explanation: str
    confounders: List[str] = Field(
        default_factory=list,
        description="Potential confounding factors"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "sample_id": "SAMPLE_001",
                "predicted_disease": "COPD",
                "confidence": 0.95,
                "triage_score": 95,
                "triage_flag": "elevated_priority",
                "top_features": [
                    {"voc": "hydrogen sulfide", "importance": 0.135},
                    {"voc": "dimethyl sulfide", "importance": 0.089}
                ],
                "explanation": "High hydrogen sulfide and dimethyl sulfide...",
                "confounders": ["smoking history", "air quality"]
            }
        }


class DiseaseInfo(BaseModel):
    """Information about a disease"""
    code: int
    name: str
    description: str
    icd10: str
    prevalence: str
    biomarkers: List[str]


class VOCInfo(BaseModel):
    """Information about a VOC"""
    name: str
    description: str
    relevance_score: float
    diseases: List[str]


# ============================================================================
# DISEASE DATABASE
# ============================================================================
disease_database = {
    'COPD': {
        'code': 0,
        'name': 'COPD (Chronic Obstructive Pulmonary Disease)',
        'description': 'Chronic lung disease characterized by persistent airflow limitation',
        'icd10': 'J43-J44',
        'prevalence': '3-10% globally',
        'biomarkers': ['hydrogen sulfide', 'dimethyl sulfide', 'acetone'],
        'confounders': ['smoking history', 'occupational exposure', 'air quality']
    },
    'Asthma': {
        'code': 1,
        'name': 'Asthma',
        'description': 'Chronic inflammatory airway disease with reversible airflow obstruction',
        'icd10': 'J45',
        'prevalence': '4-8% globally',
        'biomarkers': ['toluene', 'xylene', 'ethylbenzene'],
        'confounders': ['allergen exposure', 'exercise', 'stress', 'air pollution']
    },
    'Bronchiectasis': {
        'code': 2,
        'name': 'Bronchiectasis',
        'description': 'Permanent dilation of airways due to destruction of elastic tissue',
        'icd10': 'J47',
        'prevalence': '0.4-0.6% in developed countries',
        'biomarkers': ['limonene', 'pinene', 'dimethyl sulfide'],
        'confounders': ['infection history', 'immune status', 'genetic factors']
    }
}

# ============================================================================
# VOC DATABASE
# ============================================================================
voc_database = {
    'hydrogen sulfide': {
        'name': 'Hydrogen Sulfide (H₂S)',
        'description': 'Volatile sulfur compound produced by anaerobic bacteria',
        'relevance_score': 0.135,
        'diseases': ['COPD', 'Bronchiectasis'],
        'source': 'Bacterial metabolism in airways'
    },
    'toluene': {
        'name': 'Toluene',
        'description': 'Volatile organic compound linked to airway inflammation',
        'relevance_score': 0.123,
        'diseases': ['Asthma'],
        'source': 'Environmental pollution, metabolic pathways'
    },
    'xylene': {
        'name': 'Xylene',
        'description': 'Aromatic hydrocarbon associated with airway reactivity',
        'relevance_score': 0.085,
        'diseases': ['Asthma'],
        'source': 'Environmental exposure, industrial pollutants'
    },
    'limonene': {
        'name': 'Limonene',
        'description': 'Monoterpene with anti-inflammatory properties',
        'relevance_score': 0.073,
        'diseases': ['Bronchiectasis'],
        'source': 'Plant-derived, dietary sources'
    },
    'dimethyl sulfide': {
        'name': 'Dimethyl Sulfide (DMS)',
        'description': 'Volatile sulfur compound from microbial metabolism',
        'relevance_score': 0.071,
        'diseases': ['COPD', 'Bronchiectasis'],
        'source': 'Bacterial fermentation'
    }
}

# ============================================================================
# DEMO SAMPLES FOR TESTING
# ============================================================================
demo_samples = {
    'COPD': {
        'sample_id': 'DEMO_COPD_001',
        'voc_intensities': {
            'hydrogen sulfide': 35000.0,
            'dimethyl sulfide': 28000.0,
            'acetone': 15000.0,
            'toluene': 8000.0,
            'xylene': 4000.0,
            'limonene': 5000.0,
            'pinene': 3000.0
        }
    },
    'Asthma': {
        'sample_id': 'DEMO_ASTHMA_001',
        'voc_intensities': {
            'toluene': 32000.0,
            'xylene': 28000.0,
            'ethylbenzene': 18000.0,
            'hydrogen sulfide': 5000.0,
            'dimethyl sulfide': 3000.0,
            'limonene': 4000.0,
            'pinene': 2000.0
        }
    },
    'Bronchiectasis': {
        'sample_id': 'DEMO_BRONCHI_001',
        'voc_intensities': {
            'limonene': 25000.0,
            'pinene': 20000.0,
            'hydrogen sulfide': 22000.0,
            'dimethyl sulfide': 18000.0,
            'acetone': 8000.0,
            'toluene': 3000.0,
            'xylene': 2000.0
        }
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def prepare_voc_input(voc_intensities: Dict[str, float]) -> np.ndarray:
    """
    Convert VOC intensities dict to model input array.

    Creates a vector in the same order as training data, filling missing
    VOCs with mean values from training data.
    """
    # Create array in correct VOC order
    input_array = np.zeros(len(voc_names))

    for i, voc_name in enumerate(voc_names):
        if voc_name in voc_intensities:
            input_array[i] = voc_intensities[voc_name]
        else:
            # Use training data mean for missing VOCs
            input_array[i] = scaler.mean_[i] if i < len(scaler.mean_) else 0

    return input_array.reshape(1, -1)


def get_top_features(voc_intensities: Dict[str, float], top_n: int = 5) -> List[Dict]:
    """Extract top N VOCs by intensity in the sample"""
    sorted_vocs = sorted(
        voc_intensities.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return [
        {
            'voc': voc,
            'intensity': intensity,
            'importance': top_vocs.get(voc, 0.0)
        }
        for voc, intensity in sorted_vocs
    ]


def get_confounders(predicted_disease: str) -> List[str]:
    """Get list of potential confounders for predicted disease"""
    if predicted_disease in disease_database:
        return disease_database[predicted_disease]['confounders']
    return []


def generate_explanation(
    predicted_disease: str,
    confidence: float,
    top_features: List[Dict]
) -> str:
    """Generate plain-English explanation of prediction"""
    if confidence < 0.6:
        return f"Low confidence prediction ({confidence:.1%}). Result should be validated with clinical examination."

    disease_info = disease_database.get(predicted_disease, {})
    biomarkers = disease_info.get('biomarkers', [])

    top_feature_names = [f["voc"] for f in top_features[:3]]

    explanation = f"Predicted disease: {predicted_disease} (confidence: {confidence:.1%}). "

    if top_feature_names:
        explanation += f"Key biomarkers detected: {', '.join(top_feature_names)}. "

    if predicted_disease == 'COPD':
        explanation += "Pattern consistent with COPD: elevated sulfur compounds indicating bacterial dysbiosis in airways."
    elif predicted_disease == 'Asthma':
        explanation += "Pattern consistent with Asthma: elevated aromatic compounds indicating airway inflammation."
    elif predicted_disease == 'Bronchiectasis':
        explanation += "Pattern consistent with Bronchiectasis: elevated terpenes and sulfur compounds from chronic infection."

    return explanation


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """Welcome endpoint"""
    return {
        "name": "VOC-Triage API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "sample_diseases": list(demo_samples.keys())
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "vocs_available": len(voc_names)
    }


@app.post("/api/triage/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_disease(profile: VOCProfile) -> PredictionResponse:
    """
    🔬 MAIN ENDPOINT: Predict disease from VOC profile

    Takes a breath sample with VOC intensities and returns:
    - Predicted disease class
    - Confidence score (0-100)
    - Top contributing VOCs
    - Plain-English explanation

    Use for: Breath analysis, triage, research
    """
    try:
        # Prepare input
        X = prepare_voc_input(profile.voc_intensities)
        X_scaled = scaler.transform(X)

        # Make prediction
        y_pred = rf_model.predict(X_scaled)[0]
        y_proba = rf_model.predict_proba(X_scaled)[0]

        # Get disease name
        predicted_disease = disease_map[y_pred]
        confidence = float(y_proba[y_pred])
        triage_score = int(confidence * 100)

        # Determine triage flag
        if confidence >= 0.85:
            triage_flag = "elevated_priority"
        elif confidence >= 0.70:
            triage_flag = "standard_priority"
        else:
            triage_flag = "low_priority"

        # Get top features
        top_features = get_top_features(profile.voc_intensities, top_n=5)

        # Generate explanation
        explanation = generate_explanation(predicted_disease, confidence, top_features)

        # Get confounders
        confounders = get_confounders(predicted_disease)

        return PredictionResponse(
            sample_id=profile.sample_id,
            predicted_disease=predicted_disease,
            confidence=confidence,
            triage_score=triage_score,
            triage_flag=triage_flag,
            top_features=top_features,
            explanation=explanation,
            confounders=confounders
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.get("/api/diseases", tags=["Reference"])
def list_diseases():
    """List all supported disease classes"""
    return {
        "diseases": [
            {
                "name": info['name'],
                "code": info['code'],
                "description": info['description']
            }
            for info in disease_database.values()
        ]
    }


@app.get("/api/disease/{disease}", response_model=DiseaseInfo, tags=["Reference"])
def get_disease_info(disease: str):
    """Get detailed information about a disease"""
    if disease not in disease_database:
        raise HTTPException(status_code=404, detail=f"Disease '{disease}' not found")

    info = disease_database[disease]
    return DiseaseInfo(
        code=info['code'],
        name=info['name'],
        description=info['description'],
        icd10=info['icd10'],
        prevalence=info['prevalence'],
        biomarkers=info['biomarkers']
    )


@app.get("/api/voc/{voc_name}", response_model=VOCInfo, tags=["Reference"])
def get_voc_info(voc_name: str):
    """Get information about a VOC"""
    if voc_name not in voc_database:
        raise HTTPException(status_code=404, detail=f"VOC '{voc_name}' not found")

    info = voc_database[voc_name]
    return VOCInfo(
        name=info['name'],
        description=info['description'],
        relevance_score=info['relevance_score'],
        diseases=info['diseases']
    )


@app.get("/api/panel/{disease}", tags=["Reference"])
def get_biomarker_panel(disease: str):
    """Get biomarker panel for a disease"""
    if disease not in disease_database:
        raise HTTPException(status_code=404, detail=f"Disease '{disease}' not found")

    info = disease_database[disease]
    return {
        "disease": disease,
        "biomarkers": info['biomarkers'],
        "confounders": info['confounders']
    }


@app.get("/api/demo/sample/{disease}", tags=["Demo"])
def get_demo_sample(disease: str):
    """Get demo sample for testing"""
    if disease not in demo_samples:
        raise HTTPException(status_code=404, detail=f"Demo sample for '{disease}' not found")

    return demo_samples[disease]


@app.get("/api/demo/prediction/{disease}", response_model=PredictionResponse, tags=["Demo"])
async def get_demo_prediction(disease: str):
    """Get demo prediction for a disease"""
    if disease not in demo_samples:
        raise HTTPException(status_code=404, detail=f"Demo sample for '{disease}' not found")

    demo = demo_samples[disease]
    return await predict_disease(VOCProfile(**demo))


@app.get("/api/feature-importance", tags=["Model Info"])
def get_feature_importance():
    """Get top 15 most important VOCs"""
    return {
        "top_features": [
            {"voc": voc, "importance": importance}
            for voc, importance in top_vocs.items()
        ],
        "total_features": len(voc_names)
    }


@app.get("/api/model-info", tags=["Model Info"])
def get_model_info():
    """Get information about the trained model"""
    return {
        "model_type": type(rf_model).__name__,
        "n_estimators": rf_model.n_estimators if hasattr(rf_model, 'n_estimators') else None,
        "max_depth": rf_model.max_depth if hasattr(rf_model, 'max_depth') else None,
        "classes": list(disease_map.values()),
        "n_features": len(voc_names),
        "vocs": voc_names[:10] + (['...'] if len(voc_names) > 10 else [])
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    print("\n" + "="*80)
    print("VOC-TRIAGE FASTAPI BACKEND STARTED")
    print("="*80)
    print(f"✓ Model loaded: Random Forest")
    print(f"✓ Features: {len(voc_names)} VOCs")
    print(f"✓ Classes: {list(disease_map.values())}")
    print(f"✓ API docs: http://localhost:8000/docs")
    print("="*80 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
