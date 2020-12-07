#import libraries here
import datetime
import dateutil
import math
import numpy as np
import pandas as pd
import random
import string
import time



def GenerateDate(start, end):
    """Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formateed in the following format:
    'M(M)/D(D)/yyyy"
    , giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
 
    formatDate =  '%m/%d/%Y'

    StartDate = time.mktime(time.strptime(start, formatDate))
    EndDate = time.mktime(time.strptime(end, formatDate))

    ptime = StartDate + random.random() * (EndDate - StartDate)

    return time.strftime(formatDate, time.localtime(ptime))

def GenerateDateTime(start, end):
    """Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formateed in the following format:
    'M(M)/D(D)/yyyy h(h):m(m):s(s)"
    , giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    

    
    formatDateTime =  '%m/%d/%Y %H:%M:%S'

    stime = time.mktime(time.strptime(start, formatDateTime))
    etime = time.mktime(time.strptime(end, formatDateTime))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(formatDateTime, time.localtime(ptime))

#ExampleDateTime = GenerateDateTime("12/31/2008 16:3:2", "8/15/2010 4:5:56")

def GeneratePseudoICDDiseaseGroup(NumICD, NumComorbid):
    '''
    NumComorbid <=10
    '''
    #Generate Comorbid Condition Probability
    if NumComorbid > 10:
        print("NumComorbid should be less or equal to 10")
        return None
    
    DiseaseGroup_list = list()
    DiseaseProb_list = list()
    DiseaseProb_Total = 0
    
    for ind in range(NumComorbid):
        DiseaseGroup_list.append('CormorbidCondition'+str(ind+1))
        ComorbidProb = random.randint(1, 5)*0.01
        DiseaseProb_list.append(ComorbidProb)
        DiseaseProb_Total += ComorbidProb
   
    #Specific Disease
    SpecificDiseaseProb = random.randint(1, 5)*0.03
    DiseaseProb_Total += SpecificDiseaseProb
    DiseaseGroup_list.append('SpecificDisease')
    DiseaseProb_list.append(ComorbidProb)
    
    DiseaseGroup_list.append("Others")
    DiseaseProb_list.append(1-DiseaseProb_Total)
    

    
    DiagnosisMap_list = list()
    #Generate ICD
    Counter = 0
    while Counter < NumICD:
        Letter = random.choice(string.ascii_uppercase)
        BeforeDec = random.randint(0, 99)
        AfterDec = random.randint(0, 99)
        if AfterDec < 10:
            PseudoICD = Letter + str(BeforeDec) + ".0" + str(AfterDec)
        else:
            PseudoICD = Letter + str(BeforeDec) + "." + str(AfterDec)

        DiseaseGroup = random.choices(DiseaseGroup_list, DiseaseProb_list, k=1)
        DiagnosisMap_list.append([PseudoICD, DiseaseGroup[0]])
        Counter +=1
    ICDCodebook_df = pd.DataFrame(DiagnosisMap_list, columns = ['PseudoICD', 'DiseaseGroup'])
    return ICDCodebook_df

#ICDCodebook = GeneratePseudoICDDiseaseGroup(1000,10)
#ICDCodebook.head()
    

def GenerateVitalSign(item, age):
    if item == "Temperature":
        return round(random.uniform(35, 40), 1)
    elif item == "Pulse":
        if age < 1:
            return random.randint(65, 140)
        elif age < 4:
            return random.randint(70, 140)    
        elif age < 6:
            return random.randint(70, 125)            
        elif age < 10:
            return random.randint(65, 125)                    
        elif age < 14:
            return random.randint(55, 120)                    
        else:
            return random.randint(45, 110)                            
    elif item == "Systolic Pressure":
        if age < 1:
            return random.randint(65, 110)
        elif age < 3:
            return random.randint(80, 115)    
        elif age < 12:
            return random.randint(90, 125)                            
        else:
            return random.randint(100, 150)                
    elif item == "Diastolic Pressure":
        if age < 1:
            return random.randint(40, 70)
        elif age < 3:
            return random.randint(50, 80)    
        elif age < 12:
            return random.randint(50, 90)                            
        else:
            return random.randint(55, 100)        
    elif item == "Breath Rate":
        if age < 1:
            return random.randint(20, 60)
        elif age < 3:
            return random.randint(15, 35)    
        elif age < 12:
            return random.randint(12, 27)                            
        else:
            return random.randint(9, 30)                
    elif item == "SpO2":        
        return random.randint(90, 100)                
    else:
        return "No such vital sign. Please check spelling."
    
