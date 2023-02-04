import sqlite3
import streamlit as st
import pandas as pd
from pandasql import sqldf
import openai
import numpy as np
import graphviz as graphviz

# Library created to store df_matching from main_page to page2
import df_matching

# Library created to store user inputs from main_page to page2
import input_store

# Computer Vision Program to estimate face beauty
import howcuteami

# App Introduction
def introduction():
    st.markdown("<h1 style='text-align: center; color: lightblue;'>Renovated Tinder App</h1>", unsafe_allow_html=True)
    st.caption("<h1 style='text-align: center;'>By Tobi Bui</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: left; color: red;'>Introduction about the project</h1>", unsafe_allow_html=True)
    st.subheader('1: Project Purposes')
    st.markdown("""The objective of my project is to understand the structure of Tinder and implement decision tree algorithm to do the best matching.
                I developed separated table filter based on the user selection to do the matching activities. The filter has a total of 10 filter layers
                in general. Additionally, I implemented the OpenAI's engine GPT-3 to support my response in convincing people to use the app (a mini chatbot kind alike) as well as
                developing a Computer Vision Algorithm which detects a person's face and evaluate gender, age and beauty score based on the Golden Face Ratio. 
""")
    st.subheader('2: How the system works')
    agree = st.checkbox('Do you want to see the system design graph?')
    if agree:
        st.graphviz_chart('''
            digraph {
            fontname="Helvetica,Arial,sans-serif"
            node [fontname="Helvetica,Arial,sans-serif"]
            edge [fontname="Helvetica,Arial,sans-serif"]
            graph [
            rankdir = "LR"
            ];
            node [
            fontsize = "16"
            shape = "ellipse"
            ];
            edge [
            ];
            "node0" [
            label = "<f0> Have you used online dating app(s) before?| Yes | No"
            shape = "record"
            ];
            "node1" [
            label = "<f0> Yes Table| Name | Age | Gender | Have you used online dating app(s) before? | How often do you use online dating app(s)? | What are you looking for in online dating app(s)? | How long have you used online dating app(s)? |Do you prefer dating app(s) to have more interactive ice breaker activities? | Do you prefer to have a certain number, but selective profiles or unlimited profiles recommended per day? | Have you experienced ghosting or being ghosted? | What's your overall experience using online dating app(s)?  "
            shape = "record"
            ];
            "node2" [
            label = "<f0> No Table| Name | Age | Gender | Have you used online dating app(s) before? | What’s the main reason you haven’t used any dating app? | Do you intend to use any online dating app? "
            shape = "record"
            ];
            "node3" [
            label = "<f0> Male | Male vs Male | Male vs Female"
            shape = "record"
            ];
            "node4" [
            label = "<f0> Female| Female vs Female | Male vs Female |-1"
            shape = "record"
            ];
            "node5" [
            label = "<f0> Do you want to join the beauty matching feature? "
            shape = "record"
            ];
            "node6" [
            label = "<f0> No "
            shape = "record"
            ];
            "node7" [
            label = "<f0> Yes "
            shape = "record"
            ];
            "node8" [
            label = "<f0> Name | Gender | Beauty Score "
            shape = "record"
            ];
            "node0":f0 -> "node1":f0 [
            id = 0
            ];
            "node0":f1 -> "node2":f0 [
            id = 1
            ];
            "node1":f0 -> "node3":f0 [
            id = 2
            ];
            "node1":f1 -> "node4":f0 [
            id = 3
            ];
            "node2":f0 -> "node3":f0 [
            id = 4
            ];
            "node2":f1 -> "node4":f0 [
            id = 5
            ];
            "node2":f1 -> "node5":f0 [
            id = 6
            ];
            "node5":f1 -> "node6":f0 [
            id = 7
            ];
            "node5":f1 -> "node7":f0 [
            id = 8
            ];
            "node6":f1 -> "node3":f0 [
            id = 9
            ];
            "node6":f1 -> "node4":f0 [
            id = 10
            ];
            "node7":f1 -> "node8":f0 [
            id = 11
            ];
            }
        ''')
    
    st.markdown("<h1 style='text-align: left; color: red;'>Features</h1>", unsafe_allow_html=True)
    st.markdown(" - Automatically update dataframe after every submission")
    st.markdown(" - Filter out dataframe based on user options")
    st.markdown(" - Apply OpenAi's GPT-3 engine to convince users to use the app")
    st.markdown(" - Evaluate a person's age, gender, beauty for matching using Computer Vision algorithm")
    st.markdown(" - Efficiently matching with decision tree algorithm without support libraries besides pandas and numpy")
        
    st.write("---")
    
