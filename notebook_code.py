# Libraries: 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option("display.max_columns",None)
import warnings
warnings.filterwarnings("ignore")


# Evaluation
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score

---
dataset = pd.read_csv('smoking_drinking_dataset.csv')

---
dataset.head()

---
dataset.shape

---
dataset.dtypes

---
dataset.describe()

---
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

---
dataset.head(3)

---
print("Missing values:\n", dataset.isnull().sum())

---
dataset[dataset.duplicated()]

---
data['']drop

---
# current_y_is_smoking_or_drinking = 'smoking_status'
currently_is_smoking_or_drinking = 'is_drinker'

sns.set(style="whitegrid")
plt.figure(figsize=(40, 20))

for idx, column in enumerate(['gender', 'age', 'height_cm', 'weight_kg', 'vision_left', 'vision_right', 'hear_left', 'hear_right',
                              "urine_protein", currently_is_smoking_or_drinking, "is_drinker"], start=1):

    plt.subplot(4, 3, idx)

    sns.countplot(x=column, data=dataset , hue=currently_is_smoking_or_drinking)

    plt.xlabel(column)
    plt.xticks(rotation=70)
    plt.ylabel('Frequency')
    plt.title(f'Frequency of {column} by Smoking Status')

plt.tight_layout()
plt.show()

---
dataset.groupby('is_drinker').mean(numeric_only=True)

---
dataset.drop(['hear_left', 'hear_right', 'urine_protein','blood_sugar'], axis=1, inplace=True)

---
# Liver_Enzyme_Ratio = SGOT_AST / SGOT_ALT
dataset['Liver_Enzyme_Ratio'] = dataset['SGOT_AST'] / dataset['SGOT_ALT']

---
# Anemia_Indicator if hemoglobin < 12 --> anemia
anemia_threshold = 12
dataset['Anemia_Indicator'] = (dataset['hemoglobin'] < anemia_threshold).astype(int)

---
dataset.head()

---
dataset['is_drinker'].value_counts() # Dataset already balanced

---
plt.figure(figsize=(12,8))
sns.countplot(x='is_drinker', data=dataset)
plt.title('Class Distribution')
plt.show()

---
from sklearn.preprocessing import LabelEncoder

---
le = LabelEncoder()

---
dataset['gender'] = le.fit_transform(dataset.gender)        # Male=1, Female=0
dataset['is_drinker'] = le.fit_transform(dataset.is_drinker)  # N=0, Y=1 
dataset

---
dataset.describe()

---
original_data = dataset.copy() 

---
# Apply IQR-based clipping to numerical columns
for col in dataset.columns:
    q1 = dataset[col].quantile(0.25)
    q3 = dataset[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    dataset[col] = dataset[col].clip(lower=lower, upper=upper)

---
print("After outlier treatment:")
print(dataset.describe())

---
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 20))

# Boxplot before
original_data.boxplot(ax=axes[0])
axes[0].set_title("Before Outlier Treatment")
axes[0].tick_params(axis='x', rotation=45)

# Boxplot after
dataset.boxplot(ax=axes[1])
axes[1].set_title("After Outlier Treatment")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

---
from sklearn.model_selection import train_test_split

---
X = dataset.drop('is_drinker', axis=1)
Y = dataset['is_drinker']

---
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

---
print(X.shape, X_train.shape, X_test.shape)

---
print(Y.shape, Y_train.shape, Y_test.shape)

---
from sklearn.preprocessing import StandardScaler

---
scaler = StandardScaler()

---
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

---
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV

---
lr_param = {
    'C': np.logspace(-3, 3, 7),  # Exponential range of C values
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear', 'saga']
}

---
lr = LogisticRegression(random_state=42, max_iter=500)

