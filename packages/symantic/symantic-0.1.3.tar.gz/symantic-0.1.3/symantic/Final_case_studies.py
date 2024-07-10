#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:18:50 2024

@author: muthyala.7
"""

import pandas as pd 

import FeatureSpaceConstruction as fc
import Regressor as sr
import DimensionalFeatureSpaceConstruction as dfc
import Regressor_dimension as srd
import sys
import time
import pdb
import numpy as np 

from sympy import symbols
from sklearn.model_selection import train_test_split

class symantic_model:

  def __init__(self,df,operators=None,multi_task = None,no_of_operators=None,dimension=None,sis_features=20,device='cpu',relational_units = None,initial_screening = None,dimensionality=None,output_dim = None,regressor_screening = None,metrics=[0.06,0.995]):

    self.operators = operators
    self.df=df
    self.no_of_operators = no_of_operators
    self.device = device
    if dimension == None: self.dimension = 3#dimension
    else: self.dimension = dimension
    if sis_features == None: self.sis_features = 10
    else: self.sis_features = sis_features
    self.relational_units = relational_units
    self.initial_screening = initial_screening
    self.dimensionality = dimensionality
    self.output_dim = output_dim
    self.regressor_screening = regressor_screening
    self.metrics   = metrics
    self.multi_task = multi_task
    if multi_task!=None:
        self.multi_task_target = multi_task[0]
        self.multi_task_features = multi_task[1]
    

      
  def fit(self):
      
    if self.dimensionality == None:
        
        if self.operators==None: sys.exit('Please provide the operators set for the non dimensional Regression!!')
        
        if self.multi_task!=None:
            
            print('Performing MultiTask Symbolic regression!!..')
            
            equations =[]
            
            for i in range(len(self.multi_task_target)):
                
                #Get the target variable and feature variabls 
                print('Performing symbolic regression of',i+1,'Target variables....')
                
                list1 =[]
                
                list1.extend([self.multi_task_target[i]]+self.multi_task_features[i])
                
                df1 = self.df.iloc[:,list1]
                
                if self.no_of_operators==None:
                    
                    st = time.time()
                    
                    rmse,equation,r2 = fc.feature_space_construction(self.operators,df1,self.no_of_operators,self.device,self.initial_screening,self.metrics).feature_space()
                    
                    print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        print('Equations found::',equations)
                        return rmse,equation,r2,equations
                    else:continue
                
                else:
                    
                    x,y,names = fc.feature_space_construction(self.operators,df1,self.no_of_operators,self.device,self.initial_screening).feature_space()
                    
                    rmse, equation,r2 =  sr.Regressor(x,y,names,self.dimension,self.sis_features,self.device).regressor_fit()
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        print('Equations found::',equations)
                        return rmse, equation, r2,equations
                    else: continue
                
        elif self.no_of_operators==None:
            
            st = time.time()
            
            rmse,equation,r2 = fc.feature_space_construction(self.operators,self.df,self.no_of_operators,self.device,self.initial_screening,self.metrics).feature_space()
            
            print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
            
            return rmse,equation,r2
                
            
        else:
            
            x,y,names = fc.feature_space_construction(self.operators,self.df,self.no_of_operators,self.device,self.initial_screening).feature_space()
            
            rmse, equation,r2 =  sr.Regressor(x,y,names,self.dimension,self.sis_features,self.device).regressor_fit()
        
            return rmse, equation, r2
  
    else: 
        
        if self.multi_task!=None:
            
            print('************************************************ Performing MultiTask Symbolic regression!!..************************************************ \n')
            
            equations =[]
            
            for i in range(len(self.multi_task_target)):
                
                #Get the target variable and feature variabls 
                print('************************************************ Performing symbolic regression of',i+1,'Target variables....************************************************ \n')
                
                list1 =[]
                
                list1.extend([self.multi_task_target[i]]+self.multi_task_features[i])
                
                df1 = self.df.iloc[:,list1]
                
                if self.no_of_operators==None:
                    
                    st = time.time()
                    
                    rmse,equation,r2 = dfc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,self.metrics,self.output_dim).feature_expansion()
                    
                    print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        
                        print('Equations found::',equations)
                        
                        return rmse,equation,r2,equations
                    
                    else:continue
                
                else:
                    
                    x,y,names,dim = dfc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality).feature_expansion()
                    
                    #print(names)
                    rmse,equation,r2 = srd.Regressor(x,y,names,dim,self.dimension,self.sis_features,self.device,self.output_dim,self.regressor_screening).regressor_fit()
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        
                        print('Equations found::',equations)
                        
                        return rmse, equation, r2,equations
                    
                    else: continue
                
        if self.no_of_operators==None:
            
            st = time.time()
            
            rmse,equation,r2 = dfc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,self.metrics,self.output_dim).feature_expansion()
            
            print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
            
            return rmse,equation,r2
        
        
        else:
            
            x,y,names,dim = dfc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality).feature_expansion()
            
            #print(names)
            rmse,equation,r2 = srd.Regressor(x,y,names,dim,self.dimension,self.sis_features,self.device,self.output_dim,self.regressor_screening).regressor_fit()
            
            return rmse,equation,r2



'''


'''
####################################################################################################################


#SYNTHETIC CASE STUDIES....

#######################################################################################################################

'''


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/1/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['/','+']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators,no_of_operators=3,dimension=1).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/2/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['sin','pow(1/2)']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators,no_of_operators=3,dimension=2,sis_features=20).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')




df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/3/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['/','+','exp']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators,no_of_operators=4,dimension=1).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/4/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(2)','pow(3)'],no_of_operators=2,dimension=3,sis_features=5).fit()
print("SISSO Completed in: ",time.time()-st,'\n')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/5/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(2)','+','/','exp','-'],no_of_operators=4,dimension=1,sis_features=20).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/6/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(1/2)','pow(2)','exp','+'],no_of_operators=4,dimension=1,sis_features=5).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/7/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['exp(-1)','sin','*'],no_of_operators=3,dimension=2,sis_features=20).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/8/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(3)','pow(2)','*'],no_of_operators=3,dimension=3,sis_features=10).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/9/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
operators = ['ln','-','*','/']
rmse,equation,r2 = symantic_model(df,operators=operators,no_of_operators=4,dimension=1,sis_features=10).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/10/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
operators = ['exp(-1)','/']
rmse,equation,r2 = symantic_model(df,operators=operators,no_of_operators=4,dimension=1,sis_features=10).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')





'''
####################################################################################################################


# Real datasets of redox potential and solvation energy....

#######################################################################################################################

'''

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/padel_redox/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
start_c = time.time()
operators = ['+','-','*','/']
rmse,equation,r2 = symantic_model(df,operators=operators,metrics=[0.025,0.99],initial_screening=['spearman',0.99]).fit()

#rmse,equation,r2 = symantic_model(df,operators=operators,dimension=3,no_of_operators=3,sis_features=10,initial_screening=['spearman',0.99]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')

import matplotlib.pyplot as plt 
import matplotlib

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

import matplotlib
matplotlib.rcParams.update({# Use mathtext, not LaTeX
                            'text.usetex': False,
                            # Use the Computer modern font
                            'font.family': 'serif',
                            'font.serif': 'cmr10',
                            'mathtext.fontset': 'cm',
                            # Use ASCII minus
                            'axes.unicode_minus': False,
                            'figure.dpi' : 300,

                            })

font = {'weight' : 'bold',
        'size'   : 34}
plt.rc('font', **font)

predicted_train = 144.146766945998*((df.SpMax4_Bhm+df.MLFER_L)/(df.MW*df.MLFER_L))+0.06388827111251938

predicted_2d = -106.77303791869888*((df.MLFER_L/df.MW)/(df.SpMax4_Bhm-df.MLFER_L)) -0.25326293870328537*((df.SpMax4_Bhm-df.SpMax5_Bhm)-(df.SpMax4_Bhm/df.SpMax5_Bhm)) -0.035775314803984326

predicted_3d = 94.78148127016601*((df.SpMax4_Bhm+df.MLFER_L)/(df.MW*df.MLFER_L))   + 2330.6753717871925*((df.SpMax4_Bhm/df.MLFER_L)/(df.ATS2m+df.ZMIC0))   + 0.021322180419827048*((df.SpMax4_Bhm-df.MLFER_L)*(df.SpMax4_Bhm-df.SpMax5_Bhm))+0.19302379805499048

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

r2_train = r2_score(df.Target,predicted_train)
r2_train2 = r2_score(df.Target,predicted_2d)
r2_train3 = r2_score(df.Target,predicted_3d)
rmse_2d = mean_squared_error(df.Target,predicted_2d)
print(r2_train)

df_train_symantecs = pd.DataFrame()
df_train_symantecs['True'] = df.Target
df_train_symantecs['1D'] = predicted_train
df_train_symantecs['2D'] = predicted_2d
df_train_symantecs['3D'] = predicted_3d
df_train_symantecs.to_csv('Training_True_predictions_symantecs.csv')

plt.plot([0,2.5],[0,2.5],color="black")
plt.scatter(df.Target, predicted_train,c='green',marker='^',s=100,alpha=1.0,label=f'Train - R$^2$:{r2_train:.3f}')
#plt.scatter(df.Target, predicted_2d,c='blue',marker='o',s=100,alpha=0.7,label=f'R$^2$:{r2_train2:.3f}')
#plt.scatter(df.Target, predicted_3d,c='orange',marker='x',s=40,alpha=0.5,label=f'Train - R$^2$:{r2_train3:.3f};3-term')
plt.xlabel("DFT Specific Energy")
plt.ylabel("Predicted Specific Energy")
plt.title('Training')
plt.xlim(0,2.5)
plt.ylim(0,2.5)
#plt.legend()
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14)
plt.tick_params(axis='both', which='both', labelsize='medium')
legend = plt.legend(facecolor='lightgray', edgecolor='black')

plt.savefig('symantecs_train.png')
plt.show()

predicted_train = 1.032521911*((df.ATS3i/df.SpAD_Dzi)/(df.SpAD_Dzi*df.SpMax1_Bhm)) + 0.5533907820
predicted_2d = 8.313376203*((df.SpMin1_Bhi/df['SP-3'])/(df.SpMax1_Bhm+df.SpMax4_Bhm)) +14.85502453*((df.SpMin1_Bhi/df.SpAD_Dzi)/(df.AATS0p-df.ETA_EtaP_F_L)) + 0.2611027328
predicted_3d = 7.750974934*((df.SpMin1_Bhi/df['SP-3'])/(df.SpMax1_Bhm+df.SpMax4_Bhm)) +16.76116823*((df.SpMin1_Bhi/df.SpAD_Dzi)/(df.AATS0p-df.ETA_EtaP_F_L)) + 0.2941239911 -0.006580062660*((df.ATSC3i*df.MLFER_BO)/(df.AATS0p-df['SP-3']))

#predicted_train = 1136.307370*((df.GATS3s+df.SpMin1_Bhv)/(df.ATS2m+df.SpDiam_Dzv)) + 0.2177688647
#predicted_2d = 1107.806951*((df.GATS3s+df.SpMin1_Bhv)/(df.ATS2m+df.AATS1i)) -0.002424529527*((df.AMR+df.SpMax8_Bhi)+(df.ATSC3v/df.AATSC0v)) +0.3718966781
#predicted_3d = 1090.173976*((df.GATS3s+df.SpMin1_Bhv)/(df.ATS2m+df.AATS1i)) -0.002756790708*((df.AMR-df.ATSC7e)+(df.ATSC3v/df.AATSC0v)) -1.515093709*((df.MATS1i*df.SpMax8_Bhi)*(df.SpMax8_Bhi/df.SpDiam_Dzv)) + 0.4049213096

r2_train = r2_score(df.Target,predicted_train)
r2_train2 = r2_score(df.Target,predicted_2d)
r2_train3 = r2_score(df.Target,predicted_3d)
rmse_2d = mean_squared_error(df.Target,predicted_2d)
print(r2_train)

fig = plt.figure(figsize=(10,8))
plt.plot([0,2.5],[0,2.5],color="black")
plt.scatter(df.Target, predicted_train,c='green',marker='^',s=100,alpha=1.0,label=f'Train - R$^2$:{r2_train:.3f}')
#plt.scatter(df.Target, predicted_2d,c='black',marker='x',s=100,alpha=0.7,label=f'R$^2$:{r2_train2:.3f}')
#plt.scatter(df.Target, predicted_3d,c='orange',marker='x',s=40,alpha=0.5,label=f'Train - R$^2$:{r2_train3:.3f};3-term')
plt.xlabel("DFT Specific Energy")
plt.ylabel("Predicted Specific Energy")
plt.title('Training')
plt.xlim(0,2.5)
plt.ylim(0,2.5)
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14)
plt.tick_params(axis='both', which='both', labelsize='medium')
legend = plt.legend(facecolor='lightgray', edgecolor='black')

plt.savefig('sisso_train.png')
plt.show()
df_train_sisso = pd.DataFrame()
df_train_sisso['True'] = df.Target
df_train_sisso['1D'] = predicted_train
df_train_sisso['2D'] = predicted_2d
df_train_sisso['3D'] = predicted_3d
df_train_sisso.to_csv('Training_True_predictions_sisso.csv')


df_test = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/padel_redox/redox_test_pade.csv')
df_test.drop(df_test.columns[[0,2]],axis=1,inplace=True)

df_test1 = pd.read_csv('/home/muthyala.7/padel_Desc_test_above_1.csv')
df_test1.drop(df_test1.columns[[0]],axis=1,inplace=True)
df_test1.rename(columns={'Redox': 'Target'}, inplace=True)

df_test2 = pd.read_csv('/home/muthyala.7/padel_desc_se_below_05.csv')
#pdb.set_trace()
df_test2.drop(df_test2.columns[[0]],axis=1,inplace=True)
df_test = pd.concat([df_test, df_test1,df_test2], axis=0)
df_test.reset_index(drop=True,inplace=True)



predicted_test = 144.146766945998*((df_test.SpMax4_Bhm+df_test.MLFER_L)/(df_test.MW*df_test.MLFER_L))+0.06388827111251938

predicted_2d = -106.77303791869888*((df_test.MLFER_L/df_test.MW)/(df_test.SpMax4_Bhm-df_test.MLFER_L)) -0.25326293870328537*((df_test.SpMax4_Bhm-df_test.SpMax5_Bhm)-(df_test.SpMax4_Bhm/df_test.SpMax5_Bhm)) -0.035775314803984326

predicted_3d = 94.78148127016601*((df_test.SpMax4_Bhm+df_test.MLFER_L)/(df_test.MW*df_test.MLFER_L))   + 2330.6753717871925*((df_test.SpMax4_Bhm/df_test.MLFER_L)/(df_test.ATS2m+df_test.ZMIC0))   + 0.021322180419827048*((df_test.SpMax4_Bhm-df_test.MLFER_L)*(df_test.SpMax4_Bhm-df_test.SpMax5_Bhm))+0.19302379805499048


from sklearn.metrics import r2_score



r2_test = r2_score(df_test.Target,predicted_test)
r2_test2 = r2_score(df_test.Target,predicted_2d)
r2_test3 = r2_score(df_test.Target,predicted_3d)
mse_2d = mean_squared_error(df_test.Target,predicted_2d)
print(r2_test)

fig = plt.figure(figsize=(10,8))
plt.plot([0,2.5],[0,2.5],color="black")
plt.scatter(df_test.Target, predicted_test,c='orange',marker='s',s=100,alpha=0.9,label=f'Test - R$^2$:{r2_test:.3f}')
#plt.scatter(df_test.Target, predicted_2d,c='green',marker='^',s=70,alpha=0.70,label=f'R$^2$:{r2_test2:.3f}')
#plt.scatter(df_test.Target, predicted_3d,c='black',marker='x',s=40,alpha=0.5,label=f'Test - R$^2$:{r2_test3:.3f};3-term')
plt.xlabel("DFT Specific Energy")
plt.ylabel("Predicted Specific Energy")
plt.title('Testing')
plt.xlim(0,2.5)
plt.ylim(0,2.5)
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14)
plt.tick_params(axis='both', which='both', labelsize='medium')
legend = plt.legend(facecolor='lightgray', edgecolor='black')

plt.savefig('symantecs_test.png')
plt.show()
df_train_symantecs = pd.DataFrame()
df_train_symantecs['True'] = df_test.Target
df_train_symantecs['1D'] = predicted_test
df_train_symantecs['2D'] = predicted_2d
df_train_symantecs['3D'] = predicted_3d
df_train_symantecs.to_csv('Testing_True_predictions_symantecs.csv')

predicted_train = 1.032521911*((df_test.ATS3i/df_test.SpAD_Dzi)/(df_test.SpAD_Dzi*df_test.SpMax1_Bhm)) + 0.5533907820
predicted_2d = 8.313376203*((df_test.SpMin1_Bhi/df_test['SP-3'])/(df_test.SpMax1_Bhm+df_test.SpMax4_Bhm)) +14.85502453*((df_test.SpMin1_Bhi/df_test.SpAD_Dzi)/(df_test.AATS0p-df_test.ETA_EtaP_F_L)) + 0.2611027328
predicted_3d = 7.750974934*((df_test.SpMin1_Bhi/df_test['SP-3'])/(df_test.SpMax1_Bhm+df_test.SpMax4_Bhm)) +16.76116823*((df_test.SpMin1_Bhi/df_test.SpAD_Dzi)/(df_test.AATS0p-df_test.ETA_EtaP_F_L)) + 0.2941239911 -0.006580062660*((df_test.ATSC3i*df_test.MLFER_BO)/(df_test.AATS0p-df_test['SP-3']))
r2_train = r2_score(df_test.Target,predicted_train)
r2_train2 = r2_score(df_test.Target,predicted_2d)
r2_train3 = r2_score(df_test.Target,predicted_3d)
mse_2d = mean_squared_error(df_test.Target,predicted_2d)

r2_test = r2_score(df_test.Target,predicted_test)

fig = plt.figure(figsize=(10,8))
plt.plot([0,2.5],[0,2.5],color="black")

plt.scatter(df_test.Target, predicted_train,c='orange',marker='s',s=100,alpha=0.9,label=f'Test - R$^2$:{r2_train:.3f}')
#plt.scatter(df_test.Target, predicted_2d,c='orange',marker='s',s=70,alpha=0.7,label=f'R$^2$:{r2_train2:.3f}')
#plt.scatter(df_test.Target, predicted_3d,c='black',marker='x',s=40,alpha=0.5,label=f'Test - R$^2$:{r2_train3:.3f};3-term')
plt.xlabel("DFT Specific Energy")
plt.ylabel("Predicted Specific Energy")
plt.title('Testing')
plt.xlim(0,2.5)
plt.ylim(0,2.5)
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14)
plt.tick_params(axis='both', which='both', labelsize='medium')
legend = plt.legend(facecolor='lightgray', edgecolor='black')
plt.savefig('sisso_test.png')
plt.show()


df_train_symantecs = pd.DataFrame()
df_train_symantecs['True'] = df_test.Target
df_train_symantecs['1D'] = predicted_train
df_train_symantecs['2D'] = predicted_2d
df_train_symantecs['3D'] = predicted_3d
df_train_symantecs.to_csv('Testing_True_predictions_sisso.csv')

pdb.set_trace()


import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/solv2/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
start_c = time.time()
operators = ['+','-','*','/']
rmse,equation,r2 = symantic_model(df,operators=operators,metrics=[0.15,0.99],initial_screening=['mi',0.99]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')

#predicted_train = -0.0005799545402075436*((df.AATS1m*df.AATSC0s)+(df.ATS2i/df.AATSC0s))+0.099358261269612

predicted_train = -0.003448691822153573*((df.AATS0m+df.AATS1m)+(df.ATSC0v/df.AATSC0s))+0.6897374553808384
predicted_2d = -0.0037312489445682465*((df.AATS2s*df.MIC0)+(df.ATSC0v/df.AATSC0s))  -0.2742596350026408*((df.AMW+df.MATS2m)+(df.AATSC0s*df.MATS2m)) + 3.1412327295177693
predicted_3d = -0.004193913273660162*((df.AMW*df.MIC0)+(df.ATSC0v/df.AATSC0s))  -0.34591187593018796*((df.AMW+df.MATS2m)+(df.AATSC0s*df.MATS2m))   + 3.406315783699522e-07*((df.ATSC2m+df.ATSC0v)*(df.ATSC2m*df.MATS2m)) + 4.289374170831487


fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

r2_train = r2_score(df.Target,predicted_train)
r2_train2 = r2_score(df.Target,predicted_2d)
r2_train3 = r2_score(df.Target,predicted_3d)
print(r2_train)

plt.plot([-3,0],[-3,0],color="black")
plt.scatter(df.Target, predicted_train,c='red',marker='x',s=40,alpha=0.9,label=f'Train - R$^2$:{r2_train:.3f}')
#plt.scatter(df.Target, predicted_2d,c='black',marker='x',s=40,alpha=0.7,label=f'Train - R$^2$:{r2_train2:.3f}')
#plt.scatter(df.Target, predicted_3d,c='orange',marker='x',s=40,alpha=0.5,label=f'Train - R$^2$:{r2_train3:.3f}')
plt.xlabel("DFT Solvation Energy",weight ='bold')
plt.ylabel("Predicted Solvation Energy", weight='bold')
plt.title('Training pairity plot',weight='bold')
plt.xlim(-3,0)
plt.ylim(-3,0)
plt.legend()
plt.show()


predicted_train = -0.2684274297*((df.ATS2e*df.MATS2i)*(df['VCH-6']/df.GATS1e)) -0.7466743398

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

r2_train = r2_score(df.Target,predicted_train)
print(r2_train)

plt.plot([-3,0],[-3,0],color="black")
plt.scatter(df.Target, predicted_train,c='red',marker='x',s=40,alpha=0.8,label=f'Train - R$^2$:{r2_train:.3f}')
plt.xlabel("DFT Solvation Energy",weight ='bold')
plt.ylabel("Predicted Solvation Energy", weight='bold')
plt.title('Training pairity plot',weight='bold')
plt.xlim(-3,0)
plt.ylim(-3,0)
plt.legend()
plt.show()

df_test = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/solv2/solv_mi_test.csv')

predicted_train = -0.003448691822153573*((df_test.AATS0m+df_test.AATS1m)+(df_test.ATSC0v/df_test.AATSC0s))+0.6897374553808384
predicted_2d = -0.0037312489445682465*((df_test.AATS2s*df_test.MIC0)+(df_test.ATSC0v/df_test.AATSC0s))  -0.2742596350026408*((df_test.AMW+df_test.MATS2m)+(df_test.AATSC0s*df_test.MATS2m)) + 3.1412327295177693
predicted_3d = -0.004193913273660162*((df_test.AMW*df_test.MIC0)+(df_test.ATSC0v/df_test.AATSC0s))  -0.34591187593018796*((df_test.AMW+df_test.MATS2m)+(df_test.AATSC0s*df_test.MATS2m))   + 3.406315783699522e-07*((df_test.ATSC2m+df_test.ATSC0v)*(df_test.ATSC2m*df_test.MATS2m)) + 4.289374170831487

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
r2_train = r2_score(df_test.Target,predicted_train)

r2_train2 = r2_score(df_test.Target,predicted_2d)
r2_train3 = r2_score(df_test.Target,predicted_3d)
print(r2_train)

plt.plot([-3,0],[-3,0],color="black")
plt.scatter(df_test.Target, predicted_train,c='red',marker='x',s=40,alpha=0.9,label=f'Train - R$^2$:{r2_train:.3f}')
plt.scatter(df_test.Target, predicted_2d,c='blue',marker='x',s=40,alpha=0.7,label=f'Train - R$^2$:{r2_train2:.3f}')
plt.scatter(df_test.Target, predicted_3d,c='green',marker='x',s=40,alpha=0.5,label=f'Train - R$^2$:{r2_train3:.3f}')


plt.xlabel("DFT Solvation Energy",weight ='bold')
plt.ylabel("Predicted Solvation Energy", weight='bold')
plt.title('Testing pairity plot',weight='bold')
plt.xlim(-3,0)
plt.ylim(-3,0)
plt.legend()
plt.show()

pdb.set_trace()
predicted_test = -0.2684274297*((df_test.ATS2e*df_test.MATS2i)*(df_test['VCH-6']/df_test.GATS1e)) -0.7466743398
fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
r2_test = r2_score(df_test.Target,predicted_test)
plt.plot([-3,0],[-3,0],color="black")
plt.scatter(df_test.Target, predicted_test,c='green',marker='x',s=40,alpha=0.8,label=f'Test - R$^2$:{r2_test:.3f}')
plt.xlabel("DFT Solvation Energy",weight ='bold')
plt.ylabel("Predicted Solvation Energy", weight='bold')
plt.title('Testing pairity plot',weight='bold')
plt.xlim(-3,0)
plt.ylim(-3,0)
plt.legend()
plt.show()
print(sum((df_test.Target - predicted_test)**2))

pdb.set_trace()



'''
####################################################################################################################


# FEYNMAN DATASETS WHERE DIMENSIONALITY FAILS....

#######################################################################################################################

'''


df =pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/dim_fail_SISSO/distance/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['+','-','pow(1/2)','pow(2)'],dimensionality=['u1','u1','u1','u1'],output_dim=(symbols('u1')*symbols('u1'))).fit()
print('DIMENSIONAL SyMANTIC  COMPLETED IN::',time.time()-st)
pdb.set_trace()

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/dim_fail_SISSO/medium_12_11/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['+','*','sin'],dimensionality=['u1','u2','u3','u4','1']).fit()
print('DIMENSIONAL SISSO COMPLETED IN::',time.time()-st)
pdb.set_trace()

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/dim_fail_SISSO/10.7/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['/','*','pow(2)','-'],dimensionality=['u1','u2','u2'],output_dim=(symbols('u1')*symbols('u1')),metrics=[0.001,1.0]).fit()
print('DIMENSIONAL SISSO COMPLETED IN::',time.time()-st)
pdb.set_trace()

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/dim_fail_SISSO/11.3/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['/','*','pow(2)','-'],dimensionality=['u1','u2','u3','u4','u4'],metrics=[0.001,1.0]).fit()

print('DIMENSIONAL SISSO COMPLETED IN::',time.time()-st)
pdb.set_trace()

'''



'''

#######################################################################################

#SYNTHETIC DATASETS....

############################################################################################

'''



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/1/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['/','+']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators,metrics=[0.04,0.995]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()
print('#########################################################################################################')

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/2/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['sin','pow(1/2)']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#########################################################################################################')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/3/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['/','+','exp']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#########################################################################################################')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/4/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
st = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(2)','pow(3)']).fit()
print("SISSO Completed in: ",time.time()-st,'\n')
pdb.set_trace()

print('#########################################################################################################')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/5/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(2)','+','/','exp','-']).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#########################################################################################################')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/6/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(1/2)','pow(2)','+'],metrics=[0.05,1.0],sis_features=5).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#########################################################################################################')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/7/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['exp(-1)','sin','*']).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#########################################################################################################')


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/8/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=['pow(3)','pow(2)','*']).fit()

print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('###################################################################################################')



df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/9/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
operators = ['ln','*','/']
rmse,equation,r2 = symantic_model(df,operators=operators,metrics=[0.01,1.0]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')
pdb.set_trace()

print('#############################################################')

df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/10/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)

start_c = time.time()
operators = ['exp(-1)','*','/']
rmse,equation,r2 = symantic_model(df,operators=operators,metrics=[0.01,1.0]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')


pdb.set_trace()

'''
##################################################################################################################


##### GPLEARN BENCHMARKING..........................

####################################################################################################################



import numpy as np
from gplearn.genetic import SymbolicRegressor
from sklearn.metrics import mean_squared_error

# Generate some sample data



from gplearn.functions import make_function


def _protected_exponent(x1):
    with np.errstate(over='ignore'):
        return np.where(np.abs(x1) < 100, np.exp(x1), 0.)

exp = make_function(function=_protected_exponent,
                        name='exp',
                        arity=1)

def pow2(x1):
   with np.errstate(over='ignore'):
       return np.where(np.abs(x1) < 100, np.power(x1,2), 0.)

square = make_function(function=pow2,
                        name='square',
                        arity=1)

def pow3(x1):
   with np.errstate(over='ignore'):
       return np.where(np.abs(x1) < 100, np.power(x1,3), 0.)

cube = make_function(function=pow3,
                        name='cube',
                        arity=1)

paths = ['/home/muthyala.7/TorchSisso_casestudies/Case_Studies/1/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/2/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/3/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/4/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/5/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/6/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/7/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/8/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/9/train.dat',
         '/home/muthyala.7/TorchSisso_casestudies/Case_Studies/10/train.dat'
            
    ]

function_set =[['add','div'],['sin','sqrt','add'],[exp,'add','div'],[square,cube,'add'],[square,exp,'add','sub','div'],
               ['sqrt',square,exp,'add'],['sin',exp,'mul','add'],[square,cube,'mul','add'],['log','add','mul'],[exp,'add','mul']
               ]


from gplearn.genetic import SymbolicRegressor
from sympy import *
converter = {
    'sub': lambda x, y : x - y,
    'div': lambda x, y : x/y,
    'mul': lambda x, y : x*y,
    'add': lambda x, y : x + y,
    'square': lambda x, y : x**2,
    'sin': lambda x    : sin(x),
    'cos': lambda x    : cos(x),
    'sqrt': lambda x: x**0.5,
    'cube': lambda x: x**3,
    'exp': lambda x: exp(x),
    'log': lambda x: log(x)
}

gp_learn_equations =[]
scores = []
RMSE=[]

for i,path in enumerate(paths):
    print(path)
    df = pd.read_csv(path,sep='\t')
    df.drop(df.columns[[0]],axis=1,inplace=True)
    X_train = df.iloc[:,1:].to_numpy()
    y_train = df.iloc[:,0].to_numpy()
    
    est_gp = SymbolicRegressor(
    population_size=20000,
    function_set=function_set[i],
    generations=20,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.01,
    random_state=0,
    feature_names=df.iloc[:,1:].columns,
    metric='rmse')

    est_gp.fit(X_train, y_train)
    
    #print(est_gp._program)
    y_pred = est_gp.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, y_pred))
    RMSE.append(rmse)
    print(f'RMSE: {rmse:.4f}')
    print('R2:',est_gp.score(X_train, y_train))
    s = est_gp.score(X_train, y_train)
    
    
    try:
        next_e = sympify((est_gp._program), locals=converter)
    except:
        
        next_e = est_gp._program
        
    scores.append(s)
    gp_learn_equations.append(next_e)


df_eq = pd.DataFrame()
df_eq['Equations'] = gp_learn_equations
df_eq ['Scores (R2)'] = scores
df_eq['RMSE'] = RMSE
df_eq.to_csv('gp_learn_equations.csv')

pdb.set_trace()


'''
#Case study to checke the multi-task feature...
'''
X = np.random.uniform(1,5,(10,4))
cols = [f'x{i+1}' for i in range(4)]

df = pd.DataFrame(X,columns=cols)
y1 = df.iloc[:,0]/(df.iloc[:,1]*(df.iloc[:,2]+df.iloc[:,3]))
y2 = df.iloc[:,0]/(df.iloc[:,1]*(df.iloc[:,2]-df.iloc[:,3]))

df.insert(0,'Target1',y1)
df.insert(1,'Target2',y2)



operators = ['/','+','-']
start_c = time.time()
rmse,equation,r2 = symantic_model(df,operators=operators,multi_task=[[0,1],[[2,3,4,5],[2,3,4,5]]],no_of_operators=3).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')
'''



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import rainbow
import numpy as np
from scipy.integrate import solve_ivp
from scipy.io import loadmat

import pysindy as ps 

from pysindy import utils# import linear_damped_SHO
from pysindy.utils import cubic_damped_SHO
from pysindy.utils import linear_3D
from pysindy.utils import hopf
from pysindy.utils import lorenz

import pysindy as ps

# ignore user warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#np.random.seed(1000)  # Seed for reproducibility

# Integrator keywords for solve_ivp
integrator_keywords = {}
integrator_keywords['rtol'] = 1e-12
integrator_keywords['method'] = 'LSODA'
integrator_keywords['atol'] = 1e-12

dt = 0.001
t_train = np.arange(0, 100, dt)
t_train_span = (t_train[0], t_train[-1])
x0_train = [-8, 8, 27]
x_train = solve_ivp(lorenz, t_train_span,
                    x0_train, t_eval=t_train, **integrator_keywords).y.T
x_dot_train_measured = np.array(
    [lorenz(0, x_train[i]) for i in range(t_train.size)]
)


y1 = x_dot_train_measured[:,0] #+ noise#10*(x_train[:,1]-x_train[:,0])
y2 = x_dot_train_measured[:,1] #+ noise#x_train[:,0]*(28-x_train[:,2]) - x_train[:,1]
y3 = x_dot_train_measured[:,2] #+ noise#x_train[:,0]*x_train[:,1] - (8/3)*x_train[:,2]

cols = ['x','y','z']

df = pd.DataFrame(x_train,columns=cols)
df.insert(0,'Target1',y1)
df.insert(1,'Target2',y2)
df.insert(2,'Target3',y3)
df['Time'] = t_train

import random 
random.seed(41)
random_numbers = sorted(random.sample(range(1, 100000), 5))
print(random_numbers)

df1 = df.iloc[random_numbers,:]
df.drop(df1.index,inplace=True)
df1.reset_index(drop=True,inplace=True)
df1.iloc[:,3] = df1.iloc[:,3] #+ np.random.normal(0,0.1,50)
df1.iloc[:,4] = df1.iloc[:,4] #+ np.random.normal(0,0.1,50)
df1.iloc[:,5] = df1.iloc[:,5] #+ np.random.normal(0,0.1,50)
import time
st = time.time()
model = ps.SINDy(feature_library=ps.PolynomialLibrary(interaction_only=True),feature_names=['x','y','z'])
model.fit(df1.iloc[:,[3,4,5]].to_numpy(),t = df1.Time.to_numpy(),x_dot=df1.iloc[:,[0,1,2]].to_numpy())
model.print()
print(time.time()-st)

operators = ['*']
start_c = time.time()
rmse,equation,r2,equations = symantic_model(df1.iloc[:,:-1],operators=operators,multi_task=[[0,1,2],[[3,4,5],[3,4,5],[3,4,5]]],metrics=[0.05,0.99]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')

pdb.set_trace()


x = df.iloc[:,3]
y = df.iloc[:,4]
z = df.iloc[:,5]



t_test = np.arange(0, 15, dt)
x0_test = np.array([8, 7, 15])
t_test_span = (t_test[0], t_test[-1])
x_test = solve_ivp(
    lorenz, t_test_span, x0_test, t_eval=t_test, **integrator_keywords
).y.T


x_test1 = model.simulate(x0_test, t_test)

def lorenz_1(t,x):
    return [
        10.000 * (x[1] - x[0]),
        -1.0000000000000004*(x[0]*x[2])  -1.00000000000001*x[1]   + 28.00000000000002*x[0],
        #-3.265 + 6.591*x[0] + 11.441*x[1]  -0.599*x[1]*x[2], 
        #-2.344 + 5.524*x[0] + 12.303*x[1]-0.601*x[2]*x[1],
        x[0] * x[1] - 2.667 * x[2],
    ]

def lorenz_2(t,x):
    return [
        10.0000*(x[1]-x[0]),
        -1.000*x[0]*x[2] -1.000000*x[1]   + 28.000000*x[0],
         #1.0000000*x[0]*x[1] -2.6666700000000003*x[2],
         #1.0000000*x[0]*x[1] -2.666669999999999*x[2], # 5datapoints
         1.0000000*x[0]*x[1] -2.666670000000000*x[2], #10 datapoints
    ]

'''
x_test1= solve_ivp(
    lorenz_1, t_test_span, x0_test, t_eval=t_test, **integrator_keywords
).y.T
'''
x_test2= solve_ivp(
    lorenz_2, t_test_span, x0_test, t_eval=t_test, **integrator_keywords
).y.T

from sklearn.metrics import mean_squared_error
r_syn = ((mean_squared_error(x_test[:,0], x_test1[:,0]) + mean_squared_error(x_test[:,1], x_test1[:,1]) +mean_squared_error(x_test[:,2], x_test1[:,2]))/3)
r_sym = ((mean_squared_error(x_test[:,0], x_test2[:,0]) + mean_squared_error(x_test[:,1], x_test2[:,1]) +mean_squared_error(x_test[:,2], x_test2[:,2]))/3)

pdb.set_trace()

df_sym = pd.DataFrame(x_test2,columns=['x','y','z'])
df_syn = pd.DataFrame(x_test1,columns=['x','y','z'])
df_original = pd.DataFrame(x_test,columns=['x','y','z'])

df_original.to_csv('15_points_oringal.csv')
df_sym.to_csv('symantecs_15_points.csv')
df_syn.to_csv('15_points_sindy.csv')



import matplotlib
matplotlib.rcParams.update({# Use mathtext, not LaTeX
                            'text.usetex': False,
                            # Use the Computer modern font
                            'font.family': 'serif',
                            'font.serif': 'cmr10',
                            'mathtext.fontset': 'cm',
                            # Use ASCII minus
                            'axes.unicode_minus': False,
                            'figure.dpi' : 300,

                            })

font = {'weight' : 'bold',
        'size'   : 34}
plt.rc('font', **font)


# Create a figure and a 3D axis
fig = plt.figure(figsize=(10, 10))
ax1 = plt.axes(projection="3d")

# Plot data
ax1.plot(x_test[:, 0], x_test[:, 1], x_test[:, 2], color='blue', label='Original', alpha=0.8, lw=1.5, linestyle='-')
line2, = ax1.plot(x_test2[:, 0], x_test2[:, 1], x_test2[:, 2], color='red', label='SyMANTIC', alpha=1.0, lw=1.5, linestyle='--')

# Customize the dashed line (increase the space between dashes)
line2.set_dashes([10, 10])  # Dash length of 10 points and space of 10 points

# Set labels and title
ax1.set_xlabel("$x$", fontsize=25, labelpad=10, weight='bold')
ax1.set_ylabel("$y$", fontsize=25, labelpad=10, weight='bold')
ax1.set_zlabel("$z$", fontsize=25, weight='bold')
ax1.zaxis.labelpad = -1.0 
ax1.tick_params(axis='x', labelsize=25)
ax1.tick_params(axis='y', labelsize=25)
ax1.tick_params(axis='z', labelsize=20)
ax1.set_title("Test System", fontsize=14, pad=20, weight='bold')

# Show legend
plt.legend(fontsize=14)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('Test_system_5datapoints_symantic.png')
plt.show()


fig = plt.figure(figsize=(10, 10))
ax1 = plt.axes(projection="3d")
ax1.plot(x_test[:,0],x_test[:,1],x_test[:,2], "k",color='blue',label='Original',alpha=0.8,lw=1.5,linestyle='-')
ax1.plot(x_test1[:,0],x_test1[:,1],x_test1[:,2], "k",color='red',label=f'PySINDy',alpha=1.0,linestyle='--',lw = 1.5)
# Set labels and title
ax1.set_xlabel("$x$", fontsize=25, labelpad=10,weight='bold')
ax1.set_ylabel("$y$", fontsize=25, labelpad=10,weight='bold')
ax1.set_zlabel("$z$",fontsize=25,weight='bold')  # Increased labelpad for z-label
ax1.zaxis.labelpad=-1.0 
ax1.tick_params(axis='x', labelsize=25)
ax1.tick_params(axis='y', labelsize=25)
ax1.tick_params(axis='z', labelsize=20)

ax1.set_title("Test System", fontsize=14, pad=20,weight='bold')
plt.legend(fontsize=14)
plt.tight_layout()
#plt.savefig('Test_system_5datapoints.png')
plt.savefig('Test_system_5datapoints_sindy.png')
#plt.savefig('Test_system_15datapoints.png')
plt.show()


'''

plt.figure(figsize=(10,8))

plt.plot(t_test, (x_test[:,2]-x_test2[:,2]), label='SyMANTIC', alpha=0.6, c='red', linewidth=1)
plt.plot(t_test, (x_test[:,2]-x_test1[:,2]), label='pySindy', alpha=0.8, c='green', linewidth=1,linestyle='dashed')

plt.xlabel('Time (t)',weight='bold',fontsize=20)
plt.ylabel(r'$\epsilon_z$',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend()

plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)


#plt.savefig('z_error_5.png')
#plt.savefig('z_error_10.png')
plt.savefig('z_error_15.png')

###############################################

plt.figure(figsize=(10,8))

plt.plot(t_test, (x_test[:,0]-x_test2[:,0]), label='SyMANTIC', alpha=0.6, c='red', linewidth=1)
plt.plot(t_test, (x_test[:,0]-x_test1[:,0]), label='pySindy', alpha=0.8, c='green', linewidth=1,linestyle='dashed')

plt.xlabel('Time (t)',weight='bold',fontsize=20)
plt.ylabel(r'$\epsilon_x$',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend()

plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('x_error_5.png')
#plt.savefig('x_error_10.png')
plt.savefig('x_error_15.png')

plt.figure(figsize=(10,8))

plt.plot(t_test, (x_test[:,1]-x_test2[:,1]), label='SyMANTIC', alpha=0.6, c='red', linewidth=1)
plt.plot(t_test, (x_test[:,1]-x_test1[:,1]), label='pySindy', alpha=0.8, c='green', linewidth=1,linestyle='dashed')

plt.xlabel('Time (t)',weight='bold',fontsize=20)
plt.ylabel(r'$\epsilon_y$',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend()
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_error_5.png')
#plt.savefig('y_error_10.png')
plt.savefig('y_error_15.png')
'''
plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,1], label='Original', alpha=0.8, c='blue', linewidth=1.5,linestyle='-')

line2, = plt.plot(t_test[:], x_test2[:,1], label='SyMANTIC', alpha=1.0, c='red', linewidth=1.5,linestyle='--')
line2.set_dashes([10, 10])

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('y',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('y_vs_t_5_symantic.png')
#plt.savefig('y_vs_t_15.png')

plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,1], label='Original', alpha=0.6, c='blue', linewidth=1.5,linestyle='-')
plt.plot(t_test, x_test1[:,1], label='PySINDy', alpha=1.0, c='red', linewidth=2,linestyle='dotted')

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('y',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('y_vs_t_5_sindy.png')
#plt.savefig('y_vs_t_15.png')


plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,0], label='Original', alpha=0.8, c='blue', linewidth=1.5,linestyle='-')

line2, = plt.plot(t_test[:], x_test2[:,0], label='SyMANTIC', alpha=1.0, c='red', linewidth=1.5,linestyle='--')
line2.set_dashes([10, 10])

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('x',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('x_vs_t_5_symantic.png')
#plt.savefig('y_vs_t_15.png')

plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,0], label='Original', alpha=0.6, c='blue', linewidth=1.5,linestyle='-')
plt.plot(t_test, x_test1[:,0], label='PySINDy', alpha=1.0, c='red', linewidth=2,linestyle='dotted')

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('x',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('x_vs_t_5_sindy.png')
#plt.savefig('y_vs_t_15.png')


plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,2], label='Original', alpha=0.8, c='blue', linewidth=1.5,linestyle='-')

line2, = plt.plot(t_test[:], x_test2[:,2], label='SyMANTIC', alpha=1.0, c='red', linewidth=1.5,linestyle='--')
line2.set_dashes([10, 10])

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('z',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('z_vs_t_5_symantic.png')
#plt.savefig('y_vs_t_15.png')

plt.figure(figsize=(10,8))
plt.plot(t_test[:], x_test[:,2], label='Original', alpha=0.6, c='blue', linewidth=1.5,linestyle='-')
plt.plot(t_test, x_test1[:,2], label='PySINDy', alpha=1.0, c='red', linewidth=2,linestyle='dotted')

plt.xlabel('t',weight='bold',fontsize=20)
plt.ylabel('z',weight='bold',fontsize=20) 
plt.xlim(0,15)
plt.legend(fontsize=14)
plt.xticks(fontsize = 20) 
plt.yticks(fontsize = 20)
#plt.savefig('y_vs_t_5.png')
plt.savefig('z_vs_t_5_sindy.png')
#plt.savefig('y_vs_t_15.png')



