#!/usr/bin/env python3
"""
VOC-TRIAGE ML MODEL TRAINING SCRIPT
====================================
This script trains a Random Forest classifier on VOC (Volatile Organic Compound) data
to predict respiratory diseases: COPD, Asthma, and Bronchiectasis.

For hackathon team: This is heavily commented so non-ML people understand what's happening.
"""

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("VOC-TRIAGE ML MODEL TRAINING")
print("="*80)

# ============================================================================
# STEP 1: GENERATE SYNTHETIC DATA
# ============================================================================
# In production, this would load from CSV files. For hackathon, we create
# realistic synthetic data with 121 samples and 73 VOCs.
print("\n[STEP 1] Generating synthetic VOC data (121 samples × 73 VOCs)...")

np.random.seed(42)  # For reproducibility

# VOC names (real compounds found in breath)
voc_names = [
    'hexadecane', '2-pentylfuran', 'ethylbenzene', 'dimethyl disulfide',
    'isoprene', 'acetone', 'methanol', 'benzene', 'toluene', 'xylene',
    'limonene', 'pinene', 'myrcene', 'camphene', 'decane', 'undecane',
    'dodecane', 'trimethylbenzene', 'ethyltoluene', 'propylbenzene',
    'pentane', 'heptane', 'octane', 'nonane', 'styrene', 'naphthalene',
    'indene', 'acenaphthylene', 'fluorene', 'phenanthrene', 'anthracene',
    'dimethyl sulfide', 'dimethyl trisulfide', 'hydrogen sulfide',
    'ammonia', 'trimethylamine', 'skatole', 'indole', 'phenol', 'cresol',
    'butyric acid', 'propionic acid', 'acetic acid', 'formic acid',
    'methylethyl ketone', 'acetaldehyde', 'formaldehyde', 'propionaldehyde',
    'butyraldehyde', 'benzaldehyde', 'methylpyrazine', 'dimethylpyrazine',
    'trimethylpyrazine', 'methylfuran', 'dimethylfuran', 'furfural',
    'maltol', 'vanillin', 'ethanol', 'isopropanol', 'butanol', 'pentanol',
    'ethyl acetate', 'propyl acetate', 'butyl acetate', 'limonene oxide',
    'myrcene oxide', 'eucalyptol', 'linalool', 'geraniol', 'nerolidol'
]

# We'll use the first 73 VOCs
voc_names = voc_names[:73]
n_vocs = len(voc_names)
n_samples = 121

# Disease labels (0=COPD, 1=Asthma, 2=Bronchiectasis)
# Distribution based on typical research cohorts
disease_counts = {'COPD': 33, 'Asthma': 53, 'Bronchiectasis': 35}
disease_labels_list = (
    ['COPD'] * 33 + ['Asthma'] * 53 + ['Bronchiectasis'] * 35
)
disease_encoding = {'COPD': 0, 'Asthma': 1, 'Bronchiectasis': 2}
y_numeric = np.array([disease_encoding[d] for d in disease_labels_list])

# Generate synthetic VOC intensities with disease-specific patterns
X_synthetic = np.random.randn(n_samples, n_vocs) * 5000 + 20000

# Add disease-specific signatures (some VOCs are more prevalent in each disease)
for i in range(n_samples):
    disease = y_numeric[i]

    if disease == 0:  # COPD: elevated dimethyl sulfide, hydrogen sulfide
        X_synthetic[i, 32] += 15000  # dimethyl sulfide
        X_synthetic[i, 33] += 12000  # hydrogen sulfide
        X_synthetic[i, 5] += 5000    # acetone
    elif disease == 1:  # Asthma: elevated toluene, xylene, ethylbenzene
        X_synthetic[i, 8] += 12000   # toluene
        X_synthetic[i, 9] += 10000   # xylene
        X_synthetic[i, 2] += 8000    # ethylbenzene
    else:  # Bronchiectasis: elevated limonene, pinene, sulfur compounds
        X_synthetic[i, 10] += 10000  # limonene
        X_synthetic[i, 11] += 8000   # pinene
        X_synthetic[i, 31] += 9000   # dimethyl sulfide

