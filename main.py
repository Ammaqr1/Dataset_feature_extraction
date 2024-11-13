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
    st.write(df3.head())
    print(df3.head())
    st.sidebar.write(old_features)
    st.write(df.columns)
        

    
    
    


# # Main heading
# st.title("Welcome to My App! 👋")

# # Brief introduction
# st.write("""
# Hello and welcome! This application is designed to provide insights and interactive tools for exploring datasets, 
# running machine learning models, and visualizing results. Whether you're here to analyze data, 
# learn about machine learning, or just explore, you've come to the right place!
# """)

# # Display an image or logo (replace with your image path or URL)
# st.image("https://your-image-url.com/logo.png", width=300)

# # A call-to-action button to start the experience
# if st.button("Get Started"):
#     st.write("You clicked the button! Navigate through the sidebar to explore different features.")
# else:
#     st.write("Use the button above to begin!")

# # Sidebar for navigation (optional)
# st.sidebar.header("Navigation")
# st.sidebar.write("Choose an option from below:")
# st.sidebar.button("Explore Data")
# st.sidebar.button("Run Model")
# st.sidebar.button("Visualize Results")

# # Footer text
# st.markdown("---")
# st.markdown("Created with ❤️ by [Your Name](https://your-linkedin-profile.com)")


#  st.header("Solve Your problem using through Image")
#     input_text = st.text_input("Input Prompt: ", key="input")
#     uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
#     image = ""   
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Image.", use_column_width=True)

#     submit = st.button("Start Solving")
    
#     if submit:
#         response = app.get_gemini_response(input_text, image)
#         st.subheader("The Response is")
#         st.write(response)
