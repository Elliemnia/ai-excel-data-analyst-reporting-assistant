import streamlit as st
import pandas as pd
import plotly.express as px


def generate_insights(df):
    insights = []

    insights.append(
        f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
    )

    insights.append(
        f"Missing values detected: {df.isnull().sum().sum()}."
    )

    duplicate_count = df.duplicated().sum()
    insights.append(
        f"Duplicate rows found: {duplicate_count}."
    )

    categorical_columns = df.select_dtypes(include="object").columns

    if len(categorical_columns) > 0:
        top_column = categorical_columns[0]
        most_common = df[top_column].mode()[0]

        insights.append(
            f"Most common {top_column} is '{most_common}'."
        )

    return insights


def create_profile_report(df, insights):
    report = f"""
AI EXCEL DATA ANALYST - DATASET PROFILE REPORT

Dataset Summary
---------------
Total Rows: {len(df)}
Total Columns: {len(df.columns)}
Missing Values: {df.isnull().sum().sum()}
Duplicate Rows: {df.duplicated().sum()}

Columns
-------
{', '.join(df.columns)}

Quick Insights
--------------
"""

    for item in insights:
        report += f"- {item}\n"

    return report


def answer_data_question(df, question):
    question_lower = question.lower()

    if "missing" in question_lower:
        return f"The dataset has {df.isnull().sum().sum()} missing values."

    if "duplicate" in question_lower:
        return f"The dataset has {df.duplicated().sum()} duplicate rows."

    if "rows" in question_lower:
        return f"The dataset contains {len(df)} rows."

    if "columns" in question_lower:
        return f"The dataset contains {len(df.columns)} columns."

    if "highest" in question_lower or "most" in question_lower or "top" in question_lower:
        for col in df.columns:
            if col.lower() in question_lower:
                if pd.api.types.is_numeric_dtype(df[col]):
                    top_value = df[col].max()
                    return f"The highest value in {col} is {top_value}."
                else:
                    top_value = df[col].value_counts().idxmax()
                    top_count = df[col].value_counts().max()
                    return f"The most common value in {col} is '{top_value}' with {top_count} records."

    return (
        "I can answer questions about rows, columns, missing values, duplicates, "
        "and the most common value in a selected column."
    )


st.set_page_config(
    page_title="AI Excel Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Excel Data Analyst")

st.markdown(
    """
Upload a CSV or Excel file and automatically generate insights, charts, and dataset quality checks.
"""
)

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Summary Cards")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", len(df))

    with col2:
        st.metric("Columns", len(df.columns))

    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    with col4:
        st.metric("Duplicate Rows", df.duplicated().sum())


    st.subheader("Dataset Health Check")

    health_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(health_df)

    st.subheader("📊 Quick Insights")

    insights = generate_insights(df)

    for item in insights:
        st.write("•", item)

    profile_report = create_profile_report(df, insights)

    st.download_button(
        label="Download Dataset Profile Report",
        data=profile_report,
        file_name="dataset_profile_report.txt",
        mime="text/plain"
    )

    st.subheader("📈 Interactive Chart")

    chart_column = st.selectbox(
        "Select a column to visualize",
        df.columns
    )

    chart_data = (
        df[chart_column]
        .value_counts()
        .reset_index()
    )

    chart_data.columns = [chart_column, "Count"]

    fig = px.bar(
        chart_data,
        x=chart_column,
        y="Count",
        title=f"{chart_column} Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("Ask a Question About the Dataset")

user_question = st.text_input(
    "Ask a question, for example: Which month appears most often?"
)

if st.button("Ask Data Analyst"):
    answer = answer_data_question(df, user_question)
    st.markdown("### Answer")
    st.write(answer)

    st.download_button(
        label="Download Answer",
        data=answer,
        file_name="data_answer.txt",
        mime="text/plain"
    )