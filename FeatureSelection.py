
import pandas as pd

def FeatureSelection(Cohort, ComorbidCondition, LabExam, VitalSign):
    '''
    This function takes the following four dataframes:
    1. Cohort: Cohort with label of ICU admission in the first day.
    2. ComorbidCondition: Patitent data of their comorbid conditions.
    3. LabExam: Patitent initial exam results within admission -3~+1 days.
    4. VitalSign: Patitent vital sign data preprocessed, recorded within admission +/- 1 day.
    
    The function outputs a dataframe of AdmissionID, Group (prediction taget, transferred into ICU or not within the first day of admission) and selected features.
    '''
    
    Dataset = Cohort[['AdmissionID', 'FirstDayICU', 'Age', 'Sex_int']]
  
    
    #Comorbid Conditions: 'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5'
    
    ComorbidConditionSelected = ComorbidCondition[['AdmissionID', 'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5']]
    
    Dataset = pd.merge(Dataset, ComorbidConditionSelected, how = 'left', on = 'AdmissionID')
    #LabExam 'LabItemA', 'LabItemB', 'LabItemC', "PathogenA"
    LabExamSelected = LabExam[['AdmissionID', 'LabItemA', 'LabItemB', 'LabItemC', "PathogenA"]]
    
    Dataset = pd.merge(Dataset, LabExamSelected, how = 'left', on = 'AdmissionID')
    
  
    
    #Vital Sign ['Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN'
    VitalSignSelected = VitalSign[['AdmissionID', 'Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN']]
    
    Dataset = pd.merge(Dataset, VitalSignSelected, how = 'left', on = 'AdmissionID')    
    
    
    return Dataset
