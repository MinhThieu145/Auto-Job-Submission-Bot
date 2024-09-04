import streamlit as st
import boto3

import pandas as pd

# Some Name
BUCKET_NAME = 'job-description-process'
FOLDER_NAME = 'indeed-scraper'

# get instance id
def get_instance_id(ec2_client):
    instance_id = ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['InstanceId']
    return instance_id

# get instance type
def get_instance_type(ec2_client):
    instance_type = ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['InstanceType']
    return instance_type

# get the availability zone
def get_availability_zone(ec2_client):
    availability_zone = ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
    return availability_zone


def main():

    st.title("Welcome to my multi-tier AWS architecture!")

    st.divider()

    st.subheader('Some info about Ec2')

    # get client 
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    # get instance id
    instance_id = get_instance_id(ec2_client)
    st.write("Instance ID: ", instance_id)

    # get instance type
    instance_type = get_instance_type(ec2_client)
    st.write("Instance Type: ", instance_type)

    # get availability zone
    availability_zone = get_availability_zone(ec2_client)
    st.write("Availability Zone: ", availability_zone)

    # divider
    st.divider()

    # get some files in there
    s3_client = boto3.client('s3', region_name='us-east-1')

    # List objects in the specified folder
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f'{FOLDER_NAME}/')
    df_dict = {}
    for obj in response['Contents']:
        st.write(obj['Key'])

        

        # if that file is a csv, then read it to a dataframe
        if obj['Key'].endswith('.csv'):
            # the name of the dataframe is the name of the file without the .csv
            df_name = obj['Key'].split('/')[-1].split('.')[0]
            # read the csv
            df = pd.read_csv(f's3://{BUCKET_NAME}/{obj["Key"]}')

            # add the dataframe to the dictionary
            df_dict[df_name] = df

    # create a dropdown menu to select the dataframe
    df_name_list = st.selectbox('Select a dataframe', list(df_dict.keys()))

    # display the dataframe
    st.dataframe(df_dict[df_name_list])



        
        




if __name__ == "__main__":
    main()