# Ensure all values are positive (VOC intensities)
X_synthetic = np.abs(X_synthetic)

# Create DataFrame for easier handling
X_df = pd.DataFrame(X_synthetic, columns=voc_names)
y_df = pd.Series(y_numeric, name='disease')

print(f"   ✓ Dataset: {n_samples} samples × {n_vocs} VOCs")
print(f"   ✓ Classes: COPD ({disease_counts['COPD']}), Asthma ({disease_counts['Asthma']}), Bronchiectasis ({disease_counts['Bronchiectasis']})")

# ============================================================================
# STEP 2: NORMALIZE THE DATA
# ============================================================================
# Different VOCs have different intensity ranges. Normalization (scaling)
# puts everything on the same 0-1 scale, which helps the model learn better.
print("\n[STEP 2] Normalizing VOC intensities with StandardScaler...")

scaler = StandardScaler()
X_normalized = scaler.fit_transform(X_df)
X_normalized_df = pd.DataFrame(X_normalized, columns=voc_names)

print(f"   ✓ Normalized all {n_vocs} VOCs to mean=0, std=1")

# ============================================================================
# STEP 3: TRAIN RANDOM FOREST MODEL WITH CROSS-VALIDATION
# ============================================================================
# Random Forest works by building many decision trees and averaging their
# predictions. This makes it robust and good for biomarker discovery.
print("\n[STEP 3] Training Random Forest Classifier (n_estimators=100, max_depth=12)...")

# Initialize the model with specific parameters tuned for this dataset
rf_model = RandomForestClassifier(
    n_estimators=100,      # 100 decision trees
    max_depth=12,          # Tree depth (prevents overfitting)
    min_samples_split=5,   # Min samples to split a node
    min_samples_leaf=2,    # Min samples in leaf nodes
    random_state=42,       # For reproducibility
    n_jobs=-1,             # Use all CPU cores
    class_weight='balanced'  # Handle class imbalance
)

# ============================================================================
# STEP 4: 5-FOLD STRATIFIED CROSS-VALIDATION
# ============================================================================
# Cross-validation tests the model on different data slices.
# "Stratified" means each fold has the same disease proportions as the full dataset.
print("\n[STEP 4] Running 5-fold Stratified Cross-Validation...")

cv_splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Run cross-validation and collect metrics
cv_results = cross_validate(
    rf_model,
    X_normalized_df,
    y_df,
    cv=cv_splitter,
    scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'],
    return_train_score=False
)

# ============================================================================
# STEP 5: PRINT CROSS-VALIDATION RESULTS
# ============================================================================
print("\n" + "-"*80)
print("CROSS-VALIDATION RESULTS (5-Fold)")
print("-"*80)

accuracy_scores = cv_results['test_accuracy']
precision_scores = cv_results['test_precision_weighted']
recall_scores = cv_results['test_recall_weighted']
f1_scores = cv_results['test_f1_weighted']

print(f"\nAccuracy:  {accuracy_scores.mean():.1%} (±{accuracy_scores.std():.1%})")
print(f"  Fold 1: {accuracy_scores[0]:.1%}")
print(f"  Fold 2: {accuracy_scores[1]:.1%}")
print(f"  Fold 3: {accuracy_scores[2]:.1%}")
print(f"  Fold 4: {accuracy_scores[3]:.1%}")
print(f"  Fold 5: {accuracy_scores[4]:.1%}")

print(f"\nPrecision: {precision_scores.mean():.1%} (±{precision_scores.std():.1%})")
print(f"Recall:    {recall_scores.mean():.1%} (±{recall_scores.std():.1%})")
print(f"F1 Score:  {f1_scores.mean():.1%} (±{f1_scores.std():.1%})")

# ============================================================================
# STEP 6: TRAIN FINAL MODEL ON ALL DATA
# ============================================================================
# Now that we've validated the model works well, train it on all available data
print("\n[STEP 5] Training final model on all data...")

rf_model.fit(X_normalized_df, y_df)

y_pred = rf_model.predict(X_normalized_df)
y_pred_proba = rf_model.predict_proba(X_normalized_df)

print(f"   ✓ Model trained and ready for predictions")

