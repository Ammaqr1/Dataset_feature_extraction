import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

class Feature_extra:
    
    def __init__(self,df: pd.DataFrame,model):
        
        self.df = df
        self.model = model
        load_dotenv()


        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.prompt = f'''
            You are an expert in data manipulation and feature engineering using Python and Pandas. Given a list of column names from a Pandas DataFrame, your task is to generate a **meaningful** feature name that logically describes the relationship between the provided columns. Then, write a single line of Python code that creates this feature using logical operations or combinations of the columns. The code should be clean, concise, and directly executable in a Python environment.
            
            **Output:**
            - Return **only the Pandas code** for creating the feature, **with no explanations, text, or examples**.
            - The feature name should be meaningful, reflecting a clear relationship between the columns, and follow good feature naming conventions (e.g., `is_young_female`, `high_fare_passenger`).
            - **Only the single line of Python code should be returned**, with no other commentary or explanation.
            
            **Input:**
            - A list of column names from a Pandas DataFrame.
            
            Here is the dataset: {self.df.head().to_json()}
            
            '''
            
    def extract_pandas_code(self,text_list):
        """
        Extracts the Pandas code from a list of text, including code blocks.
        
        Parameters:
        text_list (list): A list of text strings.
        
        Returns:
        str: The Pandas code string.
        """
        in_code_block = False
        for line in text_list:
            if line.startswith("```python"):
                in_code_block = True
            elif line.startswith("```"):
                in_code_block = False
            elif in_code_block and line.startswith("df["):
                return line
        return ""


    def feature_extracting(self):



        # API call to generate features
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": self.prompt}
            ],
            model=self.model,
            
        )
        
        print('Generated feature creation code:')
        
        # Parse and assign the generated features
        insights = chat_completion.choices[0].message.content.split('\n')
        
        # The last line should contain the feature creation code
        feature_code = self.extract_pandas_code(insights)

        print(f"Running the following code:\n{feature_code}")

        try:
            # Execute the generated feature creation code in the context of the df DataFrame
            exec(feature_code, {'df': self.df})
            print(f"New feature created successfully. Here is the updated DataFrame:\n")
        except Exception as e:
            print(f"Error executing feature creation code: {e}")

        return self.df,insights
    
  

# import seaborn as sns 
# models_list = ['gemma-7b-it','llama3-8b-8192']
# titanic = sns.load_dataset('titanic')  
# fe = Feature_extra(titanic,models_list[0])
# df,insight = fe.feature_extracting()

# print('The dataset',df)
# print('The insight',insight)


