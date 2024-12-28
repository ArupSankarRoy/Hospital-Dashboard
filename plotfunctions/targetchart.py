import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
from validation.validator import FilesValidationChecker
import seaborn as sns
import streamlit as st

class TargetChartClass(object):
    def __init__(self, csv_file_path, model_path, user_df): 

        self.file_path = FilesValidationChecker(csv_file_path, model_path).check_csv_exist()
        self.model_path = FilesValidationChecker(csv_file_path, model_path).check_model_exist()
        self.user_df = user_df

        if self.file_path and self.model_path and isinstance(self.user_df, pd.DataFrame):
            self.calc_no_of_person_df_testing = pd.read_csv(self.file_path)
            self.target_1st = int(self.calc_no_of_person_df_testing['total_amount'].max())
            self.target_threshold = int(self.calc_no_of_person_df_testing['total_amount'].mean())
        else:
            st.error("More than one file exists, or something went wrong.")
            # raise ValueError("More than one file exists, or something went wrong.")
            sys.exit(1)

    def close_chk(self,df, col ,mode='mean_line'):
    
        if mode=='mean_line':
            target_mean = self.calc_no_of_person_df_testing['total_amount'].mean()
            df['diff'] = abs(df[col] - target_mean)
            idx = df['diff'].idxmin()
        else:
            return df.loc[df[col].idxmax(),["ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward"]]
            
        return df.loc[idx,["ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward"]]
    
    def sol(self,df , target_mean , target_max):

        mean_line_dic = dict(self.close_chk(self.calc_no_of_person_df_testing , 'total_amount','mean_line'))
        target_line_dic = dict(self.close_chk(self.calc_no_of_person_df_testing , 'total_amount','target_line'))
        # Points which are upper from the meanline
        upper_df = df[(df['predictions'] >= target_mean) & (df['predictions'] < target_max)].loc[:,["months","ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward"]]
        # Points which are lower from the meanline
        lower_df = df[(df['predictions'] < target_mean)].loc[:,["months","ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward"]]

        result_upper_maxline_target_df = upper_df.copy() # upper points to maxline diff dataframe
        result_lower_meanline_target_df =lower_df.copy()
        result_lower_maxline_target_df = lower_df.copy()
        
        for col in target_line_dic:
            result_upper_maxline_target_df[col]= target_line_dic[col] - upper_df[col]
            result_upper_maxline_target_df[col]= result_upper_maxline_target_df[col].clip(lower=0)
            result_lower_maxline_target_df[col] = target_line_dic[col] - lower_df[col]
            result_lower_maxline_target_df[col] = result_lower_maxline_target_df[col].clip(lower=0)
            
        for col in mean_line_dic:
            result_lower_meanline_target_df[col] = mean_line_dic[col] - lower_df[col]
            result_lower_meanline_target_df[col] = result_lower_meanline_target_df[col].clip(lower=0)

        
        result_lower_to_maxline_target_df = pd.concat([result_lower_maxline_target_df,result_upper_maxline_target_df]).sort_index()
        return result_lower_meanline_target_df,result_lower_to_maxline_target_df
    
    def monthly_target_maxline_and_thresholdline(self):

        result_lower_meanline_target_df,result_lower_to_maxline_target_df = self.sol(self.user_df , self.target_threshold , self.target_1st)    
        result_lower_meanline_target_df_transpose = result_lower_meanline_target_df.T
        result_lower_meanline_target_df_transpose.columns = result_lower_meanline_target_df_transpose.iloc[0]
        result_lower_meanline_target_df_transpose = result_lower_meanline_target_df_transpose[1:]

        result_lower_to_maxline_target_df_transpose = result_lower_to_maxline_target_df.T
        result_lower_to_maxline_target_df_transpose.columns = result_lower_to_maxline_target_df_transpose.iloc[0]
        result_lower_to_maxline_target_df_transpose = result_lower_to_maxline_target_df_transpose[1:]
        
        st.markdown("#### Predictive Target Chart (UNIT WISE)")
        plt.figure(figsize=(12, 8))
        ax = result_lower_to_maxline_target_df_transpose.plot(kind='bar',
                                                      edgecolor='black',
                                                      figsize=(12,8),
                                                      alpha=0.85,
                                                      linewidth=1.2
                                                     )
        plt.title("Monthly Target (MAX LINE)",color='darkred',fontsize=16,fontweight='bold')
        plt.xlabel('Units',fontsize=14,labelpad=10)
        plt.ylabel('Target (NoP)',fontsize=14,labelpad=10)
        plt.xticks(rotation=90,fontsize=12)
        plt.yticks(fontsize=12)

        plt.legend(title='Months',loc='upper right',fontsize=12,title_fontsize=14)
        plt.grid(axis='y',linestyle='--',alpha=0.6)

        for container in ax.containers:
            ax.bar_label(container,fmt=f"+%.0f",label_type='edge',fontsize=10,color='red',padding=3)

        plt.tight_layout()
        st.pyplot(plt.gcf())
        
        plt.figure(figsize=(12, 8))
        ax1 = result_lower_meanline_target_df_transpose.plot(kind='bar',
                                                      edgecolor='black',
                                                      figsize=(12,8),
                                                      linewidth=1.2,
                                                      colormap='plasma',
                                                      alpha=0.83
                                                     )
        plt.title("Monthly Target (THRESHOLD LINE)",color='darkgreen',fontsize=16,fontweight='bold')
        plt.xlabel('Units',fontsize=14,labelpad=10)
        plt.ylabel('Target (NoP)',fontsize=14,labelpad=10)
        plt.xticks(rotation=90,fontsize=12)
        plt.yticks(fontsize=12)

        plt.legend(title='Months',loc='upper right',fontsize=12,title_fontsize=14)
        plt.grid(axis='y',linestyle='--',alpha=0.6)

        for container in ax1.containers:
            ax1.bar_label(container,fmt=f"+%.0f",label_type='edge',fontsize=10,color='green',padding=3)

        plt.tight_layout()
        st.pyplot(plt.gcf())