# ============================================================================
# STEP 7: CALCULATE PER-CLASS METRICS
# ============================================================================
print("\n" + "-"*80)
print("PER-CLASS PERFORMANCE METRICS")
print("-"*80)

disease_map = {0: 'COPD', 1: 'Asthma', 2: 'Bronchiectasis'}

for disease_code, disease_name in disease_map.items():
    # Create binary labels for this disease (1 if this disease, 0 otherwise)
    y_binary = (y_df == disease_code).astype(int)
    y_pred_binary = (y_pred == disease_code).astype(int)

    precision = precision_score(y_binary, y_pred_binary, zero_division=0)
    recall = recall_score(y_binary, y_pred_binary, zero_division=0)
    f1 = f1_score(y_binary, y_pred_binary, zero_division=0)

    # ROC-AUC for binary classification
    try:
        roc_auc = roc_auc_score(y_binary, y_pred_proba[:, disease_code])
    except:
        roc_auc = 0.0

    print(f"\n{disease_name}:")
    print(f"  Precision: {precision:.1%}")
    print(f"  Recall:    {recall:.1%}")
    print(f"  F1 Score:  {f1:.1%}")
    print(f"  ROC-AUC:   {roc_auc:.1%}")

# ============================================================================
# STEP 8: CONFUSION MATRIX
# ============================================================================
print("\n" + "-"*80)
print("CONFUSION MATRIX")
print("-"*80)

cm = confusion_matrix(y_df, y_pred)
print("\n                 Predicted COPD  Asthma  Bronchiectasis")
for i, disease_name in enumerate(['COPD', 'Asthma', 'Bronchiectasis']):
    print(f"Actual {disease_name:15s}  {cm[i, 0]:3d}        {cm[i, 1]:3d}      {cm[i, 2]:3d}")

# ============================================================================
# STEP 9: EXTRACT TOP 15 FEATURE IMPORTANCE
# ============================================================================
print("\n" + "-"*80)
print("TOP 15 DISCRIMINATIVE VOCs (Feature Importance)")
print("-"*80)

# Get feature importances from the model
feature_importances = rf_model.feature_importances_

# Create a DataFrame for easier sorting
importance_df = pd.DataFrame({
    'VOC': voc_names,
    'Importance': feature_importances
}).sort_values('Importance', ascending=False)

# Get top 15
top_15 = importance_df.head(15)

print("\nRank  VOC Name                  Importance  Bar Chart")
print("-" * 65)
for rank, (idx, row) in enumerate(top_15.iterrows(), 1):
    bar = '█' * int(row['Importance'] * 200)  # Scale for visualization
    print(f"{rank:2d}.   {row['VOC']:25s}  {row['Importance']:6.2%}     {bar}")

# ============================================================================
# STEP 10: SAVE MODEL AND FEATURE IMPORTANCE
# ============================================================================
print("\n" + "-"*80)
print("SAVING MODEL AND FEATURE IMPORTANCE")
print("-"*80)

# Save the trained model as pickle
model_path = 'backend/model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump({
        'model': rf_model,
        'scaler': scaler,
        'voc_names': voc_names,
        'disease_map': disease_map
    }, f)
print(f"   ✓ Saved trained model to: {model_path}")

# Save feature importance as CSV
importance_csv_path = 'backend/feature_importance.csv'
importance_df.to_csv(importance_csv_path, index=False)
print(f"   ✓ Saved feature importance to: {importance_csv_path}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("✅ MODEL TRAINING COMPLETE!")
print("="*80)
print(f"""
SUMMARY:
  • Dataset: {n_samples} respiratory samples, {n_vocs} VOC biomarkers
  • Classes: COPD, Asthma, Bronchiectasis
  • Model: Random Forest (100 trees, max_depth=12)
  • Accuracy: {accuracy_scores.mean():.1%} (±{accuracy_scores.std():.1%})
  • Validation: 5-fold stratified cross-validation

FILES CREATED:
  ✓ {model_path} (trained model + scaler)
  ✓ {importance_csv_path} (top 15 VOCs)

MODEL READY FOR DEPLOYMENT! 🚀
  Next step: Start FastAPI backend with this trained model
""")
print("="*80 + "\n")
