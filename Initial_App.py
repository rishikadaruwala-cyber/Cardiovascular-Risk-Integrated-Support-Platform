#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import joblib
import pandas as pd

# Load presaved model from athena's code
@st.cache_resource
def load_model():
    return joblib.load("logreg_model.pkl")

model = load_model()

st.title("10-Year CHD Risk Calculator")
st.write("Enter patient information below to estimate the probability of developing coronary heart disease within 10 years.")

# defining the input fields
male = st.selectbox("Sex", ["Female", "Male"])
male = 1 if male == "Male" else 0

age = st.number_input("Age (years)", min_value=20, max_value=100, value=50)

education = st.selectbox("Education Level (1–4)", [1, 2, 3, 4])

currentSmoker = st.selectbox("Current Smoker?", ["No", "Yes"])
currentSmoker = 1 if currentSmoker == "Yes" else 0

cigsPerDay = st.number_input("Cigarettes per Day", min_value=0, max_value=70, value=0)

BPMeds = st.selectbox("On BP Medications?", ["No", "Yes"])
BPMeds = 1 if BPMeds == "Yes" else 0

prevalentStroke = st.selectbox("History of Stroke?", ["No", "Yes"])
prevalentStroke = 1 if prevalentStroke == "Yes" else 0

prevalentHyp = st.selectbox("Hypertension Diagnosed?", ["No", "Yes"])
prevalentHyp = 1 if prevalentHyp == "Yes" else 0

diabetes = st.selectbox("Diabetes?", ["No", "Yes"])
diabetes = 1 if diabetes == "Yes" else 0

totChol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=700, value=200)
sysBP = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=300, value=120)
diaBP = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80)
BMI = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
heartRate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=70)
glucose = st.number_input("Glucose (mg/dL)", min_value=40, max_value=400, value=90)

# building a 1 row df for predicting one specific patient
input_df = pd.DataFrame({
    "male": [male],
    "age": [age],
    "education": [education],
    "currentSmoker": [currentSmoker],
    "cigsPerDay": [cigsPerDay],
    "BPMeds": [BPMeds],
    "prevalentStroke": [prevalentStroke],
    "prevalentHyp": [prevalentHyp],
    "diabetes": [diabetes],
    "totChol": [totChol],
    "sysBP": [sysBP],
    "diaBP": [diaBP],
    "BMI": [BMI],
    "heartRate": [heartRate],
    "glucose": [glucose]
})

# predict the risk
if st.button("Predict 10-Year CHD Risk"):
    prob = model.predict_proba(input_df)[0, 1]  # probability of CHD = 1
    risk_percent = prob * 100

    st.subheader("Estimated CHD Risk:")
    st.metric("10-Year CHD Probability", f"{risk_percent:.1f}%")

