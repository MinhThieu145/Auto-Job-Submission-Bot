import streamlit as st
import pandas as pd
import numpy as np
import shutil

import os
import subprocess
import time 
# use state of streamlit to store the variables
def StoreState(name, value=None):
    if value is None:
        # return the value
        return st.session_state[name]
    else:
        # set the value
        st.session_state[name] = value


# save file to folder and cache the function
def save_file(file, folder_name):
    # write the file to the folder with the same name and extension
    with open(os.path.join(folder_name, file.name), 'wb') as f:
        f.write(file.getbuffer())
        st.success(f'File {file.name} saved successfully')

# main function
def main():
    st.title('Job Reciever')

    # ask how many files you want to upload
    num_files = st.number_input('How many files do you want to upload?', min_value=1, max_value=10, value=1)

    # create the number of file uploaders based on the number of files
    with st.form('File Uploader'):
        files = []
        for i in range(num_files):
            # append the file to the list if the file is not None
            file = st.file_uploader(f'File {i+1}')
            if file:
                files.append(file)
            else:
                st.warning(f'File {i+1} is not uploaded')

        # Save the files to StoreState
        StoreState('files', files)

        # create a folder
        folder_name = st.text_input('Enter a folder name')
        StoreState('folder_name', folder_name)

        # save all the files in the folder
        if st.form_submit_button('Submit'):
            if folder_name:
                if os.path.exists(folder_name):
                    st.error('Folder already exists and will be overwritten')
                    
                    # delete the folder
                    shutil.rmtree(folder_name)
                    # create the folder
                    os.makedirs(folder_name, exist_ok=False)
                    # save files to the folder
                    for i, file in enumerate(StoreState('files')):
                        save_file(file, StoreState('folder_name'))
                else:
                    # create the folder
                    os.makedirs(folder_name, exist_ok=False)
                    # save files to the folder
                    for i, file in enumerate(StoreState('files')):
                        save_file(file, StoreState('folder_name'))

                        st.write(file)


# run the app
if __name__ == '__main__':
    main()