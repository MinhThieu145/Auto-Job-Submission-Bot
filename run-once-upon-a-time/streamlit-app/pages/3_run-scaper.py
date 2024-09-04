import streamlit as st

import os
import subprocess


def StoreState(name, value=None):
    if value is None:
        # return the value
        return st.session_state[name]
    else:
        # set the value
        st.session_state[name] = value



def main():
    st.title("Run Python Scraper")

    if StoreState('folder_name') != '' and StoreState('folder_name') is not None:
        st.write(f"Folder name: {[StoreState('folder_name')]}")

        # get the list of files in the folder
        file_list = os.listdir(st.session_state['folder_name'])
        st.write(file_list)

        # create a selectbox to select the file
        file_name = st.selectbox('Select a file', file_list)

        # check if the file_name is a python file and is it main.py
        if file_name.endswith('.py') and file_name == 'main.py':
            # write the content of the file
            code = st.code(open(os.path.join(st.session_state['folder_name'], file_name)).read())

            # check a few things in the code
            # check if there is '--headless=new' in the code
            if '--headless=new' in code:
                st.success('Good! You are using the new headless mode')
            else:
                st.warning('Please use the new headless mode')

            # check if --no-sandbox is in the code
            if '--no-sandbox' in code:
                st.success('Good! You are using --no-sandbox')
            else:
                st.warning('Please use --no-sandbox')

            # then if it is a main.py file, then has a button to run the scraper
            if st.button('Run Scraper'):
                # run and get result with subprocess and check_output
                with st.spinner('Running the scraper...'):  
                    folder_path = os.path.join(os.getcwd(),st.session_state['folder_name'])
                    script_path = os.path.join(folder_path, file_name)
                    script_name = file_name

                    st.write(folder_path, script_path, script_name)  
                    result = subprocess.run(['python', script_path], cwd=folder_path, capture_output=True,).stdout
                    # write the result
                    st.write([result])


        # if it not a main.py file, then write a warning
        elif file_name.endswith('.py') and file_name != 'main.py':
            st.warning('Please named your main scraper as main.py')

        # elif it is not a python file, then write a warning
        else:
            st.warning('Please select a python file')


        st.divider()
        # select folder again button
        if st.button('Select another folder'):
            StoreState('folder_name', '')
    else:
        with st.form('Select a folder'):
            st.warning("No folder name found. Please upload files first or enter a folder name manually")

            # get the list of folder in the current directory
            folder_list = os.listdir()
            st.write(folder_list)    

            # only get the folder names in folder_list
            folder_list = [folder for folder in folder_list if os.path.isdir(folder)]

            # create a folder name input
            folder_name = st.selectbox('Select a folder name', folder_list)
            st.write(folder_name)

            # create a submit button
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                # save the folder name to session state
                st.session_state['folder_name'] = folder_name

if __name__ == "__main__":
    main()