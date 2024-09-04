import streamlit as st
    
import datetime
import time


st.set_page_config(page_title="Job Automation", page_icon=":work:" )

st.title("Job Automation")

st.write('''
    Welcome to my job automation app. Hope we have a great time together. There are a few rules you need to follow in order for the app to work properly!
''')
         
st.divider()
        
st.markdown("**Rule 1:** Always start from the homepage an end with check-files-upload page (from top to bottom). The only exception is when you reload the app,\
            then you can start from any pages you want, but read the warning carefully.")

st.markdown('''**Rule 2:** I will briefly explain the process and what each tab does. This app allows you (or, another me, I would say) to automate the job\
                 scraping and application submission process. Read 3 rules below to know which each tab does specifically
            ''')

st.markdown('''**Rule 3:** *uload-save-files* allows you to load the *main scraper*(or the script that you need to run), all the supplementary files\
            like cookies, list of job titles or smaller scripts,... Select **EXACTLY** the number of files you want to upload (do not left a upload tray empty)   
            You then enter the folder name, this will be the name of the folder for your scrapers, and it will be upload to S3 under the same name.\
            I suggest you to use the name that make sense, such as linkedin-scraper, indeed-scraper,... just for your convenience.\
''')

st.markdown('''**Rule 4:** *run-scraper* will first prompt you to choose a folder if you reload the app. If you haven't created a folder,\
            please go back to create a folder and upload files you need. You won't have to do anything if you don't reload the app.   
            The next step is to select a file that you want to run (your main scraper). However, your main script should always be named as *main.py*\
            Trust me, it is easier. 
''')
            
st.markdown('''**Rule 5:** Your result need to follow this certain format in order for the app to work properly (even the name of the column need to be the same):   
            - **firt column**: job title (this is the name of the position such as Data Analyst, Data Engineer), while it may not be very obvious,\
            something like: Data Analyst Fall 2021, or some shit like that is still okay. I'll clean them later on.   
            - **second column:** job link (the link to the original post)   
            - **third column:** description (the description of the job, what it is about).     
            *For other column, you can have it your way.*
            
''')
            

st.divider()

st.markdown(''' This is the end of the instruction, please read carefully and adhere the rules. **Good luck with your job search!**
''')