def main_page():
    st.sidebar.markdown("# Users Input")
    
    #connect to database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Define 2 dataframe representing 2 different scenario of the survey
    df_yes = None
    df_no = None

    st.title("Add User")
    
    #create a table 
    #cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    #query to fetch data from the database
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    #get user input
    name = st.text_input("Name: ")
    input_store.name = name
    
    age = st.number_input("Age: ", 18,60)
    input_store.age = age
    
    gender = st.radio('Gender', ['Male', 'Female'])
    input_store.gender = gender
    
    usage = st.radio('Have you used online dating app(s) before?', ['Yes', 'No'])
    input_store.usage = usage
    
    if usage == 'Yes':
        frequency = st.radio('How often do you use online dating app(s)?', ['Frequently', 'Occasionally', "Rarely"])
        input_store.frequency = frequency
        
        relationship_status = st.radio('What are you looking for in online dating app(s)?', ['Long-term', 'Short-term', "I don't know"])
        input_store.relationship_status = relationship_status
        
        app_usage =  st.radio('How long have you used online dating app(s)?', ['1-6 months', 'Approximately 1 year', "More than 1 year"])
        input_store.app_usage = app_usage
        
        ice_breaker = st.radio('Do you prefer dating app(s) to have more interactive ice breaker activities?', ['Yes', 'No'])
        input_store.ice_breaker = ice_breaker
        
        recommendation = st.radio('Do you prefer to have a certain number, but selective profiles or unlimited profiles recommended per day?', ['Certain but selective profiles', 'Unlimited profiles'])
        input_store.recommendation = recommendation
        
        ghost =  st.radio('Have you experienced ghosting or being ghosted?', ['Ghosting', 'Being ghosted', 'Both','Neither'])
        input_store.ghost = ghost
        
        overall = st.radio("What's your overall experience using online dating app(s)?", ['Very positive', 'Positive', 'Negative','Very negative'])
        input_store.overall = overall
        
    else:
        reason = st.radio('What’s the main reason you haven’t used any dating app?', ['am not interested', 'Prefer real connection over online dating', 'Other (specify)'])
        input_store.reason = reason 
        
        # Creating AI response from the user reason input for better convince
        if reason == 'am not interested':
            prompt = "Can you convince me to use Tinder if I" + " " + reason + " " + "in it"
        
        elif reason == 'Prefer real connection over online dating':
            prompt = "Can you convince me to use Tinder if I" + " " + reason
        
        else:
            comment = st.text_area("Please provide more details")
            prompt = "Can you convince me to use Tinder based on the following sentence:" + " " + comment
            
        intend = st.radio('Do you intend to use any online dating app?', ['Yes', 'No'])
        input_store.intend = intend
        
        # Chat GPT Application
        if intend == "No":
            openai.api_key = "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"
            model_engine = "text-davinci-003"

            completion = openai.Completion.create(
                engine = model_engine,
                prompt = prompt,
                max_tokens = 1024,
                n = 1,
                stop = None,
                temperature = 0.5,
            ) 

            response = completion.choices[0].text
            st.markdown(response)
    
    button = st.button("Submit")
    if button:
        input_store.input_list = []
        if usage == 'Yes':
            columns = ["gender TEXT", "usage TEXT", "frequency TEXT", "relationship_status TEXT", "app_usage TEXT", "ice_breaker TEXT", "recommendation TEXT", "ghost TEXT", "overall TEXT"]
            for column in columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column}")
                except:
                    pass

            cursor.execute("INSERT INTO users (name, age, gender, usage, frequency, relationship_status, app_usage, ice_breaker, recommendation, ghost,overall) VALUES (?, ?, ?,?,?,?,?,?,?,?,?)", (name, age, gender, usage, frequency, relationship_status, app_usage, ice_breaker, recommendation,ghost,overall))
            conn.commit()
            st.success("User added successfully!")
            last_id = cursor.lastrowid
            rows = cursor.execute("SELECT * FROM users").fetchall()

            #create a dataframe from the query results
            df = pd.DataFrame(rows, columns=["id", "name", "age","gender", "usage", "frequency", "relationship_status", "app_usage", "ice_breaker","recommendation",'ghost','overall','a','b'])
            df['id'] = last_id

            st.write("Users' data")
            
            # Create new column based on the user's age input to merge to 1 specific range
            df = sqldf("SELECT *, CASE WHEN age BETWEEN 18 AND 24 THEN '18 to 24' WHEN age BETWEEN 24 AND 34 THEN '24 to 34' ELSE '35+' END AS 'What is your age?' FROM df")
            df_yes = df
        
        else:
            columns = [("gender", "TEXT"), ("usage", "TEXT"), ("reason", "TEXT"), ("intend", "TEXT")]
            for column in columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column[0]} {column[1]}")
                except:
                    pass
            
            cursor.execute("INSERT INTO users (name, age, gender, usage, reason,intend) VALUES (?, ?, ?,?,?,?)", (name, age, gender, usage, reason, intend))
            conn.commit()
            st.success("User added successfully!")
            last_id = cursor.lastrowid
            rows = cursor.execute("SELECT * FROM users").fetchall()

            #create a dataframe from the query results
            df1 = pd.DataFrame(rows, columns=["id", "name", "age","gender", "usage", "reason", "intend",'a','b','c','d','e','f','g'])
            df1['id'] = last_id

            st.write("Users' data")
            
            # Create new column based on the user's age input to merge to 1 specific range
            df1 = sqldf("SELECT *, CASE WHEN age BETWEEN 18 AND 24 THEN '18 to 24' WHEN age BETWEEN 24 AND 34 THEN '24 to 34' ELSE '35+' END AS 'What is your age?' FROM df1")
            df_no = df1

    conn.close()

    if usage == "Yes":
        if button:
            df_yes_backup = df_yes.copy()
            
            # Rename column
            df_yes_backup = df_yes_backup.rename(columns={"frequency": "How often do you use online dating app(s)?","relationship_status": "What are you looking for in online dating app(s)?", "a": "What is the main reason you have not used any dating app?", "b": "Do you intend to use any online dating app?","app_usage": "How long have you used online dating app(s)?", "ice_breaker": "Do you prefer dating app(s) to have more interactive ice breaker activities?", "recommendation":"Do you prefer to have a certain number, but selective profiles or unlimited profiles recommended per day?", "ghost": "Have you experienced ghosting or being ghosted?", "overall": "What's your overall experience using online dating app(s)?"})
            
            # Copy the data from yes for matching dataframe
            df_matching.df_matching = df_yes_backup
            
            #Display all dataframe
            st.write(df_yes_backup)
            
            # Split Yes from the data
            df_yes_split = sqldf("SELECT * FROM df_yes_backup where usage = 'Yes' ")
            
            # Drop column
            df_yes_split = df_yes_split.drop(['Do you intend to use any online dating app?', "What is the main reason you have not used any dating app?"], axis=1)
            
            # Copy the data from yes response only for matching dataframe
            df_matching.df_matching_yes = df_yes_split
            
            #Display yes dataframe
            st.write(df_yes_split)
            
            # Split no from the data
            df_no_split = sqldf("SELECT * FROM df_yes_backup where usage = 'No' ")
            
            # Drop column
            df_no_split = df_no_split.drop(['How often do you use online dating app(s)?', 'What are you looking for in online dating app(s)?','How long have you used online dating app(s)?',"Do you prefer dating app(s) to have more interactive ice breaker activities?","Do you prefer to have a certain number, but selective profiles or unlimited profiles recommended per day?", "Have you experienced ghosting or being ghosted?", "What's your overall experience using online dating app(s)?"], axis=1)

            # Copy the data from no response for matching dataframe
            df_matching.df_matching_no = df_no_split
            
            #Display no dataframe
            st.write(df_no_split)
        
    else:
        if button:
            df_no_backup = df_no.copy()
            
            # Rename column
            df_no_backup = df_no_backup.rename(columns={"reason": "How often do you use online dating app(s)?", "intend": "What are you looking for in online dating app(s)?", "a":"How long have you used online dating app(s)?", "b":"Do you prefer dating app(s) to have more interactive ice breaker activities?", "c":"Do you prefer to have a certain number but selective profiles or unlimited profiles recommended per day?", "d": "Have you experienced ghosting or being ghosted?", "e": "What's your overall experience using online dating app(s)?","f": "What's the main reason you haven't used any dating app?", "g": "Do you intend to use any online dating app?" })

            # Copy the data from no for matching dataframe
            df_matching.df_matching = df_no_backup
            
            #Display all dataframe
            st.write(df_no_backup)

            # Split Yes from the data
            df_yes_split = sqldf("SELECT * FROM df_no_backup where usage = 'Yes' ")

            # Drop column
            df_yes_split = df_yes_split.drop(["What's the main reason you haven't used any dating app?", 'Do you intend to use any online dating app?'], axis=1)

            # Copy the data from yes response only for matching dataframe
            df_matching.df_matching_yes = df_yes_split
            
            #Display yes dataframe
            st.write(df_yes_split)

            # Split no from the data
            df_no_split = sqldf("SELECT * FROM df_no_backup where usage = 'No' ")

            # Drop column
            df_no_split = df_no_split.drop(['How often do you use online dating app(s)?', 'What are you looking for in online dating app(s)?','How long have you used online dating app(s)?','Do you prefer dating app(s) to have more interactive ice breaker activities?',"Do you prefer to have a certain number but selective profiles or unlimited profiles recommended per day?","Have you experienced ghosting or being ghosted?", "What's your overall experience using online dating app(s)?"], axis=1)

            # Copy the data from no response only for matching dataframe
            df_matching.df_matching_no = df_no_split
            
            #Display no dataframe
            st.write(df_no_split)

    # Create dictionary to store all the input
    if usage == 'Yes':
        # List of inputs from Yes user
        list = [input_store.name, input_store.age, input_store.gender, input_store.usage, input_store.frequency, input_store.relationship_status, input_store.app_usage, input_store.ice_breaker, input_store.recommendation, input_store.ghost, input_store.overall]
        
        # Store user inputs in list for matching purpose
        for i in list:
            input_store.input_list.append(i)
        
        # Store user inputs in dictionary for clear display information
        input_store.input_dict = {'Name' : input_store.name, 'Age':input_store.age, "Gender":input_store.gender, "Usage":input_store.usage, "Frequency": input_store.frequency, "Relationship_status": input_store.relationship_status, "App_usage":input_store.app_usage, "Ice_breaker": input_store.ice_breaker, "Recommendation": input_store.recommendation, "Ghost": input_store.ghost, "Overall": input_store.overall}
    
    else:
        # List of inputs from No user
        list = [input_store.name, input_store.age, input_store.gender,  input_store.usage, input_store.reason, input_store.intend]
        
        # Store user inputs in list for matching purpose
        for i in list:
            input_store.input_list.append(i)
        
        # Store user inputs in dictionary for clear display information
        input_store.input_dict = {'Name' : input_store.name, 'Age':input_store.age, "Gender":input_store.gender, "Usage": input_store.usage, "Reason" : input_store.reason, "Intend": input_store.intend}
    
