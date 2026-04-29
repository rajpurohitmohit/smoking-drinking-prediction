import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

def prepare_and_train():
    print("Loading data...")
    dataset = pd.read_csv('../smoking_drinking_dataset.csv')

    print("Preprocessing data...")
    dataset.rename(columns={
        'sex': 'gender',
        'waistline': 'waist_cm',
        'height': 'height_cm',
        'weight': 'weight_kg',
        'sight_left': 'vision_left',
        'sight_right': 'vision_right',
        'SBP': 'systolic_bp',
        'DBP': 'diastolic_bp',
        'BLDS': 'blood_sugar',
        'tot_chole': 'total_cholesterol',
        'HDL_chole': 'hdl_cholesterol',
        'LDL_chole': 'ldl_cholesterol',
        'triglyceride': 'triglycerides',
        'Urine_protein': 'urine_protein',
        'serum_creatinine': 'creatinine',
        'AST': 'liver_ast',
        'ALT': 'liver_alt',
        'gamma_GTP': 'gamma_gtp',
        'SMK_stat_type_cd': 'smoking_status',
        'DRK_YN': 'is_drinker'
    }, inplace=True)

    dataset.drop(['hear_left', 'hear_right', 'urine_protein','blood_sugar'], axis=1, inplace=True)

    # Feature Engineering
    dataset['Liver_Enzyme_Ratio'] = dataset['SGOT_AST'] / dataset['SGOT_ALT']
    anemia_threshold = 12
    dataset['Anemia_Indicator'] = (dataset['hemoglobin'] < anemia_threshold).astype(int)

    # Encoding
    le = LabelEncoder()
    dataset['gender'] = le.fit_transform(dataset.gender)        # Male=1, Female=0
    dataset['is_drinker'] = le.fit_transform(dataset.is_drinker)  # N=0, Y=1 

    # Outlier clipping
    for col in dataset.columns:
        q1 = dataset[col].quantile(0.25)
        q3 = dataset[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        dataset[col] = dataset[col].clip(lower=lower, upper=upper)

    X = dataset.drop('is_drinker', axis=1)
    Y = dataset['is_drinker']

    # Scale Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Define Models with best params
    print("Training models... (This might take a few minutes)")
    lr_best = LogisticRegression(solver='saga', penalty='l1', C=1000.0, random_state=42, max_iter=500)
    rf_best = RandomForestClassifier(n_estimators=400, min_samples_split=15, min_samples_leaf=3,
                                     max_features='log2', max_depth=10, bootstrap=True, random_state=42)
    svc = SVC(probability=True, random_state=42)
    xgb_best = XGBClassifier(subsample=1.0, n_estimators=200, min_child_weight=5, max_depth=5, 
                             learning_rate=0.05, gamma=5, colsample_bytree=0.8, random_state=42, 
                             use_label_encoder=False, eval_metric='logloss')
    gb_best = GradientBoostingClassifier(subsample=0.8, n_estimators=500, min_samples_split=10, 
                                         min_samples_leaf=4, max_features=None, learning_rate=0.05, 
                                         random_state=42)

    stacking_clf = StackingClassifier(
        estimators=[
            ('lr', lr_best),
            ('rf', rf_best),
            ('svc', svc),
            ('xgb', xgb_best),
            ('gb', gb_best)
        ],
        final_estimator=LogisticRegression(),
        passthrough=True
    )

    stacking_clf.fit(X_scaled, Y)
    print("Training completed.")

    # Save models
    print("Saving models...")
    joblib.dump(stacking_clf, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("Model and scaler saved to model.pkl and scaler.pkl")

if __name__ == "__main__":
    prepare_and_train()