---
lr_random_search = RandomizedSearchCV(
    estimator=lr,
    param_distributions=lr_param,
    n_iter=20,  # Number of random combinations to try
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

---
lr_random_search.fit(X_train, Y_train)

---
lr_best_params = lr_random_search.best_params_
print("Best Parameters for Logistic Regression:", lr_best_params)

---
lr_best = LogisticRegression(solver='saga',penalty='l1',C=np.float64(1000.0), random_state=42, max_iter=500)
lr_best.fit(X_train, Y_train)

---
lr_train_predictions = lr_best.predict(X_train)
lr_test_predictions = lr_best.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, lr_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, lr_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, lr_train_predictions))
print("------------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, lr_test_predictions))

---
from sklearn.ensemble import RandomForestClassifier

---
rf_param = {
    'n_estimators': [50, 100, 200, 500],  # Number of trees
    'max_depth': [10, 20, 30, None],  # Maximum depth of each tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples to split a node
    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples in a leaf
    'max_features': ['auto', 'sqrt', 'log2'],  # Number of features to consider for best split
    'bootstrap': [True, False]  # Whether bootstrap samples are used
}

---
rf = RandomForestClassifier(random_state=42)

---
rf_random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=rf_param,
    n_iter=20,  # Number of random combinations to try
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

---
rf_random_search.fit(X_train, Y_train)

---
rf_best_params = rf_random_search.best_params_
print("Best Parameters for Random Forest:", rf_best_params)

---
rf_best = RandomForestClassifier(n_estimators=400, min_samples_split=15, min_samples_leaf=3,
                            max_features='log2', max_depth=10, bootstrap=True, random_state=42)
rf_best.fit(X_train, Y_train)

---
rf_train_predictions = rf_best.predict(X_train)
rf_test_predictions = rf_best.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, rf_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, rf_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, rf_train_predictions))
print("------------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, rf_test_predictions))

---
from sklearn.svm import SVC

---
svc = SVC(probability=True, random_state=42)

---
svc.fit(X_train, Y_train)

---
svc_train_predictions = svc.predict(X_train)
svc_test_predictions = svc.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, svc_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, svc_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, svc_train_predictions))
print("------------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, svc_test_predictions))

---
from xgboost import XGBClassifier

---
xgb_param = {
    'n_estimators': [50, 100, 200, 500],  # Number of trees
    'max_depth': [3, 5, 10, 15],  # Maximum tree depth
    'learning_rate': [0.01, 0.05, 0.1, 0.2],  # Learning rate
    'subsample': [0.6, 0.8, 1.0],  # Fraction of samples used for training
    'colsample_bytree': [0.6, 0.8, 1.0],  # Fraction of features used at each split
    'gamma': [0, 1, 5],  # Minimum loss reduction
    'min_child_weight': [1, 3, 5],  # Minimum sum of instance weight needed for a child
}

---
xgb = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')

---
xgb_random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=xgb_param,
    n_iter=20,  # Number of random combinations to try
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

---
xgb_random_search.fit(X_train, Y_train)

---
xgb_best_params = xgb_random_search.best_params_
print("Best Parameters for XGBoost:", xgb_best_params)

---
xgb_best = XGBClassifier(subsample=1.0, n_estimators=200, min_child_weight=5, max_depth=5, 
                           learning_rate= 0.05, gamma=5, colsample_bytree=0.8, random_state=42, use_label_encoder=False, eval_metric='logloss')
xgb_best.fit(X_train, Y_train)

---
xgb_train_predictions = xgb_best.predict(X_train)
xgb_test_predictions = xgb_best.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, xgb_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, xgb_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, xgb_train_predictions))
print("------------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, xgb_test_predictions))

---
from sklearn.ensemble import GradientBoostingClassifier

---
gb_param = {
    'n_estimators': [50, 100, 200, 500],  # Number of boosting stages
    'max_depth': [3, 5, 10],  # Maximum depth of the individual estimators
    'learning_rate': [0.01, 0.05, 0.1, 0.2],  # Learning rate shrinks contribution of each tree
    'subsample': [0.6, 0.8, 1.0],  # Fraction of samples used for fitting individual base learners
    'min_samples_split': [2, 5, 10],  # Minimum samples to split an internal node
    'min_samples_leaf': [1, 2, 4],  # Minimum samples in a leaf node
    'max_features': ['sqrt', 'log2', None],  # Number of features to consider for split
}

---
gb = GradientBoostingClassifier(random_state=42)

---
gb_random_search = RandomizedSearchCV(
    estimator=gb,
    param_distributions=gb_param,
    n_iter=20,  # Number of random combinations to try
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

---
gb_random_search.fit(X_train, Y_train)

---
gb_best_params = gb_random_search.best_params_
print("Best Parameters for Gradient Boosting:", gb_best_params)

---
gb_best = GradientBoostingClassifier(subsample=0.8, n_estimators=500, min_samples_split=10, min_samples_leaf=4, 
                                     max_features=None, learning_rate=0.05, random_state=42)
gb_best.fit(X_train, Y_train)

---
gb_train_predictions = gb_best.predict(X_train)
gb_test_predictions = gb_best.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, gb_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, gb_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, gb_train_predictions))
print("-----------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, gb_test_predictions))

---
from sklearn.ensemble import StackingClassifier

---
stacking_clf = StackingClassifier(
    estimators=[
        ('lr', lr_best),
        ('rf', rf_best),
        ('svc', svc),
        ('xgb', xgb_best),
        ('gb', gb_best)
    ],
    final_estimator=LogisticRegression(),  # Meta-learner
    passthrough=True  # Optional: gives final model access to original features as well
)

---
stacking_clf.fit(X_train, Y_train)

---
stacking_train_predictions = stacking_clf.predict(X_train)
stacking_test_predictions = stacking_clf.predict(X_test)

---
print(f"\nTraining Accuracy: {accuracy_score(Y_train, stacking_train_predictions) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(Y_test, stacking_test_predictions) * 100:.2f}%")

---
print("\nClassification Report on Training Data:")
print(classification_report(Y_train, stacking_train_predictions))
print("-----------------------------------------------------")
print("\nClassification Report on Testing Data:")
print(classification_report(Y_test, stacking_test_predictions))

---
first_row_values = dataset.iloc[3].values
formatted_values = ", ".join(map(str, first_row_values))

print(f"({formatted_values})")

---
dataset.head(3)

---
input_data = (1.0, 40.0, 165.0, 75.0, 91.0, 1.2, 1.5, 120.0, 70.0, 136.0, 41.0, 74.0, 104.0, 15.8, 0.9, 41.5, 32.0, 68.0, 1.0, 0.0, 1.46875)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the input data
std_data = scaler.transform(input_data_reshaped)
# print(std_data)

prediction = stacking_clf.predict(std_data)
# print(prediction)

if (prediction[0] == 0):
  print('This person is not a Drinker')
else:
  print('The person is a Drinker')

---
