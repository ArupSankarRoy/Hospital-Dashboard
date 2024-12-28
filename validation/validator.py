import sys
from pathlib import Path

class FilesValidationChecker(object):
      
      def __init__(self , csv_file_path:None , model_path:None):
         self.csv_file_path = csv_file_path
         self.model_path = model_path

      def check_csv_exist(self):
         path = Path(self.csv_file_path)
         
         if path.exists():
            
            if path.suffix.lower() != '.csv':
               print("Enter Only CSV File !")
               sys.exit(1)

            if path.name != 'user_input.csv' and path.parent.name =='csv':

               new_path= path.parent/"user_input.csv"
               path = path.rename(new_path)
               print("CSV File Rename Successful")
               with open(path,'r') as file:
                  text = file.read()
                  if len(text) <= 0:

                     print("CSV File is Empty...")
                     sys.exit(1)

         else:
            print("Enter a Valid CSV File Path")
            sys.exit(1)

         return path if len(list(path.parent.iterdir())) == 1 else None

      def check_model_exist(self):
         path = Path(self.model_path)
         
         if path.exists():
            
            if path.suffix.lower() != '.joblib':
               print("Enter Only joblib model !")
               sys.exit(1)

            if path.name != 'sample_model.joblib' and path.parent.name =='model':

               new_path= path.parent/"sample_model.joblib"
               path = path.rename(new_path)
               print("Model File Rename Successful")
               
               if path.stat().st_size == 0:
                  print("Enter a valid Model")
                  sys.exit(1)

         else:
            print("Enter a Valid Model File Path")
            sys.exit(1)

         return path if len(list(path.parent.iterdir())) == 1 else None

      

   
      
      

      

   
   
