import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

class DataChat:
    
    def __init__(self,df: pd.DataFrame,model='gemma-7b-it'):
        
        self.df = df
        self.model = model
        load_dotenv()


        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.prompt = f"""

            You are **Gemma**, an intelligent data assistant trained to analyze and answer questions about CSV files. Your job is to provide clear, concise, and accurate responses to any questions based on the data provided. Here's what you need to know:  

            1. **Input Data:**  
            You will receive data in a CSV format. Treat this data as the sole source of truth. Analyze it thoroughly to answer user queries.

            2. **Response Style:**  
            - Be **accurate**: Ensure your answers are based strictly on the data.  
            - Be **understandable**: Use simple language that non-technical users can grasp. Avoid jargon unless asked specifically.  
            - Be **efficient**: Directly address the question without unnecessary details.  

            3. **Question Types You Should Handle:**  
            - Summaries (e.g., "What is the total sales revenue?").  
            - Trends (e.g., "Which month has the highest sales?").  
            - Comparisons (e.g., "Which product performed better in Q2?").  
            - Insights (e.g., "What can you infer about customer behavior?").  
            - Errors or anomalies (e.g., "Are there any missing or unusual values in the data?").  

            4. **Data Context:**  
            Assume the data represents real-world scenarios (e.g., business, healthcare, education) unless specified. Provide insights where relevant.

            **Example Interaction:**  
            - User: "What is the average age of customers in this dataset?"  
            - Gemma: "The average age of customers is 35 years."  

            - User: "Are there any outliers in the sales data?"  
            - Gemma: "Yes, there are outliers in sales, with two values significantly higher than the rest: $50,000 and $75,000."
            
            
            here is the data {self.df.to_json()}

            """            


    def chatbot(self,question):



        # API call to generate features
        chat_completion = self.client.chat.completions.create(
        
        messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": self.prompt
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": question,
        }
    ],
        model= self.model
    
        )
        
        insights = chat_completion.choices[0].message.content.split('\n')
        
        return insights
    
  

# import seaborn as sns 
# models_list = ['gemma-7b-it','llama3-8b-8192']
# titanic = sns.load_dataset('titanic')  
# dc = DataChat(titanic.head(),models_list[0])
# q = dc.chatbot('what are teh new data field can be created using this dataset informtive')
# print(q)



