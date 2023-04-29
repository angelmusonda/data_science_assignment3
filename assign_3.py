import pickle
import streamlit as st

# Load the saved model from file
with open('classifier_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)


@st.cache_data()
  
# defining the function which will make the prediction using the data which the user inputs 

# Input ApplicantIncome','LoanAmount','Credit_History','Loan_Amount_Term','Property_Area','Married','Education'
def prediction(ApplicantIncome, LoanAmount, Credit_History, Loan_Amount_Term, Property_Area,Married,Education):   
 
    # Pre-processing user input 
    if Credit_History == "Uncleared Debts":
        Credit_History = 0
    else:
        Credit_History = 1  
        
    Loan_Amount_Term = float(Loan_Amount_Term)
    
    if Property_Area == "Urban":
       Property_Area = 3
    elif Property_Area == "Semi Urban":
       Property_Area = 2
    else:
       Property_Area = 1

 
    if Married == "Unmarried":
        Married = 0
    else:
        Married = 1
 
    if Education == "Graduate":
        Education = 1
    else:
        Education = 0 
 

 
    # Making predictions 
    prediction = loaded_model.predict( 
        [[ApplicantIncome, LoanAmount, Credit_History, Loan_Amount_Term, Property_Area,Married,Education]])
     
    if prediction == 0:
        pred = 'Not Eligible'
    else:
        pred = 'Eligible'
    return pred
    
# this is the main function in which we define our webpage  
# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt


# Define the Streamlit app
def main():  
    
    chartTitleFontSize = 18;
    chartAxisNameFontSize = 18;
    chartAxisValuesFontSize = 14;
    

    st.set_page_config(
        page_title="Loan Applications",
        page_icon=":smiley:",
        layout="wide",
    
       
    )


    

 
    st.markdown("""
            <style>
                    
                    
                    .block-container {
                        padding-top: 0.2rem;
                        padding-bottom: 1rem;
                        padding-left: 1rem;
                        padding-right: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)

            

    

    # Load the loan data
    loan_data = pd.read_csv("processed_loan_data.csv")
    loan_data["Loan_Status"] = ["Awarded" if val == "Y" else "Rejected" for val in loan_data["Loan_Status"]]
    loan_data["Married"] = ["Married" if val == "Yes" else "Not Married" for val in loan_data["Married"]]
    # Set up the sidebar with the input fields for prediction
   


    df = loan_data.copy()


    status_colors = alt.Scale(domain=['Awarded', 'Rejected'], range=['#59CE8F', '#FF1E00'])
    scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('ApplicantIncome:Q', axis=alt.Axis(title='Applicant Income')),
        y=alt.Y('LoanAmount:Q', axis=alt.Axis(title='Loan Amount')),
        color=alt.Color('Loan_Status',scale = status_colors),
        tooltip=['Loan_Status', 'ApplicantIncome', 'LoanAmount']
    ).properties(
        width=200,
        height=500,
        title=alt.TitleParams(text='Loan Amount vs. Applicant Income', align='center', anchor='middle',offset=70)
    )





    stacked_bar_chart_education = alt.Chart(df).mark_bar().encode(
        x=alt.X('Education:N', axis=alt.Axis(title='',labelAngle=0, labelAlign='center',labelFontSize=chartAxisValuesFontSize)),
        y=alt.Y('count()', axis=alt.Axis(title='Loan Count',labelFontSize=chartAxisValuesFontSize)),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        column=alt.Column('Gender:N', header=alt.Header(title='', labelAlign='center',labelFontSize=chartAxisValuesFontSize)),
        tooltip=['Gender', 'Education', 'Loan_Status', alt.Text('count()', format=',')]
    ).properties(
        width=190,
        height=300,
        title={
        "text": "Loan Status by Education and Gender",
        "align": "center",
        "anchor": "middle"
    }

    )
    
    stacked_bar_chart_married = alt.Chart(df).mark_bar().encode(
        x=alt.X('Married:N', axis=alt.Axis(title='',labelAngle=0, labelAlign='center',labelFontSize=chartAxisValuesFontSize)),
        y=alt.Y('count()', axis=alt.Axis(title='Loan Count',labelFontSize=chartAxisValuesFontSize)),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        column=alt.Column('Gender:N', header=alt.Header(title='', labelAlign='center',labelFontSize=chartAxisValuesFontSize)),
        tooltip=['Gender', 'Married', 'Loan_Status', alt.Text('count()', format=',')]
    ).properties(
        width=190,
        height=300,
        title={
        "text": "Loan Status by Education and Gender",
        "align": "center",
        "anchor": "middle"
    }

    )
    
     



    # create separate DataFrames for applicants with good and bad credit history
    df_good = df[(df['Credit_History'] == 1) & (df['ApplicantIncome'] < 16000)]

    df_bad = df[(df['Credit_History'] == 0) & (df['ApplicantIncome'] < 30000)]




    # create scatter plot for applicants with good credit history
    scatter_good = alt.Chart(df_good).mark_circle(size=50).encode(
        x=alt.X('ApplicantIncome:Q', axis=alt.Axis(title='Applicant Income')),
        y=alt.Y('LoanAmount:Q', axis=alt.Axis(title='Loan Amount')),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        tooltip=['Loan_Status', 'ApplicantIncome', 'LoanAmount']
    ).properties(
        width=580,
        height=400,
        title=alt.TitleParams(text='Loan Amount vs. Applicant Income (Good Credit History)', align='center', anchor='middle', offset=20)
    )
    

    # create scatter plot for applicants with bad credit history
    scatter_bad = alt.Chart(df_bad).mark_circle(size=60).encode(
        x=alt.X('ApplicantIncome:Q', axis=alt.Axis(title='Applicant Income')),
        y=alt.Y('LoanAmount:Q', axis=alt.Axis(title='Loan Amount')),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        tooltip=['Loan_Status', 'ApplicantIncome', 'LoanAmount']
    ).properties(
        width=580,
        height=400,
        title=alt.TitleParams(text='Loan Amount vs. Applicant Income (Bad Credit History)', align='center', anchor='middle', offset=20)
    ).configure_view(stroke='red')


    st.write(
        '<h1 style="text-align: center; padding-top: 20px;">ABC Loan Application Information</h1>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    listTabs = ['Insight 💡','Predict 🤖']
    #tab1, tab2 = st.tabs(["Insight", "Predict"])
    whitespace = 40
    ## Fills and centers each tab label with em-spaces
    tab1,tab2 = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])
    
    with tab1:
        m1,left_column, m,right_column = st.columns([20,100,10,100])
        left_column.altair_chart( stacked_bar_chart_education,use_container_width=False)
        
        left_column.altair_chart( scatter_good, use_container_width=False)
        right_column.altair_chart(stacked_bar_chart_married, use_container_width=False)
        right_column.altair_chart(scatter_bad, use_container_width=False)
    with tab2:
        
        col0,col1,col2,col3,col4 = st.columns([20,100,100,100,20]);
        with col1:
            ApplicantIncome = st.number_input("Applicant Monthly Income ($)",min_value=1000, max_value=1000000, step=100)
            LoanAmount = st.number_input("Total loan amount ($)",min_value=1000, max_value=1000000, step=100)
            Education = st.selectbox('Education',("Graduate","Not A Graduate"))
        with col2:
            Credit_History = st.selectbox('Credit History',("Uncleared Debts","No Uncleared Debts"))
            Loan_Amount_Term = st.selectbox('Loan Term Months',("480","360","300","240","180","120","84","60","36","12"))
        with col3:
            Property_Area = st.selectbox('Property Area',("Urban","Semi Urban","Rural"))
            Married = st.selectbox('Marital Status',("Unmarried","Married")) 
           

            # When 'Predict' is clicked, make the prediction and display the result
            if st.button("Predict"): 
                result = prediction(ApplicantIncome, LoanAmount, Credit_History, Loan_Amount_Term, Property_Area,Married,Education) 
                st.success('Applicant is {}'.format(result))
    
 
    # Display the first visualization using Plotly in the first viewport
           


# Run the Streamlit app
if __name__ == "__main__":
    main()
