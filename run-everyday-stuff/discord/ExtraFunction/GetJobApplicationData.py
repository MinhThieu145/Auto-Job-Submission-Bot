import discord 
from discord.ext import commands
from discord import app_commands

# irrelevant stuff
import datetime
import boto3
import pandas as pd

# secret token
BUCKET_NAME_RESULT = 'job-description-process'

def GetDataAndDataframe():
    
    # data result as dataframe
    scraper_result = {}

    # boto client
    s3 = boto3.client('s3')
    # list all directories
    response = s3.list_objects_v2(Bucket=BUCKET_NAME_RESULT, Delimiter='/')
    print('all scrapers: ', response)


    # Go to each folder and go to the folder with the following name: result-2021-08-01 (replace with current date)
    # get the result from the folder
    for prefix in response.get('CommonPrefixes', []):
        dir_name = prefix.get('Prefix')
        scraper_name = dir_name.split('/')[0]

        print('dir_name: ', dir_name)

        # Check if the directory matches the desired name format
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # the folder name
        folder_name = 'result-'+current_date+'/'
        print('folder_name: ', folder_name)

        # list object inside the folder
        response = s3.list_objects_v2(Bucket=BUCKET_NAME_RESULT, Prefix=f'{dir_name}{folder_name}')

        # key is the file name, value is the dataframe
        result = {}

        for obj in response.get('Contents', []):
            # if it is csv file, then proceed
            if obj.get('Key').endswith('.csv'):

                file_key = obj.get('Key')

                # read the file with pandas
                df = pd.read_csv(f's3://{BUCKET_NAME_RESULT}/{file_key}')

                # get the number of row
                num_row = df.shape[0]
                # get the file name
                file_name = file_key.split('/')[-1]

                # remove the .csv from the file name
                file_name = file_name.replace('.csv', f': **{num_row} jobs**')

                # now add the file name and the file content (dataframe) to the result dict
                result[file_name] = df

        # key of dict is the scraper name, value is the result dict
        scraper_result[scraper_name] = result
    return scraper_result
def main():
    pass


