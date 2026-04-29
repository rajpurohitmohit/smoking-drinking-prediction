# Aura Health Analyzer (Smoking & Drinking Predictor)

An end-to-end Machine Learning web application that predicts whether an individual is a drinker based on advanced biochemical markers and vitals.

## 🚀 Features
- **Machine Learning**: Stacking Classifier ensemble (Random Forest, Gradient Boosting, XGBoost, Logistic Regression, SVC) achieving robust accuracy.
- **FastAPI Backend**: High-performance, async Python API serving the model with strict data validation.
- **UI-UX Pro Max Frontend**: Stunning, interactive glassmorphism dashboard built with React, Vite, Tailwind CSS, and Framer Motion.

## 🛠️ Tech Stack
- **Frontend**: React.js, Vite, Tailwind CSS, Framer Motion, Lucide React
- **Backend**: Python, FastAPI, Pydantic, Uvicorn
- **Machine Learning**: Scikit-Learn, XGBoost, Pandas, Numpy, Joblib

## 💻 Running Locally

### 1. Start the Backend API
Navigate to the `backend` directory and start the FastAPI server:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will be running at `http://127.0.0.1:8000`. You can view the automatic Swagger documentation at `http://127.0.0.1:8000/docs`.

### 2. Start the Frontend Dashboard
Navigate to the `frontend` directory and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
The beautiful dashboard will be running at `http://localhost:5173`.

## 📦 Deployment
- The **Backend** is containerized via Docker and can be easily deployed to Render or Railway.
- The **Frontend** is optimized for immediate deployment on Vercel or Netlify.