def GenerateExam(item, age):
    if item == "LabItemA":
        return round(random.uniform(0, 2), 1)
    elif item == "LabItemB":
        if age < 6:
            return round(random.uniform(3, 18), 2)
        elif age < 18:
            return round(random.uniform(2, 15), 2)
        else:
            return round(random.uniform(2, 13), 2)       
    elif item == "LabItemC":    
        return random.randint(120, 160)
    elif item == "Pathogen Isolation":    
        ind = random.randint(1, 10)
        if ind % 10 == 0:
            return "Pathogen Isolation: Pathogen" + random.choice(string.ascii_uppercase)
        elif ind == 99:
            return string.punctuation + string.punctuation + string.punctuation
        else:
            return "No Pathogen Isolated"
    elif item == "Pathogen A Sreening":    
        ind = random.randint(1, 100)
        if ind %10 == 0:            
            return "Positive"
        elif ind == 99:
            return string.punctuation + string.punctuation + string.punctuation            
        else:
            return "Negative"
    elif item == "Others":    
        ResultType = random.randint(1, 100)
        if ResultType % 2 == 0:
            return round(random.uniform(0, 100), 2)        
        else:
            ResultLength = ResultType % 7

            result = ""
            for wordind in range(ResultLength):
                WordLength = random.randint(1, 6)
                word = ""
                for letter in range(WordLength):
                    word += random.choice(string.ascii_uppercase)

                if wordind != ResultLength:
                    word += string.whitespace[0]


                result += word

            return result
    else:
        return "Exam name not found. Please check spelling."    
    
