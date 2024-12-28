import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
from validation.validator import FilesValidationChecker
import seaborn as sns
import streamlit as st


class LineChartClass(object):

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

    def tranform_df(self):
        
        month_mapping = {
            0:"Jul",
            1:"Aug",
            2:"Sep",
            3:"Oct",
            4:"Nov",
            5:"Jan",
            6:"Feb",
            7:"Mar",
            8:"Apr",
            9:"May",
            10:"Jun"
        }
        plt.rcParams.update({
            'font.size': 12,
            'font.weight': 'bold',
            'axes.labelsize': 14,
            'axes.titlesize': 16,
            'legend.fontsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
        })

        calc_no_of_person_df_testing_copy = self.calc_no_of_person_df_testing.copy()
        calc_no_of_person_df_testing_copy['months'] = calc_no_of_person_df_testing_copy['months'].map(month_mapping)

        return calc_no_of_person_df_testing_copy


    def predictive_line_chart(self):
        
        st.markdown("#### Predictive Line Chart")
        calc_no_of_person_df_testing_copy = self.tranform_df()
        
        fig , ax = plt.subplots(1,1 , figsize=(12,8))

        sns.set_style("whitegrid")

        sns.lineplot(data=calc_no_of_person_df_testing_copy,
                    x = 'months',y='total_amount',ax=ax,marker='o',markersize=10,color='Blue',label="Total Amount")

        sns.lineplot(data=self.user_df,
                    x = 'months',y='predictions',ax=ax,marker='o',markersize=10,color='yellow',label="Predictions")

        plt.axhline(y=self.target_1st, color='red', linestyle='-', linewidth=2, label=f"Target: ₹{self.target_1st}")
        plt.axhline(y=self.target_threshold , color='green',linestyle='--',linewidth=2 ,label=f"Minimum Target: ₹{self.target_threshold}")

        # Draw vertical lines with arrows pointing from the lower to the higher target
        plt.annotate('',xy=(0,self.target_threshold),
                    xytext=(0,self.target_1st),arrowprops=dict(color='gray',arrowstyle='<->')
                    )
        plt.text(0.03 ,(self.target_threshold+self.target_1st)//2 ,f'₹{(self.target_1st-self.target_threshold):,}',fontsize=9,color='red') # This the the target_1st-target_threshold

        plt.fill_between(
            [0, (calc_no_of_person_df_testing_copy.shape[0]+self.user_df.shape[0])],  # X-range (months), adjust this if your x-axis is different
            self.target_threshold, self.target_1st,  # Y-range for the shaded area
            color='#4CC9F0', alpha=0.3, label="Target Difference Area"
        )

        for i,row in calc_no_of_person_df_testing_copy.iterrows():
            plt.text(row['months'],row['total_amount']+(row['total_amount']*0.02),
                    f"₹{row['total_amount']:,}",ha='center',va='top',color='black',fontsize=9
                    )

        for i,row in self.user_df.iterrows():
            plt.text(row['months'],row['predictions']+(row['predictions']*-0.03),
                    f"₹{row['predictions']:,}",ha='center',va='top',color='black',fontsize=9
                    )
            plt.annotate('',xy=(row['months'],self.target_threshold),
                    xytext=(row['months'],row['predictions']),arrowprops=dict(color='orange',arrowstyle='<->')
                    )
            plt.text(row['months'], (self.target_threshold + row['predictions']) // 2, 
                f'₹{(self.target_threshold - row["predictions"]):,}', 
                fontsize=9, color='red')

            plt.annotate('',xy=(row['months'],self.target_1st),
                    xytext=(row['months'],row['predictions']),arrowprops=dict(color='orange',arrowstyle='<->')
                    )
            plt.text(row['months'], (self.target_1st + row['predictions']) // 2, 
                f'₹{(self.target_1st - row["predictions"]):,}', 
                fontsize=9, color='Green')

        x1 = calc_no_of_person_df_testing_copy.iloc[[-1]]['months'].values[0]
        y1 = calc_no_of_person_df_testing_copy.iloc[[-1]]['total_amount'].values[0]
        y2 = self.user_df.iloc[[0]]['predictions'].values[0]
        x2 = self.user_df.iloc[[0]]['months'].values[0]
        segment_df = pd.DataFrame([[x1 , y1],
                                [x2 , y2]],columns=['x' , 'y'])
        sns.lineplot(data=segment_df,x='x',y='y',color='blue',ax=ax,marker='o',markersize=10,linestyle=':')

            
        plt.title('Overall Predictive Monthly Sales (UNIT-WISE)',fontsize=16,fontweight='bold')
        plt.xlabel('Months',fontsize=12)
        plt.ylabel('Sales (in ₹)',fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(fontsize=10, loc='lower right')
        st.pyplot(fig)

