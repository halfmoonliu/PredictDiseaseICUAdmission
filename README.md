# Predict Disease ICU Admission

In this directory, we will walk through a woking demo for predicting the need for ICU admission within the first 24 hours of admission.

There are five main scripts in the directory.

1. Data Generation: Generate the data needed for the demo. This project uses self generated data to avoid privacy issue of real-world data.
2. Preprocessing: A library containing preprocessing scripts which is used across settings.
3. Cohort Selection: Used to choose the predefined group of patients for ICU Admission evaluation.
4. Underlying Disease: The script utilizes discharge diagnosis code of patients and categorize them into 15 underllying, or long-term comorbid disease.
5. Lab data: Extract and preprocess clinically relavent lab data, or bio-chemical test, results.
