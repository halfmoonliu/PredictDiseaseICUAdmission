# Predict the Need for ICU Admission for Patients with Specific Disease (Under construction)

In this directory, we will walk through a woking demo for predicting the need for ICU admission within the first 24 hours of admission.

Below are the main scripts used in the project:

1. __**GenerateData**__: Generate the data needed for the demo, including patient admission record, ICD codebook, demographic data, discharge diagnosis, Exam data and vital signs.                          This project makes use of self-generated data to avoid privacy issue of real-world data.
2. __**Libraries**__: A library containing preprocessing or ETL scripts which is used across settings.
3. __**CohortSelection**__: Used to choose the predefined group of patients for ICU Admission evaluation.
4. __**ComorbidityConditions**__: The script utilizes discharge diagnosis code of patients and categorize them into 5 underllying, or long-term comorbid diseases.
5. __**Labdata**__: Extract and preprocess clinically relavent lab data, or bio-chemical test, results.
6. __**VitalSign**__: Extract and preprocess vital signs (e.g. body temperature, blood pressure and pulse) for model buildup.
7. __**Feature Selection**__: Choose relevant features to create dataset for model buildup.
8. __**Model Performance Evaluation**__: Compare the performance of diffrent family of machine learning algorithms with common indices, such as overall acuracy, precision, recall, F1 Score and area under receivor operation curve.
