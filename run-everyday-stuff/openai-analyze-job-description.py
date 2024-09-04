class ServiceUnavailableError(Exception):
    # say that openai is overloaded

    def __init__(self, message="OpenAI is overloaded"):
        self.message = message
        super().__init__(self.message)


import pandas as pd
import numpy as np
import os
import time

import boto3
import io

# open ai stuff
import openai  
import tiktoken
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)



# SOME CONSTANTS
openai.api_key=''    
SLEEP_TIME_OPEN_AI_EACH_ROW = 1
SLEEP_TIME_WHEN_FAILED = 60
BUCKET_NAME_RESULT = 'job-description-process'

# ----------------------------

# Push the result to S3
def UploadDataFrameToS3(df, folder_name, file_name):
    # convert dataframe to CSV String
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # upload to S3
    s3 = boto3.client('s3')

    # folder name will also inlcude current date
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    # change current date to result_date
    current_date = 'result-' + str(current_date)

    # add current date to the folder name path
    folder_name = folder_name + '/' + current_date

    # Upload the CSV string to S3 bucket
    s3.put_object(Body=csv_buffer.getvalue(), Bucket=BUCKET_NAME_RESULT, Key=folder_name + '/' + file_name)



# get some details about the prompt
promtId = 0

def PromptDetails(response):

    global promtId

    # number of of tokens in the prompt with tiktoken
    total_tokens = response['usage']['total_tokens']
    prompt_tokens = response['usage']['prompt_tokens']
    completion_tokens = response['usage']['completion_tokens']

    # print
    print(f'Prompt ID: {promtId} has {total_tokens} tokens, {prompt_tokens} prompt tokens, {completion_tokens} completion tokens')

    # increment prompt id
    promtId += 1

# Open AI get completion
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        PromptDetails(response)
        return response.choices[0].message["content"]
    except Exception as e:
        # error code from openai
        print("Error:", str(e))
        print("Error details:", response)
        raise e
    

def GetSummaryPrompt(job_description):

    prompt = f'''
    Your task is to generate a short summary of the job description to suggest key \ 
    ideas to a job seeker. \

    Summarize the following job description, delimited by tripple bacticks: \
    in at most 3 sentences, and focus on key skills and requirements. \

    Job Description: ```{job_description}```

    '''

    response = get_completion(prompt)
    return response


# Extract key details from the job description
def GetKeyDetails(job_description):

    prompt = f'''
    Your task is to extract key information from a job description. 

    The job description is delimited by tripple bacticks\
    Format your response as a JSON object with the following keys listed below. \
    The description of each key is delimited by double bactick, this information is only for you to understand\
    the content of each key. Don't include it in your response. 
    - "Job Title:" ``What is the job title?``
    - "Technical Skills:" ``Skills like C++, Saleforce, AWS are considered technical skills``
    - "Other Responsibilities:" ``Skills like Business Analytics, Giving data-driven decisions are considered soft skills``
    - "General Technical SKills:" ``Grouping technical skills into a more general category, like "Cloud Computing"``
    - "Background Clearance:" `Broad knowledge of enterprise business systems, but particularly CRM, BI and BPM.
    `Does the job require a background clearance? Answer in Yes or No``
    - "Years of Experience:" ``How many years of experience are required?``
    - "Is this intern or entry position" ``Answer in Yes or No``

    Job Description: ```{job_description}```

    '''

    key_details = get_completion(prompt)
    return key_details


def AnalyzeDescription(df):

    # get the number of rows
    num_rows = df.shape[0]

    i = 0
    # loop over each row
    while i < num_rows:
        # get the job description
        job_description = df.iloc[i]['description']

        # get the job summary
        job_summary = GetSummaryPrompt(job_description)

        # get the key details from the job description
        key_details = GetKeyDetails(job_description)

        # add the job summary and key details to the dataframe
        df.loc[i, 'job_summary'] = job_summary
        df.loc[i, 'key_details'] = key_details

        # increment i
        i += 1

        # sleep for 1 second
    # return the dataframe
    return df




# main function
def main():

    # get data from scraper folder
    
    # get current dir
    current_dir = os.getcwd()

    # find the scraper folder
    scraper_list = os.path.join(current_dir, 'scrapers')
    print(scraper_list)

    # loop over those folder
    for scraper in os.listdir(scraper_list):
        # go inside a folder called result
        result_folder_path = 'scrapers/' + scraper + '/result'

        # get the scraper name (also the result name)
        scraper_name = scraper.split('/')[-1]

        # list all the files inside result folder
        result_files = os.listdir(result_folder_path)

        # loop over those files
        for file in result_files:
            # get the dataframes from those files
            df = pd.read_csv(result_folder_path + '/' + file)

            # if the df is not empty
            if df.shape[0] > 0:

                # analyze the job description
                result_df = AnalyzeDescription(df)

                # convert the result to csv without saved 
                UploadDataFrameToS3(result_df, scraper_name, file)

                


if __name__ == '__main__':
    main()