def GenerateDataset(Num, StartBirthDate, EndBirthDate, AdmStartDateTime, AdmEndDateTime):
  
    #The function returns a pandas dataframe Num of data with     
    #Num Number of admission data generated from the function, limited to 1 to 999,999.
    Counter = 1
    Demographics_list = list()
    DischargeDiagnosis_list = list()
    ICURecord_list = list()
    VitalSign_list = list()
    Exam_list = list()
    ICDCodeBook = GeneratePseudoICDDiseaseGroup(1000,5)
    All_DiagnosisCode_list = ICDCodeBook['PseudoICD'].tolist()
    while Counter <= Num:


       
        #Demographics
        
        DemographicsRow_list = list()        
        
        #AdmissionID
        NoDigit = int(math.log10(Num))+1 
        AdmissionID = 'Adm'+(NoDigit-int(math.log10(Counter)))*'0'+str(Counter)
        if Counter %500 ==0:
            print("Start fabricating data of " + AdmissionID +"...")
        DemographicsRow_list.append(AdmissionID)
        #Sex: 1 indicates male, 0 indicates female
        DemographicsRow_list.append(str(random.randint(0, 1)))
        #Birthdate
        Birthdate = GenerateDate(StartBirthDate, EndBirthDate)
        DemographicsRow_list.append(Birthdate)
        #AdmissionDateTime
        AdmissionDateTime = GenerateDateTime(AdmStartDateTime, AdmEndDateTime)

        DemographicsRow_list.append(AdmissionDateTime)
        #InHospitalDays & DischargeDateTime
        InHospitalDays = random.randrange(1, 30)       
        #DischargeDateTime
        DischargeDateTime = datetime.datetime(*time.strptime(time.strftime(AdmissionDateTime), '%m/%d/%Y %H:%M:%S')[:6])+ datetime.timedelta(days = InHospitalDays, hours = int(random.random()*60), seconds = int(random.random()*60))

        DischargeDateTime = time.strftime('%m/%d/%Y %H:%M:%S', DischargeDateTime.timetuple())
        
        DemographicsRow_list.append(DischargeDateTime)
        #Transfer
        DemographicsRow_list.append(InHospitalDays)

        
        Demographics_list.append(DemographicsRow_list)

        #Dischage Diagnosis
        DischargeDiagnosisAdm_list = [AdmissionID]
        
        NumDiagAdm = random.randint(1, 10)
        for DianosisInd in range(NumDiagAdm):
            DischargeDiagnosisAdm_list.append(random.choice(All_DiagnosisCode_list))
        for DianosisSpanceInd in range(10-NumDiagAdm):
            DischargeDiagnosisAdm_list.append("-")
        DischargeDiagnosis_list.append(DischargeDiagnosisAdm_list)
        
        #ICU Record
        ICU_TXR_Times_list = [0, 1, 2, 3, 4]
        ICU_TXR_Times_Prob_list = [0.7, 0.2, 0.05, 0.01, 0.01]
        ICU_TXR_Times = random.choices(ICU_TXR_Times_list, ICU_TXR_Times_Prob_list, k=1)

        

        LatestInICUTime = AdmissionDateTime

        LatestOutICUTime = AdmissionDateTime
        FirstICU = True
        for ICURecordInd in range(ICU_TXR_Times[0]):
            
            Prob_ICU24H = random.randint(0, 6)
            if Prob_ICU24H != 0 and FirstICU == True:
                AdmissionPlus24H = datetime.datetime(*time.strptime(time.strftime(AdmissionDateTime), '%m/%d/%Y %H:%M:%S')[:6])+ datetime.timedelta(days = 1, hours = int(random.random()*60), seconds = int(random.random()*60))
                AdmissionPlus24H = time.strftime('%m/%d/%Y %H:%M:%S', AdmissionPlus24H.timetuple())
                LatestInICUTime = GenerateDateTime(LatestOutICUTime, AdmissionPlus24H)
                LatestOutICUTime = GenerateDateTime(LatestInICUTime, DischargeDateTime)
                FirstICU == False
            elif Prob_ICU24H == 0 and FirstICU == True:
                LatestInICUTime = GenerateDateTime(LatestOutICUTime, DischargeDateTime)
                LatestOutICUTime = GenerateDateTime(LatestInICUTime, DischargeDateTime)
                FirstICU == False                
            else:
                LatestInICUTime = GenerateDateTime(LatestOutICUTime, DischargeDateTime)
                LatestOutICUTime = GenerateDateTime(LatestInICUTime, DischargeDateTime)
            LatestOutICUTime = GenerateDateTime(LatestInICUTime, DischargeDateTime)
            ICURecord_list.append([AdmissionID, LatestInICUTime, LatestOutICUTime])
            
        #Vital Sign
        VitalSignTimePoint = AdmissionDateTime
        VitalSignTimeDif = -1 #minus one day before admission
        while VitalSignTimeDif < InHospitalDays:
            VitalSignTimeDif += random.uniform(0.3, 0.4)
            VitalSignTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int(VitalSignTimeDif*24*60*60))
            Recorded_Age = (dateutil.relativedelta.relativedelta(datetime.datetime.strptime(Birthdate, '%m/%d/%Y'), VitalSignTimePoint).days)/365.25
            
            
            VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'Temperature', GenerateVitalSign('Temperature', Recorded_Age)])
            
            VitalSignTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int((VitalSignTimeDif+random.randint(5, 180))*24*60*60+random.randint(5, 180))) 
            
            VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'Breath Rate', GenerateVitalSign('Breath Rate', Recorded_Age)])
            VitalSignTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int((VitalSignTimeDif+random.randint(5, 180))*24*60*60+random.randint(5, 180)))             
            VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'Pulse', GenerateVitalSign('Pulse', Recorded_Age)])
            
            if int(VitalSignTimeDif*10)%10%3 == 0:#measure 3 times a day
                VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'Systolic Pressure', GenerateVitalSign('Systolic Pressure', Recorded_Age)])
                VitalSignTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int((VitalSignTimeDif+random.randint(5, 180))*24*60*60+random.randint(5, 180))) 
                VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'Diastolic Pressure', GenerateVitalSign('Diastolic Pressure', Recorded_Age)])
                VitalSignTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int((VitalSignTimeDif+random.randint(5, 180))*24*60*60+random.randint(5, 180))) 
                VitalSign_list.append([AdmissionID, VitalSignTimePoint, 'SpO2', GenerateVitalSign('SpO2', Recorded_Age)])            
            
        #Exam
        ExamTimePoint = AdmissionDateTime
        ExamTimeDif = -3 #minus one day before admission
        while ExamTimeDif < InHospitalDays:
            ExamTimeDif += random.uniform(0.9, 1.2)
            
            ExamTimePoint = datetime.datetime.strptime(AdmissionDateTime, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(seconds = int(ExamTimeDif*24*60*60))
            Sampling_Age = (dateutil.relativedelta.relativedelta(datetime.datetime.strptime(Birthdate, '%m/%d/%Y'), ExamTimePoint).days)/365.25            

            if (ExamTimeDif < 3 and int((ExamTimeDif*10)%10%3) == 0) or int((ExamTimeDif*10)%10%7) == 0:
                
                
                TypeDice = random.randint(0, 4)
                if TypeDice == 0:
                    Exam_list.append([AdmissionID, ExamTimePoint, 'Pathogen A Sreening', GenerateExam('Pathogen A Sreening', Sampling_Age)])
                
                else:
                    Exam_list.append([AdmissionID, ExamTimePoint, 'Pathogen Isolation', GenerateExam('Pathogen Isolation', Sampling_Age)])

            if int((ExamTimeDif*10)%10%3) == 1:                    
                Exam_list.append([AdmissionID, ExamTimePoint, 'LabItemA', GenerateExam('LabItemA', Sampling_Age)])
                Exam_list.append([AdmissionID, ExamTimePoint, 'LabItemB', GenerateExam('LabItemB', Sampling_Age)])
                Exam_list.append([AdmissionID, ExamTimePoint, 'LabItemC', GenerateExam('LabItemC', Sampling_Age)])
            if int((ExamTimeDif*10)%10%4) == 0:                                    
                Exam_list.append([AdmissionID, ExamTimePoint, 'Others', GenerateExam('Others', Sampling_Age)])
                
           
            
        Counter +=1
                                   
    Demographics_df = pd.DataFrame(Demographics_list, columns = ['AdmissionID', 'Sex_int', 'Birthdate', 'AdmissionDateTime', 'DischargeDateTime', 'InHospitalDays'])                              
    DischargeDiagnosis_df = pd.DataFrame(DischargeDiagnosis_list, columns = ['AdmissionID','DiagnosisCode0', 'DiagnosisCode1', 'DiagnosisCode2', 'DiagnosisCode3', 'DiagnosisCode4', 'DiagnosisCode5', 'DiagnosisCode6', 'DiagnosisCode7', 'DiagnosisCode8', 'DiagnosisCode9'])
    ICURecord_df = pd.DataFrame(ICURecord_list, columns = ['AdmissionID', 'InICUDatetime', 'OutICUDateTime'])
    VitalSign_df = pd.DataFrame(VitalSign_list, columns = ['AdmissionID', 'RecordDateTime', 'VitalSignType', 'VitalSignValue'])
    Exam_df = pd.DataFrame(Exam_list, columns = ['AdmissionID', 'ReportDateTime', 'ExamType', 'ExamResult'])
    return Demographics_df, DischargeDiagnosis_df, ICURecord_df, VitalSign_df, Exam_df, ICDCodeBook                                           
#Demographics_raw , DischargeDiagnosis_raw, ICURecord_raw, VitalSign_df, Exam_df, ICDCodeBook = GenerateDataset(50, "1/1/1982", "12/31/2000", "1/1/2000 00:00:00", "12/31/2010 23:59:59")
#Demographics_raw.head()                                        