#Copy the data collected from main_page to page2
df_page2 = df_matching.df_matching

def page2():
    st.markdown("# Matching Recommendation ")
    st.sidebar.markdown("# Matching Result")
    st.write(df_page2)
    
    st.write("User inputs summary")
    st.write(input_store.input_dict)
    
    # Matching Activities Function
    def main_page2(sex):
        
        # Drop id and What's your age? columns for matching purpose
        if 'id' in df_matching.df_matching_no.columns:
            df_matching.df_matching_no = df_matching.df_matching_no.drop(['id'], axis=1)
        if 'What is your age?' in df_matching.df_matching_no.columns:
            df_matching.df_matching_no = df_matching.df_matching_no.drop(['What is your age?'], axis=1)
        if 'id' in df_matching.df_matching_yes.columns:
            df_matching.df_matching_yes = df_matching.df_matching_yes.drop(['id'], axis=1)
        if 'What is your age?' in df_matching.df_matching_yes.columns:
            df_matching.df_matching_yes = df_matching.df_matching_yes.drop(['What is your age?'], axis=1)
        
        # Sex option filter for the Yes users
        def dataframe_sex_filter(sex, df):
            if sex == "Male vs Male":
                df = sqldf("Select * from df where gender = 'Male'")
            elif sex == "Female vs Female":
                df = sqldf("Select * from df where gender = 'Female'")
            else:
                if 'Male' in input_store.input_list:
                    df = sqldf("Select * from df where gender = 'Female'")
                else:
                    df = sqldf("Select * from df where gender = 'Male'")
                
            return df
            
        # Matching for No users
        if input_store.input_dict["Usage"] == "No":
            # Convert the input list to a pandas series with the same number of columns
            input_series = pd.Series(input_store.input_list, index=df_matching.df_matching_no.columns)
            df = df_matching.df_matching_no
            
            # Drop the last row of the data so that can find a match that is different from themselves
            df.drop(df.tail(1).index,inplace=True)
            
            # Blind date option based on beauty
            
            # Result of Dataframe after sex selection filter
            st.write(dataframe_sex_filter(sex, df))

        # Matching for Yes Users
        elif input_store.input_dict["Usage"] == "Yes":
            # Convert the input list to a pandas series with the same number of columns
            input_series = pd.Series(input_store.input_list, index=df_matching.df_matching_yes.columns)
            df = df_matching.df_matching_yes
            
            # Drop the last row of the data so that can find a match that is different from themselves
            df.drop(df.tail(1).index,inplace=True)
            
            # Result of Dataframe after sex selection filter
            st.write(dataframe_sex_filter(sex, df))
            
        # Assign the sex selection filter to another variable
        df = dataframe_sex_filter(sex, df)
        
        # find the row with minimum difference
        best_match = df.loc[df.apply(lambda x: sum([1 if i not in x.values else 0 for i in input_series]), axis=1).idxmin()]

        st.write("Matching Result:")
        st.write(best_match)

    # Sex tension input for matching
    if "Female" in input_store.input_list:
        sex = st.radio('Choose your sex tension', ["Female vs Female", "Male vs Female"])
    else:
        sex = st.radio('Choose your sex preferences', ['Male vs Male', "Male vs Female"])
        
    # Conditions to deploy Matching Activities
    if input_store.input_dict['Usage'] == 'Yes':
        main_page2(sex)
    else:
        # If the user didn't use Tinder before but they intend to
        if input_store.input_list[5] == "Yes":
            beauty_option = st.radio('Do you want to join the beauty matching feature?', ['Yes', 'No'])
            if beauty_option == 'Yes':
                # Face Beauty Evaluation Result
                beauty_result = howcuteami.main()
                st.write(beauty_result)
                
                # If user didn't upload the picture, warn them
                if beauty_result == None:
                    st.warning('This is a warning for you to upload the picture in the correct format', icon="⚠️")
                # Else continue
                else:
                    # Beauty List:
                    df_matching.beauty_list.append([input_store.input_dict["Name"], input_store.input_dict["Gender"], beauty_result["Beauty"]])

                    # Create new beauty score dataframe
                    df_beauty = pd.DataFrame(df_matching.beauty_list, columns=["Name", "Gender", "Beauty Score"])
                    st.write(df_beauty)
                    
                    # beauty score dataframe filter based on sex preference
                    if sex == "Male vs Male":
                        df_beauty = sqldf("Select * from df_beauty where Gender = 'Male'")
                    elif sex == "Female vs Female":
                        df_beauty = sqldf("Select * from df_beauty where Gender = 'Female'")
                    else:
                        if 'Male' in input_store.input_list:
                            df_beauty = sqldf("Select * from df_beauty where gender = 'Female'")
                        else:
                            df_beauty = sqldf("Select * from df_beauty where gender = 'Male'")
                            
                    # Remove the newest user of the dataframe to do the matching activities
                    input_name = input_store.input_dict["Name"]
                    df_beauty = sqldf(f"SELECT * FROM df_beauty where Name is not '{input_name}' ")
                    
                    # Find the name whose beauty score is closely aligned to the other
                    min_diff = float('inf')
                    min_name = None
                    for name, score in df_beauty[['Name', 'Beauty Score']].values:
                        diff = abs(score - beauty_result["Beauty"])
                        if diff < min_diff:
                            min_diff = diff
                            min_name = name

                    st.write(min_name)
                
            else:
                main_page2(sex)
        
        # If the user didn't use Tinder before and they don't intend to
        else:
            st.write("I'm so sorry for this sad decision. I hope you would change your minde and come back to use my service in the near future. Best of lucks to you")
            
#Streamlit Multipage Creation
page_names_to_funcs = {
    "Introduction": introduction,
    "User Data Collection": main_page,
    "Matching System": page2,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

