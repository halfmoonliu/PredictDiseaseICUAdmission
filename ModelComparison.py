import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import torch 
import xgboost as xgb


def ModelComparison(Dataset):
    '''
    This function takes a dataset with predtion target and selected features and compare the performance with the following models:
    1. K-Nearest Neighbors
    2. Support Vector Machines
    3. Logistic Regresion, 
    4. Feedforward Neural Network
    5. Random Forest
    6. XGBoost
    '''

    print("Hello, welcome to this routine.")
    print("This routine aims at comparing model performance with ROC curves...")
    

    Dataset_df = Dataset
    def GroupInt(text):
        if text == 'Y':
            return 1
        else: 
            return 0
    Dataset_df['Group'] = Dataset['FirstDayICU'].apply(GroupInt)


    Dataset_df = Dataset_df[['AdmissionID', 'Group',
                   
                   'Age', 'Sex_int',
                   #ComorbidConditions
                   'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5',
                   #Pathogen
                   'PathogenA',
                   #LabData
                   'LabItemA', 'LabItemB', 'LabItemC',
                   #VitalSign
                   'Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN']]
    
    print("Start replacing missing values with zeros for categorical data, such as pathogens...")
    MissingListCat = ['ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5', 'PathogenA']

    for item_cat in MissingListCat:
        Dataset_df[item_cat].replace(np.nan, 0, inplace=True)

    print("Start replacing missing values with medians for lab data and vital signs...")
    MissingListVal = ['LabItemA', 'LabItemB', 'LabItemC', 'Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN']
    
    for item_val in MissingListVal:
        AdmissionID_Item_Val = Dataset[['AdmissionID', item_val]]
        AdmissionID_Item_Val = AdmissionID_Item_Val.dropna(subset=[item_val])
        ItemMedian =  AdmissionID_Item_Val[item_val].median()
        Dataset_df[item_val].fillna(ItemMedian, inplace = True) 

    feature_cols = ['Age', 'Sex_int',
                   #ComorbidConditions
                   'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5',
                   #Pathogen
                   'PathogenA',
                   #LabData
                   'LabItemA', 'LabItemB', 'LabItemC',
                   #VitalSign
                   'Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN'] 


    X = Dataset_df[feature_cols] # Features
    y = Dataset_df.Group # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


    scale_Standard = StandardScaler() 


    X_train_scale_Standard = scale_Standard.fit_transform(X_train)
    X_test_scale_Standard = scale_Standard.fit_transform(X_test)

    #KNN

    Model_KNN = KNeighborsClassifier(n_neighbors = 5)
    Model_KNN.fit(X_train_scale_Standard,y_train)

    y_pred_KNN = Model_KNN.predict(X_test_scale_Standard)
    y_pred_KNN_prob = Model_KNN.predict_proba(X_test_scale_Standard)[:,1]
    
    print("Accuracy_test_KNN:" + str(round(metrics.accuracy_score(y_test, y_pred_KNN), 3)))
    print("Precision_test_KNN:" +  str(round(metrics.precision_score(y_test, y_pred_KNN), 3)))
    print("Recall_test_KNN:" + str(round(metrics.recall_score(y_test, y_pred_KNN), 3)))
    print("F1 Score_test_KNN:" + str(round(metrics.f1_score(y_test,y_pred_KNN), 3)))

    #SVM

    Model_SVM = SVC(C = 1, probability = True, kernel='linear')
    Model_SVM.fit(X_train, y_train)

    y_pred_SVM = Model_SVM.predict(X_test)
    y_pred_SVM_prob = Model_SVM.predict_proba(X_test)[:,1]

    print("Accuracy_test_SVM:" + str(round(metrics.accuracy_score(y_test, y_pred_SVM), 3)))
    print("Precision_test_SVM:" +  str(round(metrics.precision_score(y_test, y_pred_SVM), 3)))
    print("Recall_test_SVM:" + str(round(metrics.recall_score(y_test, y_pred_SVM), 3)))
    print("F1 Score_test_SVM:" + str(round(metrics.f1_score(y_test,y_pred_SVM), 3)))

    
    #Logistic Regression

    Model_LogReg = LogisticRegression(penalty = 'l2')
    Model_LogReg.fit(X_train, y_train)

    y_pred_LogReg= Model_LogReg.predict(X_test)
    y_pred_LogReg_prob = Model_LogReg.predict_proba(X_test)[:,1]

    print("Accuracy_test_LogReg:" + str(round(metrics.accuracy_score(y_test, y_pred_LogReg), 3)))
    print("Precision_test_LogReg:" +  str(round(metrics.precision_score(y_test, y_pred_LogReg), 3)))
    print("Recall_test_LogReg:" + str(round(metrics.recall_score(y_test, y_pred_LogReg), 3)))
    print("F1 Score_test_LogReg:" + str(round(metrics.f1_score(y_test,y_pred_LogReg), 3)))


    class Feedforward(torch.nn.Module):
            def __init__(self, input_size, hidden_size1, hidden_size2):
                super(Feedforward, self).__init__()
                self.input_size = input_size
                self.hidden_size1  = hidden_size1
                self.hidden_size2  = hidden_size2
                self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size1)
                self.relu = torch.nn.ReLU()
                self.fc2 = torch.nn.Linear(self.hidden_size1, self.hidden_size2)
                self.relu = torch.nn.ReLU()
                self.fc3 = torch.nn.Linear(self.hidden_size2, 1)
                self.sigmoid = torch.nn.Sigmoid()
            def forward(self, x):
                hidden1 = self.fc1(x)
                relu1 = self.relu(hidden1)
                hidden2 = self.fc2(relu1)
                relu2 = self.relu(hidden2)
                output = self.fc3(relu2)
                output = self.sigmoid(output)
                return output



    X_train_Tensor = torch.FloatTensor(X_train.values)
    y_train_Tensor = torch.FloatTensor(y_train.values)

    X_test_Tensor = torch.FloatTensor(X_test.values)
    y_test_Tensor = torch.FloatTensor(y_test.values)



    model = Feedforward(15, 3, 3)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr = 0.01)


    model.train()   
    epoch = 100
    for epoch in range(epoch):
        optimizer.zero_grad()
        # Forward pass
        y_pred_train = model(X_train_Tensor)
        # Compute Loss
        loss = criterion(y_pred_train.squeeze(), y_train_Tensor)
        #if epoch % 20 == 0:
   
        #    print('Epoch {}: train loss: {}'.format(epoch, loss.item()))
        # Backward pass
        loss.backward()
        optimizer.step()



    y_pred_NeuralNet_prob = model(X_test_Tensor)
    y_pred_NeuralNet = torch.round(y_pred_NeuralNet_prob)

    y_pred_NeuralNet_prob  = y_pred_NeuralNet_prob.detach().numpy()
    y_pred_NeuralNet_np  = y_pred_NeuralNet.detach().numpy()

    print("Accuracy_test_NN:" + str(round(metrics.accuracy_score(y_test, y_pred_NeuralNet_np), 3)))
    print("Precision_test_NN:" +  str(round(metrics.precision_score(y_test, y_pred_NeuralNet_np), 3)))
    print("Recall_test_NN:" + str(round(metrics.recall_score(y_test, y_pred_NeuralNet_np), 3)))
    print("F1 Score_test_NN:" + str(round(metrics.f1_score(y_test, y_pred_NeuralNet_np), 3)))


    #Random Forest
    Model_RandomForest = RandomForestClassifier(n_estimators = 50, criterion = "gini")
    Model_RandomForest.fit(X_train, y_train)
    y_pred_RandomForest = Model_RandomForest.predict(X_test)
    y_pred_RandomForest_prob = Model_RandomForest.predict_proba(X_test)[:,1]
    
    print("Accuracy_test_RF:" + str(round(metrics.accuracy_score(y_test, y_pred_RandomForest), 3)))
    print("Precision_test_RF:" +  str(round(metrics.precision_score(y_test, y_pred_RandomForest), 3)))
    print("Recall_test_RF:" + str(round(metrics.recall_score(y_test, y_pred_RandomForest), 3)))
    print("F1 Score_test_RF:" + str(round(metrics.f1_score(y_test, y_pred_RandomForest), 3)))
    
        
    #XGBoost
    Model_XGBoost =xgb.XGBClassifier(max_depth= 3, learning_rate= 0.4, verbosity = 0, objective = 'binary:logistic')
    Model_XGBoost.fit(X_train, y_train,eval_metric = 'auc',  verbose = None)
    y_pred_XGBoost = Model_XGBoost.predict(X_test)
  
    print("Accuracy_test_XGB:" + str(round(metrics.accuracy_score(y_test,y_pred_XGBoost), 3)))
    print("Precision_test_XGB:" +  str(round(metrics.precision_score(y_test,y_pred_XGBoost), 3)))
    print("Recall_test_XGB:" + str(round(metrics.recall_score(y_test, y_pred_XGBoost), 3)))
    print("F1 Score_test_XGB:" + str(round(metrics.f1_score(y_test,y_pred_XGBoost), 3)))
    
    y_pred_XGBoost_prob = Model_XGBoost.predict_proba(X_test)[:,1]


    plt.figure(0).clf()
    #XGBoost
    fpr_XGBoost, tpr_XGBoost, thresh_XGBoost = metrics.roc_curve(y_test, y_pred_XGBoost_prob)
    auc_XGBoost = metrics.roc_auc_score(y_test, y_pred_XGBoost_prob)
    auc_XGBoost = round(auc_XGBoost, 2)
    plt.plot(fpr_XGBoost,tpr_XGBoost,label="XGB, AUROC = "+ str(auc_XGBoost))
    #Random Forest
    fpr_RandomForest, tpr_RandomForest, thresh_RandomForest = metrics.roc_curve(y_test, y_pred_RandomForest_prob)
    auc_RandomForest = metrics.roc_auc_score(y_test, y_pred_RandomForest_prob)
    auc_RandomForest = round(auc_RandomForest, 2)
    plt.plot(fpr_RandomForest,tpr_RandomForest,label="RF, AUROC = "+ str(auc_RandomForest))
    #Neural Net
    fpr_NeuralNet, tpr_NeuralNet, thresh_NeuralNet = metrics.roc_curve(y_test, y_pred_NeuralNet_prob)
    auc_NeuralNet = metrics.roc_auc_score(y_test, y_pred_NeuralNet_prob)
    auc_NeuralNet = round(auc_NeuralNet, 2)
    plt.plot(fpr_NeuralNet,tpr_NeuralNet,label="NN, AUROC = "+ str(auc_NeuralNet))
    #Logistic Regression
    fpr_LogReg, tpr_LogReg, thresh_LogReg = metrics.roc_curve(y_test, y_pred_LogReg_prob)
    auc_LogReg = metrics.roc_auc_score(y_test, y_pred_LogReg_prob)
    auc_LogReg = round(auc_LogReg, 2)
    plt.plot(fpr_LogReg,tpr_LogReg,label="LogReg, AUROC = "+ str(auc_LogReg))
    #SVM
    fpr_SVM, tpr_SVM, thresh_SVM = metrics.roc_curve(y_test, y_pred_SVM_prob)
    auc_SVM = metrics.roc_auc_score(y_test, y_pred_SVM_prob)
    auc_SVM = round(auc_SVM, 2)
    plt.plot(fpr_SVM,tpr_SVM,label="SVM, AUROC = "+ str(auc_SVM))
    #KNN
    fpr_KNN, tpr_KNN, thresh_KNN = metrics.roc_curve(y_test, y_pred_KNN_prob)
    auc_KNN = metrics.roc_auc_score(y_test, y_pred_KNN_prob)
    auc_KNN = round(auc_KNN, 2)
    plt.plot(fpr_KNN,tpr_KNN,label="KNN, AUROC = "+ str(auc_KNN))


    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend(loc=0)
    plt.show()


    return None
