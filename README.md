# Predict the Need for ICU Admission for Patients with SpecificDisease

The aim of this repository is to provide a workflow demo of training machine learning models for clinical decision support, from data cleansing, exploratory analysis to model training and result comparison. The code here utilizes randomly generated electronic health records (EHRs). The workflow was applied on pediatric pneumonia patient risk evaluation, achieving an AuROC of .99 on the task of evaluation need for intensive care. The results and detailed methodologies were published on JMIR Medical Informatics (Liu et al., 2022).

Below is a summary of files in this projects:

0. __**ProjectWalkThrough**__: Slides presenting the project objectives, exploratory analyais and model comparison results.
1. __**GenerateData**__: Generate the data needed for the demo, including patient admission record, ICD codebook, demographic data, discharge diagnosis, lab exam data and vital signs.                          This project makes use of self-generated data to avoid privacy issue of real-world data.
2. __**Libraries**__: A library containing preprocessing or ETL scripts used in the project.
3. __**CohortSelection**__: Used to choose the patients with SpecificDisease for the evaluation of the need for ICU Admission.
4. __**ComorbidityConditions**__: The script utilizes discharge diagnosis code of patients and categorize them into 5 comorbid conditions.
5. __**Labata**__: Extract and preprocess clinically relevant lab data, or bio-chemical exam, results.
6. __**VitalSign**__: Extract and preprocess vital signs (e.g. body temperature, blood pressure and pulse) for model buildup.
7. __**FeatureSelection**__: Choose relevant features to create dataset for model buildup.
8. __**ModelComparison**__: Compare the performances of different families of machine learning algorithms with overall accuracy, precision, recall, F1 Score and area the under receiver operation characteristic curve.

 Check also __<ins>my blog post</ins>__ (https://halfmoonliu.github.io/posts/evaluate-intensive-care-needs-with-ml-link/) for more detailed description!

**Reference**
Liu Y-C, Cheng H-Y, Chang T-H et al. Evaluation of the need for intensive care in children with pneumonia: A machine learning approach. JMIR Medical Informatics. 2022;10(1). doi:10.2196/28934.
