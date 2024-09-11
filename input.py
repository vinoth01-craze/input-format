import streamlit as st
import pandas as pd
import base64
import numpy as np

grade_values = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'RA': 0, 'AB': 0}

st.set_page_config(
    page_title="input format",
    page_icon=":bar_chart:",
    layout="wide",  # or "centered"
    initial_sidebar_state="collapsed"  # or "expanded"
)

# Function to create an empty template CSV file
def create_empty_template(num_subjects, num_students, semester, i=0):
    # Create DataFrame with grade columns
    grade_columns = [f'Grade{i}_{semester}' for i in range(num_subjects)]
    template_data_grade = {
        'Reg. No.': [],
        'Student Name': [],
    }
    for col in grade_columns:
        template_data_grade[col] = []
    df_grade = pd.DataFrame(template_data_grade)

    # Create DataFrame with credit columns
    credit_columns = [f'Credit{i}_{semester}' for i in range(1, num_subjects + 1)]
    template_data_credit = {col: [] for col in credit_columns}
    df_credit = pd.DataFrame(template_data_credit)

    # Concatenate grade and credit DataFrames
    df_template = pd.concat([df_grade, df_credit], axis=1)

    # Fill credit values for all students
    for col in credit_columns:
        i+=1
        credit_value = st.number_input(f'Enter credit value for subject{i}:', min_value=0, value=0, step=1, key=f'{col}_input')
        df_template[col] = [credit_value] * num_students

    # Fill student names range
    for i in range(num_students):
        df_template.loc[i, 'Reg. No.'] = np.nan
        df_template.loc[i, 'Student Name'] = np.nan

    return df_template

def calculate_gpa(row):
    total_credit_points = 0
    total_credits = 0
    arrear_count = 0
    absent_count = 0
    gpa = np.nan  # Default GPA to NaN

    for col in row.index:
        if 'Grade' in col:
            grade_col = col
            credit_col = col.replace('Grade', 'Credit')
            # Check if the credit column exists
            if credit_col in row.index:
                grade = row[grade_col]
                credit = row[credit_col]
                # Handle 'RA' or 'AB' grades
                if grade == 'RA':
                    arrear_count += 1
                elif grade == 'AB':
                    absent_count += 1
                else:
                    # Convert grade to its corresponding integer value
                    grade_value = grade_values.get(grade, 0)
                    # Ensure credit is converted to int type
                    credit_value = int(credit)
                    total_credit_points += grade_value * credit_value
                    total_credits += credit_value
    if arrear_count == 0 and absent_count == 0:
        gpa = total_credit_points / total_credits if total_credits != 0 else 0

    return gpa, arrear_count, absent_count

def main():
    uploaded_files = []  # Initialize uploaded_files list

    # Custom CSS to set background image
    st.markdown(
        """
        <style>
        .stTextInput>div>div>input[type="number"] {
            width: 1000px !important; /* Adjust width of number input box */
            background-color: white !important; /* Set background color to white */
        }
        h1 {
            width: 400px;
            padding: 0%;
            top: 5%;
            left: 40%;
            font-size: 60px;
            color: lightwhite;
            font-family: Garamond, serif;
            white-space: nowrap; /* Ensures text stays on a single line */
            -webkit-animation: glow 1s ease-in-out infinite alternate;
            -moz-animation: glow 1s ease-in-out infinite alternate;
            animation: glow 1s ease-in-out infinite alternate;
            margin-bottom: 100px;
            background-clip: padding-box;
            box-shadow: 0 0 50px white;
        }
        h2{
            color:lightblue;
            font-family: Copperplate, Papyrus, fantasy;
        }
        h3{
            color:yellow;
          font-family: Copperplate, Papyrus, fantasy;
        }
        P {
            color: white;
            font-family: Copperplate, Papyrus, fantasy;
        }
        .stButton>button {
            background-color: black; /* Background color of the button */
        }
        .stButton>button:hover {
            cursor: pointer;
        }
        .stApp {
            background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQK88grx-feQrFNH0DYtvM_ZH5I_2B4UcvJOQ&s");
            background-size: cover;
            object-fit:center;
            filter:contrast(5.0),brightness(10.0);
        }
        @-webkit-keyframes glow {
            from {
                text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #e60073, 0 0 40px #e60073, 0 0 50px #e60073, 0 0 60px #e60073, 0 0 70px #e60073;
            }
            to {
                text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Get The Input For CGPA :books:")

    # Input number of semesters
    num_semesters = st.number_input("Enter the number of semesters:", min_value=0, value=0, step=1)

    # Allow users to download an empty template CSV file for each semester
    for semester in range(num_semesters):
        st.markdown(f"## Sem {semester+1}")
        num_subjects = st.number_input(f"Enter the number of subjects for Semester {semester+1}:", min_value=0, value=0,
                                       step=1)
        if num_subjects > 0:
            num_students = st.number_input(f"Enter the number of students for Semester {semester+1}:", min_value=0,
                                           value=0,
                                           step=1)
            template_df = create_empty_template(num_subjects, num_students, semester)  # Pass the semester parameter
            st.markdown(f"### Download an empty template CSV file for Semester {semester+1}:")
            csv_template = template_df.to_csv(index=False)
            b64_template = base64.b64encode(csv_template.encode()).decode()  # Convert to base64
            href_template = f'<a href="data:file/csv;base64,{b64_template}" download="Semester_{semester+1}_Template.csv">Download Semester {semester+1} Template CSV File</a>'
            st.markdown(href_template, unsafe_allow_html=True)
            st.write("")

if __name__ == "__main__":
    main()