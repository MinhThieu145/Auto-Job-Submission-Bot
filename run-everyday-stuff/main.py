# import package
import boto3
import pandas as pd
import numpy as np

import os
import subprocess

# Some constants
BUCKET_NAME = 'job-site-scrapers-home'
BUCKET_NAME_RESULT = 'job-scraping-result'

local_directory = 'scrapers' # this is a folder to store result

# import the openai script
import importlib
open_ai_script = "openai-analyze-job-description"
open_ai = importlib.import_module(open_ai_script)

# get the folder in S3
def ListS3TopLevel(bucket_name):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    folders = []
    for prefix in response.get('CommonPrefixes', []):
        folder_name = prefix.get('Prefix')
        folders.append(folder_name)

    return folders


# download the folder
def DownloadFolder(bucket_name, folder_name, local_dir):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    for obj in response.get('Contents', []):
        file_key = obj.get('Key')
        local_path = os.path.join(local_dir, file_key)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3.download_file(bucket_name, file_key, local_path)


def CreateScraperFolder():
    # if exist, delete the folder
    if os.path.exists('scrapers'):
        subprocess.run(['rm', '-rf', 'scrapers'])
    subprocess.run(['mkdir', 'scrapers'])

    folder_list = ListS3TopLevel(BUCKET_NAME)
    for folder in folder_list:
        DownloadFolder(BUCKET_NAME, folder.rstrip('/'), local_directory)


# upload to a bucket called job-scraping-result
def UploadJobScrapingResult(folder_name, file, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, BUCKET_NAME_RESULT, folder_name + '/' + file)

# get the result inside each scraper folder
def GetResultandUploadS3(result_folder_path, folder_name):

    # list all the files inside result folder
    result_files = os.listdir(result_folder_path)

    csv_files = [file for file in result_files if file.endswith('.csv')]

    # add the date to folder_name
    folder_name = folder_name + '/' + str(pd.datetime.now().date())

    # upload the file to s3
    for file in csv_files:
        file_path = f'{result_folder_path}/{file}'
        UploadJobScrapingResult(folder_name=folder_name, file=file, file_path=file_path)


def main():

    # Create scrapers folder. This is the folder with all of our scrapers:
    CreateScraperFolder()

    # now get the scrapers folder
    scrapers_folder = os.listdir(local_directory)
    for folder in scrapers_folder:
        print(folder)

        # Run the scraper inside each folder
        folder_path = os.path.join(os.getcwd(), 'scrapers', folder)

        # get the script path: main.py in each folder
        script_path = os.path.join(folder_path, 'main.py')

        # run the script
        result = subprocess.run(['python3', script_path], cwd=folder_path, capture_output=True)
        print(result.stdout.decode('utf-8'))    

        # Okay. Now we have a folder called result in each scraper. Put them to S3 bucket

        # folder name of folder_path
        folder_name = folder_path.split('/')[-1]
        print('folder_name:', folder_name)
        result_folder_path = os.path.join(folder_path, 'result')
        print(result_folder_path)

        GetResultandUploadS3(result_folder_path, folder_name)

        # now after done, run the openai script for the scraper folder
        open_ai.main()

        # after that, remove the scraper folder
        subprocess.run(['rm', '-rf', folder_path])
       



if __name__ == '__main__':
    main()