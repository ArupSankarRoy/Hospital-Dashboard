from plotfunctions.linechart import PlotClass   
import pandas as pd


cols= ['months','icu','post_icu','twin_share_cabin','single_cabin','general_male_word','general_female_word','predictions']
arr = [['May_Pred',55,60,109,181,230,345,2192500],
['Jun_Pred',105,118,191,330,442,629,4083000],
['Jul_pred',109,116,185,305,450,624,4019000],
['Aug_Pred',81,81,125,235,343,474,2976000],
['Sep_Pred',80,86,125,234,337,449,2949500]]

user_df = pd.DataFrame(arr,columns=cols)
if __name__ == '__main__':
    plot = PlotClass(r"csv\user_input.csv", r"model\sample_model.joblib", user_df)
    plot.predictive_line_chart()