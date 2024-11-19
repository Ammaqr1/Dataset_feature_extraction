import streamlit as st
import pandas as pd
from database_connection import SQLiteDatabase
import json
import time
from feature_extractor import Feature_extra
from data_chat import DataChat



def navigate(page):
    st.session_state.page = page
    
if 'df' not in st.session_state:
    st.session_state.df = None
    
if 'df1' not in st.session_state:
    st.session_state.db_name = None
    
if 'no' not in st.session_state:
    st.session_state.tb_name = 0
    
    
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
    with st.spinner('Saving your dataframe into db'):
        sqlite.connect('titanic_data.db')
        sqlite.create_json_table('new_table_df')
        sqlite.insert_json(st.session_state.df,'new_table_df')
    df1 = sqlite.retrieve_all_json('new_table_df')
    data_dict = json.loads(df1[-1])
    df1 = pd.DataFrame(data_dict)
    
    st.write(df1.head())
    st.subheader('Ask any question related to the Dataset')
    Dc = DataChat(df1.head())
    prompt = st.chat_input('Ask anything related to Dataframe')
    
    if prompt:
        answer = Dc.chatbot(prompt)
        st.write(answer)
    
    no = st.sidebar.text_input('Enter your no of features are needed')
    if st.sidebar.button('Go to see the features') and int(no):
        
        st.session_state.df1 = df1
        st.session_state.no = no
        # st.write(df1)
        st.button('Navigate to the next page')
        navigate('feature_extraction')
        st.rerun()
        
        
elif st.session_state.page == 'feature_extraction':
    models_list = ['gemma-7b-it','llama3-8b-8192']
    old_features = st.session_state.df1.columns
    no = st.session_state.no
    df = st.session_state.df1
    if st.button('Run'):
        
        for i in range(int(no)):
            fe = Feature_extra(df,models_list[0])
            df,insight = fe.feature_extracting()
            
            
    st.write(df.head())
    print(df.head())
    st.sidebar.subheader('Old Features')
    st.sidebar.write(old_features)
    st.subheader('Newly created Features')
    st.write(df.columns)
        

    
