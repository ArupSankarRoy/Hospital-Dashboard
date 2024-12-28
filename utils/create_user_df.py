import numpy as np
import pandas as pd
from validation.validator import FilesValidationChecker
from joblib import load

def inputdf_to_userdf(input_array:pd.DataFrame ,csv_file_path:str, model_path:str):
    
    input_array_copy = input_array.copy()  
    input_array_copy['months'] = input_array_copy['months'].apply(lambda x: x+'_Pred')     
    user_df = input_array_copy.iloc[:,1:]

    user_df_array = np.array(user_df)

    if FilesValidationChecker(csv_file_path,model_path).check_model_exist() is not None:
        model = load(model_path)

        prediction = model.predict(user_df_array)
        prediction = [int(p) for p in prediction]

        user_df['predictions'] = prediction
        user_df['months'] = input_array_copy['months']

        user_df = user_df[["months","ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward","predictions"]]
        
    return user_df