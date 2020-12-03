#import libraries here
import pandas as pd
import GenerateData





def CombineFinalDiagnosis(DiagnosisDataFrame):

    
    print("Hi, welcome to the routine.")
    print("This routine aims at combining all final diagnoses")




    Diagnosis_All = DischargeDiagnosis_raw[['AdmissionID','DiagnosisCode0', 'DiagnosisCode1', 'DiagnosisCode2', 'DiagnosisCode3',
                                            'DiagnosisCode4', 'DiagnosisCode5', 'DiagnosisCode6', 'DiagnosisCode7', 'DiagnosisCode8', 'DiagnosisCode9']]

    print("Done. Start stacking diagnosis results..")

    list_out_diagnosis = []
    Diagnosis_Stacked = pd.DataFrame(columns=['AdmissionID', 'DiagnosisOrder', 'DiagnosisCode' ])

    #Extract each diagnosis as seperate dataframe and concatenate all dataframes.
    for i in range(10): #total of 10 diagnosis(maximum, rangning from 0 to 9)
        
        clmn_temp = 'DiagnosisCode'+str(i)
        list_out_diagnosis.append(clmn_temp)
   
        df_temp = Diagnosis_All[['AdmissionID','DiagnosisCode'+str(i)]]
        df_temp['DiagnosisOrder'] = i
        df_temp = df_temp[['AdmissionID','DiagnosisOrder', 'DiagnosisCode'+str(i)]]
        df_temp.columns = ['AdmissionID', 'DiagnosisOrder', 'DiagnosisCode' ]
        Diagnosis_Stacked = pd.concat([Diagnosis_Stacked, df_temp])
        Diagnosis_Stacked['DiagnosisCode'].replace('', np.nan, inplace=True)#Replace space with Null


        Diagnosis_Stacked= Diagnosis_Stacked.dropna(subset=['DiagnosisCode'])#Drop Null value

    return Diagnosis_Stacked

DiagnosisStacked = CombineFinalDiagnosis(DischargeDiagnosis_raw)

print(DiagnosisStacked.head(10))
