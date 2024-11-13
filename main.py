import streamlit as st
import pandas as pd
from database_connection import SQLiteDatabase
import json
import time
from feature_extractor import Feature_extra



def navigate(page):
    st.session_state.page = page
    
if 'df' not in st.session_state:
    st.session_state.df = None
    
if 'df1' not in st.session_state:
    st.session_state.db_name = None
    
if 'tb_name' not in st.session_state:
    st.session_state.tb_name = None
    
    
# # Set page configuration
st.set_page_config(page_title="Welcome to My App", page_icon="👋", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
    
    
if st.session_state.page == 'welcome':
    st.title("Welcome to My App! 👋")
    st.header("Solve Your problem using through Image")
    uploaded_file = st.file_uploader("Choose an csv dataset...", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())
        
    submit = st.button("Start uploadint to sqlite")
    
    if submit:
        with st.spinner('Converting_dat and saving to sqlite database'):
            df = df.to_json()
            st.session_state.df = df
            navigate('sqlite')
            st.rerun()
    
elif st.session_state.page == 'sqlite':
    sqlite = SQLiteDatabase()
    # db_name = st.text_input('Please enter your database name')
    # tb_name = st.text_input('Please entera table_name name')
    # if st.button('Submit',key='db_tb_name') and db_name and tb_name:
    #     pass
    with st.spinner('Saving your dataframe into db'):
        sqlite.connect('titanic_data.db')
        sqlite.create_json_table('new_table_df')
        sqlite.insert_json(st.session_state.df,'new_table_df')
    df1 = sqlite.retrieve_all_json('new_table_df')
    data_dict = json.loads(df1[-1])
    df1 = pd.DataFrame(data_dict)
    st.session_state.df1 = df1
    st.write(df1)
    with st.spinner('Navingating to new page for feature extraction'):
        time.sleep(2)
        navigate('feature_extraction')
        st.rerun()
        
        
elif st.session_state.page == 'feature_extraction':
    models_list = ['gemma-7b-it','llama3-8b-8192']
    old_features = st.session_state.df1.columns
    # no = st.text_input('Enter your no of features are needed')
    df = st.session_state.df1
    # if st.button('Sumbit and run') and int(no):
        
        # for i in range(int(no)):
    fe = Feature_extra(df,models_list[0])
    df3,insight = fe.feature_extracting()
    st.header('New_column_created')
    st.write(df3.head())
    print(df3.head())
    st.sidebar.header('old_columns')
    st.sidebar.write(old_features)
    st.write(df.columns)
        

    
    
    
