# Predict the Need for ICU Admission for Patients with SpecificDisease

In this repository, we will walk through a woking demo for predicting the need for ICU transfer of patients with SpecificDisease within the first 24 hours of admission.

Below is a summary of files in this projects:

0. __**ProjectWalkThrough**__: Slides presenting the project objectives, exploratory analyais and model comparison results.
1. __**GenerateData**__: Generate the data needed for the demo, including patient admission record, ICD codebook, demographic data, discharge diagnosis, lab exam data and vital signs.                          This project makes use of self-generated data to avoid privacy issue of real-world data.
2. __**Libraries**__: A library containing preprocessing or ETL scripts used in the project.
3. __**CohortSelection**__: Used to choose the patients with SpecificDisease for the evaluation of the need for ICU Admission.
4. __**ComorbidityConditions**__: The script utilizes discharge diagnosis code of patients and categorize them into 5 comorbid conditions.
5. __**Labata**__: Extract and preprocess clinically relavent lab data, or bio-chemical exam, results.
6. __**VitalSign**__: Extract and preprocess vital signs (e.g. body temperature, blood pressure and pulse) for model buildup.
7. __**FeatureSelection**__: Choose relevant features to create dataset for model buildup.
8. __**ModelComparison**__: Compare the performances of diffrent family of machine learning algorithms with common indices, such as overall acuracy, precision, recall, F1 Score and area the under receivor operation characteristic curve.

 Check also my website(https://halfmoonliu.github.io/posts/evaluate-intensive-care-needs-with-ml-link/) for more detailed description!
