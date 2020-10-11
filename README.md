# Predict Patients With Specific Disease ICU Admission Need

In this directory, we will walk through a woking demo for predicting the need for ICU admission within the first 24 hours of admission.

There are five main scripts in the directory.

1. Data Generation: Generate the data needed for the demo. This project makes use of self generated data to avoid privacy issue of real-world data.
2. Preprocessing: A library containing preprocessing scripts which is used across settings.
3. Cohort Selection: Used to choose the predefined group of patients for ICU Admission evaluation.
4. Underlying Disease: The script utilizes discharge diagnosis code of patients and categorize them into 15 underllying, or long-term comorbid disease.
5. Lab data: Extract and preprocess clinically relavent lab data, or bio-chemical test, results.
6. Feature Selection: Choose relevant features to create dataset for model buildup.
7. Model Performance Evaluation: Compare the performance of diffrent family of machine learning algorithms with common indices, such as overall acuracy, precision, recall, F1 Score and area under receivor operation curve.
