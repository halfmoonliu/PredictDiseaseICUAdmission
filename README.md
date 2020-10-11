# Predict the Need of ICU Admission for Patients with Specific Disease

In this directory, we will walk through a woking demo for predicting the need for ICU admission within the first 24 hours of admission.

Below are the main scripts used in the project.

1. __**Data Set Generation**__: Generate the data needed for the demo. This project makes use of self-generated data to avoid privacy issue of real-world data.
2. __**Preprocessing**__: A library containing preprocessing scripts which is used across settings.
3. __**Cohort Selection**__: Used to choose the predefined group of patients for ICU Admission evaluation.
4. __**Underlying Disease**__: The script utilizes discharge diagnosis code of patients and categorize them into 15 underllying, or long-term comorbid disease.
5. __**Lab data**__: Extract and preprocess clinically relavent lab data, or bio-chemical test, results.
6. __**Feature Selection**__: Choose relevant features to create dataset for model buildup.
7. __**Model Performance Evaluation**__: Compare the performance of diffrent family of machine learning algorithms with common indices, such as overall acuracy, precision, recall, F1 Score and area under receivor operation curve.
