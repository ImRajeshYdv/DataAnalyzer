import os
import re
import pandas as pd
from dotenv import load_dotenv
from google import genai
load_dotenv()

APIKey = os.getenv('Gemini_API_Key')
GeminiModel = os.getenv('Gemini_Model')

client = genai.Client()

#load excel file
csv_file_path = 'petstoresalesdata.csv'
df = pd.read_csv(csv_file_path) 


#build a metadata of the csv file
def create_metadata(dataframe, description):
    prompt=f'''You are a helpful ai assistant that can answer questions about the metadata of the Data.
    You would be provided with 5 rows of data along with description of the data, based on that you have to create
    a json object which talks about the data.

    Here is the description of the data: 
    {description}

    Here is the data:
    {df}

    Format:
    '''
    format='''
    {
        "metadata":{
            "description":"description of the data",
            "col1":["datatype","data_description"],
            "col2":["datatype","data_description"],
            "col3":["datatype","data_description"],
            "col4":["datatype","data_description"],
            "col5":["datatype","data_description"]
            }
    }
    '''
    
    
    response=client.models.generate_content(model=GeminiModel,contents=prompt+format)
    return response.text.replace("'''",'').replace('```json','').replace('```','').strip()


json_response=create_metadata(df.head(5), "This data contains pet store sales data")
# print(json_response)


#Create Code Generator to analyze the data
def generate_code(metadata, user_query):    
    prompt=f'''You are a helpful ai assistant that can generate python code to answer question about the data.
    You would be provided with metadata of the data and the user query, based on that you have to create
    python code to answer the user_query.

    Instructions:
    1. You have to generate python code only.
    2. The code should be able to run without any error.
    3. The code should be able to answer the user query.
    4. Use pandas library to answer the question.
    5. You have to use the user query to anwer  the question.
    6. You have to use the metadata to understand the data.
    7. You have to use the dataframe named df to answer the question.
    8. You have to use the pandas library to answer the question.
    9. Don't add any other text to the code.
    10. Do not include any explanation, only provide the code.
    11. Do not include any comments in the code.
    12. Do not include any print statements in the code.
    13. Assume the data is already loaded in a dataframe named df.
    14. You have to return the code in a string format
    15. Don't generate any data of your own at any cost.
    16. Make sure the code is syntactically correct.
    17. After genrating the code and printing it, make sure you save the dataframe to a csv file named as "result.csv".
    #line 17 is very important as we will use this file to generate insights.

    Here is the metadata of the data: 
    {json_response}

    Here is the user query:
    {user_query}

    '''
    response=client.models.generate_content(model=GeminiModel,contents=prompt)
    return response.text.replace("'''",'').replace('```json','').replace('```','').replace('python', '').strip()

user_query = "tell me how much sales have Cedar_Lane done in total?"
code = generate_code(json_response, user_query)
print("Generated code:\n", code)


#execute the code
exec(code)



#Create Insights
def create_insights(user_query, result):
    prompt=f'''You are a helpful ai assistant that can generate insights about the data.
    You would be provided with user query and result, based on that you have to create
    insights about the data.

    Instructions:
    1. You have to generate insights only.
    2. The insights should be able to answer the user query.
    3. The insights should be based on the code and result.
    4. You have to use the user query to anwer  the question.
    5. You have to use the code to understand how the result is generated.
    6. You have to use the result to generate insights.
    7. Don't add any other text to the insights.
    8. Do not include any explanation, only provide the insights.
    9. Do not include any comments in the insights.
    10. Do not include any print statements in the insights.
    11. You have to return the insights in a string format
    12. Make sure the insights are grammatically correct.

    Here is the user query:
    {user_query}

    Here is the result:
    {result}

    '''
    response=client.models.generate_content(model=GeminiModel,contents=prompt)
    return response.text.replace("'''",'').replace('```json','').replace('```','').strip()

results_df = pd.read_csv("result.csv")
insights_response=create_insights(user_query, results_df)
print("Insights:\n", insights_response)

    









