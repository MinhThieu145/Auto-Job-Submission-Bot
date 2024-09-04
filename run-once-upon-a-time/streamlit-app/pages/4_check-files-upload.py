import streamlit as st

import pandas as pd
import os

# random
import random

# boto3
import boto3

# Constant
BUCKET_NAME = 'job-site-scrapers-home'

def main():
    st.title("Check Files Upload")

    # get the current folder
    current_dir = os.getcwd()
    st.write(f"Current directory: {current_dir}")

    # list all the folders in the current directory
    folder_list = os.listdir(current_dir)
    scraping_dir_name = st.selectbox('Please select the folder store your scraping files', folder_list)

    # merge the current directory with the scraping directory
    scraping_dir = os.path.join(current_dir, scraping_dir_name)

    scraping_dir_list = os.listdir(scraping_dir)
    # only folder for scraping_dir_list
    scraping_dir_list = [folder for folder in scraping_dir_list if os.path.isdir(os.path.join(scraping_dir, folder))]
    # find a folder called result in the scraping_dir_list
    if 'result' in scraping_dir_list:
        st.success('Good! You have a folder to store result')

        # list all the files in the result folder, only if they are csv files
        result_dir = os.path.join(scraping_dir, 'result')
        result_file_list = os.listdir(result_dir)
        result_file_list = [file for file in result_file_list if file.endswith('.csv') and file is not None]
        # create a selectbox to select the file
        result_file = st.selectbox('Select a file in the result list', result_file_list)

        # print the content of the file
        if result_file.endswith('.csv'):
            # write csv file dataframe

            # if the file is empty, then write a warning
            if os.stat(os.path.join(result_dir, result_file)).st_size == 0:
                st.warning('The file is empty')
            else:
                df = (pd.read_csv(os.path.join(result_dir, result_file)))
                st.dataframe(df)

                # get the list of columns in the csv file
                column_list = df.columns.tolist()
                # print out the column list
                st.write(column_list)

                # check if
                # the first column is called job_title
                # the second column is called job_link
                # the third column is called description

                if column_list[0] == 'job_title' and column_list[1] == 'job_link' and column_list[2] == 'description':
                    st.success('The file is in the correct format')

                    # if it in the correct format. Time to upload to S3 database

                    # get the folder from folder_name session state
                    # get all files
                    st.markdown(f'Please make sure. Is this the Bucket you want to upload : **{BUCKET_NAME}**')
                    st.markdown(f'Please make sure. Is this the folder you want to upload: **{scraping_dir_name}**')

                    # get the folder name
                    st.write(os.listdir(scraping_dir))         


                    # a button said I'm sure
                    if st.button('Yes, I am sure'):
                        
                        # delete the result folder before upload
                        with st.spinner('Deleting the result folder'):
                            # delete the folder
                            for root, dirs, files in os.walk(result_dir):
                                for file in files:
                                    os.remove(os.path.join(root, file))
                                for dir in dirs:
                                    os.rmdir(os.path.join(root, dir))
                            os.rmdir(result_dir)

                        with st.spinner('Uploading the file to S3'):
                            s3_client = boto3.client('s3')
                            # upload the file to S3
                            for root, dirs, files in os.walk(scraping_dir):
                                for file in files:
                                    local_path = os.path.join(root, file)
                                    s3_key = os.path.relpath(local_path, scraping_dir)
                                    s3_key = os.path.join(scraping_dir_name, s3_key)

                                    s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
                        st.success('Upload successfully')
                else:
                    st.warning('The file is not in the correct format. Please follow Rule 5')


        # a button to delete the folder
        st.subheader('If you want to start over, please click the button below')
        if st.button('Delete the folder'):
            with st.spinner('Deleting the folder'):
                # delete the folder
                for root, dirs, files in os.walk(scraping_dir):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                os.rmdir(scraping_dir)
            st.success('Delete successfully')

        
    else:
        st.warning('Please create a folder called result to store the result')

        # End the game. Delete the folder
        st.subheader('Congratulations! You have finished the game. Please click the button below to delete the folder')
        if st.button('Delete the folder'):
            with st.spinner('Deleting the folder'):
                # delete the folder
                for root, dirs, files in os.walk(scraping_dir):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                os.rmdir(scraping_dir)
            st.success('Delete successfully')


if __name__ == '__main__':
    main()