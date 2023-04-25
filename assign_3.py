import pickle
import streamlit as st

# Load the saved model from file
with open('classifier_model2.pkl', 'rb') as f:
    loaded_model = pickle.load(f)


@st.cache_data()
  
# defining the function which will make the prediction using the data which the user inputs 

# Input ApplicantIncome','LoanAmount','Credit_History','Loan_Amount_Term','Property_Area','Married','Education'
def prediction(ApplicantIncome, LoanAmount, Credit_History, Loan_Amount_Term, Property_Area,Married,Education):   
 
    # Pre-processing user input 
    if Credit_History == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1  
        
    Loan_Amount_Term = float(Loan_Amount_Term)
    
    if Property_Area == "Urban":
       Property_Area = 1
    elif Property_Area == "Semi Urban":
       Property_Area = 2
    else:
       Property_Area = 3

 
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
  
    st.set_page_config(layout="wide")
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 0.4rem;
                        padding-bottom: 1rem;
                        padding-left: 1rem;
                        padding-right: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)

            

    st.sidebar.header("Enter Loan Details")
    # Load the loan data
    loan_data = pd.read_csv("processed_loan_data.csv")
    loan_data["Loan_Status"] = ["Awarded" if val == "Y" else "Rejected" for val in loan_data["Loan_Status"]]
    # Set up the sidebar with the input fields for prediction
   
    ApplicantIncome = st.sidebar.number_input("Applicant Monthly Income")
    LoanAmount = st.sidebar.number_input("Total loan amount")
    Credit_History = st.sidebar.selectbox('Credit_History',("Unclear Debts","No Unclear Debts"))
    Loan_Amount_Term = st.sidebar.selectbox('Loan Term Days',("360","180","480","300","240","120","90","90","60","30"))
    Property_Area = st.sidebar.selectbox('Property Area',("Urban","Semi Urban","Rural"))
    Married = st.sidebar.selectbox('Marital Status',("Unmarried","Married")) 
    Education = st.sidebar.selectbox('Education',("Graduate","Not A Graduate"))

    # When 'Predict' is clicked, make the prediction and display the result
    if st.sidebar.button("Predict"): 
        result = prediction(ApplicantIncome, LoanAmount, Credit_History, Loan_Amount_Term, Property_Area,Married,Education) 
        st.sidebar.success('Applicant is {}'.format(result))
    
 
    # Display the first visualization using Plotly in the first viewport
   

    df = loan_data.copy()


    status_colors = alt.Scale(domain=['Awarded', 'Rejected'], range=['green', 'red'])
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





    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Education:N', axis=alt.Axis(labelAngle=0, labelAlign='center')),
        y=alt.Y('count()', axis=alt.Axis(title='Loan Count')),
        color=alt.Color('Loan_Status', scale=alt.Scale(scheme='pastel2'),title="Loan Outcome"),
        column=alt.Column('Gender:N', header=alt.Header(title='Gender', labelAlign='center')),
        tooltip=['Gender', 'Education', 'Loan_Status', alt.Text('count()', format=',')]
    ).properties(
        width=175,
        height=450,
        title={
        "text": "Loan Status by Education and Gender",
        "align": "center",
        "anchor": "middle"
    }

    )



    # create separate DataFrames for applicants with good and bad credit history
    df_good = df[(df['Credit_History'] == 1) & (df['ApplicantIncome'] < 16000)]

    df_bad = df[(df['Credit_History'] == 0) & (df['ApplicantIncome'] < 30000)]


    # define the color scale for loan status
    status_colors = alt.Scale(domain=['Awarded', 'Rejected'], range=['green', 'red'])

    # create scatter plot for applicants with good credit history
    scatter_good = alt.Chart(df_good).mark_circle(size=60).encode(
        x=alt.X('ApplicantIncome:Q', axis=alt.Axis(title='Applicant Income')),
        y=alt.Y('LoanAmount:Q', axis=alt.Axis(title='Loan Amount')),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        tooltip=['Loan_Status', 'ApplicantIncome', 'LoanAmount']
    ).properties(
        width=450,
        height=300,
        title=alt.TitleParams(text='Loan Amount vs. Applicant Income (Good Credit History)', align='center', anchor='middle', offset=20)
    )

    # create scatter plot for applicants with bad credit history
    scatter_bad = alt.Chart(df_bad).mark_circle(size=60).encode(
        x=alt.X('ApplicantIncome:Q', axis=alt.Axis(title='Applicant Income')),
        y=alt.Y('LoanAmount:Q', axis=alt.Axis(title='Loan Amount')),
        color=alt.Color('Loan_Status', scale=status_colors,title="Loan Outcome"),
        tooltip=['Loan_Status', 'ApplicantIncome', 'LoanAmount']
    ).properties(
        width=450,
        height=300,
        title=alt.TitleParams(text='Loan Amount vs. Applicant Income (Bad Credit History)', align='center', anchor='middle', offset=20)
    )

    # concatenate the two scatter plots vertically
    scatter_combined = alt.vconcat(scatter_good, scatter_bad, spacing=20)

    # display the combined scatter plots
   
       
   

    #left_column.markdown('Pie Chart of Loan_Status')
    #left_column.altair_chart(loan_status_chart, use_container_width=True)
    
    #left_column.markdown('Pie Chart of Loan_Status')
    #left_column.altair_chart(heatmap_chart, use_container_width=True)
    
    #right_column.markdown('Bar Chart of Loan_Amount_Term by Property_Area')
    #right_column.altair_chart(loan_term_chart, use_container_width=True)

    #left_column.markdown('Scatter Plot of LoanAmount vs. ApplicantIncome')
    #left_column.altair_chart(scatter_chart, use_container_width=True)

    #right_column.markdown('Stacked Bar Chart of Loan_Status by Education and Gender')
    #right_column.altair_chart(stacked_bar_chart, use_container_width=True)
    
    # Layout (Content)
    


    st.write(
        '<h1 style="text-align: center; padding-top: 20px;">ABC Loan Application Information</h1>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_column, m,right_column = st.columns([100,10,100])
    left_column.altair_chart( scatter_good, use_container_width=True)
    left_column.altair_chart( scatter_bad, use_container_width=True)
    right_column.altair_chart(stacked_bar_chart, use_container_width=False)

    


# Run the Streamlit app
if __name__ == "__main__":
    main()
