# Importing the Libraries
import pandas as pd

# Load dataset
df = pd.read_excel("traffic_stops.xlsx")

# Show columns and dataset info
print(df.columns)
print(df.info())

# Handle missing values
df_1 = df.isnull().sum() * 100 / len(df)
print("Missing Values (%):\n", df_1)
print("Shape before removing missing rows:", df.shape)

df.dropna(inplace=True)
print("Shape after removing missing rows:", df.shape)

# Drop unnecessary columns
df.drop(['driver_age_raw'], axis=1, inplace=True)
print(df[['violation', 'violation_raw']].count())
df.drop(['violation_raw'], axis=1, inplace=True)

# Final check
print("Final missing values:\n", df.isnull().sum())

# Save cleaned dataset for SQL insertion
df.to_csv("cleaned_traffic_stops.csv", index=False)
print(" Data cleaned and saved as cleaned_traffic_stops.csv")

# SQL – Database Connection

import pandas as pd
from sqlalchemy import create_engine

# Load cleaned dataset
df = pd.read_csv("cleaned_traffic_stops.csv")

# Connect to MySQL
engine = create_engine("mysql+mysqlconnector://root:new_password@127.0.0.1/traffic_analysis")

# Insert into MySQL
df.to_sql("traffic_records", con=engine, if_exists="replace", index=False)
print(" Data inserted successfully into MySQL (traffic_records)")

"""# Streamlit – Dashboard

"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import base64, time

# ----------------- Background Setup -----------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: contain;
            background-position: center;
            opacity: 0.5;
        }}
        </style>
        """, unsafe_allow_html=True
    )

set_background(r"C:\Users\rajul\Downloads\Police_Logo.png")

# ----------------- Database Connection -----------------
engine = create_engine("mysql+mysqlconnector://root:new_password@127.0.0.1/traffic_analysis")

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# ----------------- Streamlit Setup -----------------
st.set_page_config(page_title="🚦 Traffic Stops Data Analysis", layout="wide")
st.title("🚦 Traffic Police Post Digital Ledger")
st.subheader(" Traffic Data Dashboard Overview")

# Show sample dataset
queries_0 = "SELECT * FROM traffic_records LIMIT 101;"
query_result_0 = run_query(queries_0)
st.dataframe(query_result_0)

st.write("""
This query retrieves **all rows and columns** from the `traffic_records` table.
It provides a complete view of the dataset after cleaning and insertion into MySQL.
""")

# ---------------------- ADD NEW POLICE LOG ----------------------
st.header(" Add New Police Log & Predict Outcome and Violation")

stop_date = st.date_input("Stop Date")
stop_time = st.time_input("Stop Time")
country_name = st.text_input("Country Name")
driver_gender = st.selectbox("Driver Gender", ["male", "female"])
driver_age = st.number_input("Driver Age", min_value=16, max_value=100, step=1)
driver_race = st.text_input("Driver Race")
search_conducted = st.selectbox("Was a Search Conducted?", [0, 1])
search_type = st.text_input("Search Type")
drugs_related_stop = st.selectbox("Was it Drug Related?", [0, 1])
stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
vehicle_number = st.text_input("Vehicle Number")



def traffic_light(active_color):
    color_map = {
        "red": "red",
        "yellow": "yellow",
        "green": "green"
    }
    st.markdown(f"""
        <div style="width:120px; margin:auto; padding:20px; border-radius:15px; background:black">
            <div style="width:70px; height:70px; margin:20px auto; border-radius:50%;
                        background:{color_map.get(active_color, '#333')};
                        box-shadow: 0 0 20px {color_map.get(active_color, '#333')};">
            </div>
        </div>
    """, unsafe_allow_html=True)

if st.button("Predict Stop Outcome & Violation"):
    with st.spinner("🚦 Traffic Signal Simulation..."):
        traffic_light("red")
        time.sleep(2)
        traffic_light("yellow")
        time.sleep(2)
        traffic_light("green")
        time.sleep(2)



    # 🔍 Filter data for prediction
    filtered_data = query_result_0[
        (query_result_0['driver_gender'] == driver_gender) &
        (query_result_0['driver_age'] == driver_age) &
        (query_result_0['search_conducted'] == int(search_conducted)) &
        (query_result_0['stop_duration'] == stop_duration) &
        (query_result_0['drugs_related_stop'] == int(drugs_related_stop))
    ]

    # 🎯 Predict stop outcome & violation
    if not filtered_data.empty:
        predicted_outcome = filtered_data['stop_outcome'].mode()[0]
        predicted_violation = filtered_data['violation'].mode()[0]
    else:
        predicted_outcome = "⚠️ Warning"       # Default fallback
        predicted_violation = "🚗 Speeding"    # Default fallback

    #  Natural language summary parts
    search_text = "✅ A search was conducted" if int(search_conducted) else "❌ No search was conducted"
    drug_text = "🧪 was drug-related" if int(drugs_related_stop) else "❎ was not drug-related"

    #  Styled output with columns
    st.markdown("##  Prediction Summary")
    st.success(f"**Predicted Outcome:** {predicted_outcome}")
    st.info(f"**Predicted Violation:** {predicted_violation}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Driver Info")
    st.markdown(f"""
    🔴 Age: **{driver_age}**
    🟡 Gender: **{driver_gender}**
    🟢 Country: **{country_name}**
    🚗 Vehicle: **{vehicle_number}**
    """)

with col2:
    st.subheader("🕒 Stop Details")
    st.markdown(f"""
    🔴 Date: **{stop_date}**
    🟡 Time: **{stop_time.strftime('%I:%M %p')}**
    🟢 Duration: **{stop_duration}**
    """)

with col3:
    st.subheader("📋 Context")
    st.markdown(f"""
    🔴 Search: **{search_type}**
    🟡 Drugs Related Stop: **{drugs_related_stop}**
    🟢 Status: **Analyzed**
    """)



# ---------------------- SQL QUERY INSIGHTS ----------------------
st.header(" SQL Medium Queries Insights")

queries = {
    "Top 10 Vehicle Numbers in Drug-Related Stops": """
        SELECT vehicle_number, COUNT(*) AS total
        FROM traffic_records
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY total DESC LIMIT 10;
    """,
    "Which vehicles were most frequently searched": """
        SELECT vehicle_number
        FROM traffic_records
        WHERE search_conducted = TRUE
        GROUP BY vehicle_number
        LIMIT 10;

    """,
    "Driver age group had the highest arrest rate": """
        SELECT driver_age, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS arrest_rate
        FROM traffic_records
        GROUP BY driver_age
        ORDER BY arrest_rate DESC
        LIMIT 5;
    """,
    "Gender distribution of drivers stopped in each country": """
        SELECT violation, COUNT(*) AS total
        FROM traffic_records
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY total DESC LIMIT 10;
    """,
    "Which race and gender combination has the highest search rate": """
        SELECT driver_race,driver_gender,SUM(search_conducted) / COUNT(*) AS search_rate
        FROM traffic_records
        GROUP BY driver_race, driver_gender
        ORDER BY search_rate DESC
        LIMIT 5;

    """,
        "Time of day sees the most traffic stops": """
        SELECT
        CASE
        WHEN HOUR(stop_time) BETWEEN 5 AND 11 THEN 'Morning'
        WHEN HOUR(stop_time) BETWEEN 12 AND 16 THEN 'Afternoon'
        WHEN HOUR(stop_time) BETWEEN 17 AND 20 THEN 'Evening'
        ELSE 'Night' END AS time_of_day,
        COUNT(*) AS total_stops
        FROM traffic_records
        GROUP BY time_of_day
        ORDER BY total_stops DESC;
    """,
    "Average stop duration for different violations": """
        SELECT violation,
        AVG(
        CASE stop_duration
        WHEN '0-15 Min' THEN 15
        WHEN '16-30 Min' THEN 30
        WHEN '30+ Min'  THEN 45
        END ) AS avg_stop_duration_minutes
        FROM traffic_records
        GROUP BY violation
        ORDER BY avg_stop_duration_minutes DESC;

    """,
    "Are stops during the night more likely to lead to arrests": """
        SELECT
        CASE
        WHEN HOUR(stop_time) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN HOUR(stop_time) BETWEEN 12 AND 17 THEN 'Noon'
        WHEN HOUR(stop_time) BETWEEN 18 AND 23 THEN 'Evening'
        ELSE 'Night' END AS time_period,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
        ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate_percent
        FROM traffic_records
        GROUP BY time_period ORDER BY arrest_rate_percent DESC;
    """,
    "Violations are most associated with searches or arrests": """
        SELECT violation, COUNT(*) AS total
        FROM traffic_records
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY total DESC LIMIT 10;
    """,
    "Violations are most common among younger drivers (<25)": """
        select driver_age,violation,count(*) as most_violations
        from traffic_records
        where driver_age < 25
        group by driver_age,violation
        order by most_violations;;

    """,
        "Is there a violation that rarely results in search or arrest": """
        SELECT
        violation,
        SUM(CASE WHEN search_conducted = TRUE OR is_arrested = TRUE THEN 1 ELSE 0 END) AS search_or_arrest_count,
        COUNT(*) AS total_stops,
        (SUM(CASE WHEN search_conducted = TRUE OR is_arrested = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS rate
        FROM traffic_records
        GROUP BY violation
        ORDER BY rate ASC;
    """,
    "Which countries report the highest rate of drug-related stops": """
        SELECT
        country_name,
        SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) AS drug_stops,
        COUNT(*) AS total_stops,
        (SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS drug_stop_rate
        FROM traffic_records
        GROUP BY country_name
        ORDER BY drug_stop_rate DESC;
    """,
    " Arrest rate by country and violation": """
        SELECT
        country_name,
        violation,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
        COUNT(*) AS total_stops,
        (SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS arrest_rate
        FROM traffic_records
        GROUP BY country_name, violation
        ORDER BY arrest_rate DESC;


    """,
    " Country has the most stops with search conducted": """
        SELECT country_name,
        COUNT(*) AS total_stops_with_search
        FROM traffic_records
        WHERE search_conducted = TRUE
        GROUP BY country_name
        ORDER BY total_stops_with_search DESC;


    """

}

selected_query = st.selectbox("Choose a Query", list(queries.keys()))
query_result = run_query(queries[selected_query])

st.write("### Query Result:")
st.dataframe(query_result)

st.header(" SQL Complex Queries  Insights")

queries_1 = {
    "Yearly Breakdown of Stops and Arrests by Country": """
        SELECT country_name,year,total_stops,total_arrests,
        ROUND(total_arrests * 100.0 / total_stops, 2) AS arrest_rate_percent,
        RANK() OVER(PARTITION BY country_name ORDER BY year) AS yearly_rank,
        DENSE_RANK() OVER(PARTITION BY country_name ORDER BY (total_arrests * 1.0 / total_stops) DESC) AS arrest_rate_rank
        FROM (
        SELECT country_name,YEAR(stop_date) AS year,
        COUNT(DISTINCT CONCAT(driver_age, driver_gender, driver_race, vehicle_number, stop_date, stop_time)) AS total_stops,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
        FROM traffic_records
        GROUP BY country_name, YEAR(stop_date)
        ) AS sub
        ORDER BY country_name, year;
    """,
    "Driver Violation Trends Based on Age and Race": """
        SELECT
    tr.driver_age,
    tr.driver_race,
    v.violation,
    COUNT(*) AS violation_count
FROM traffic_records tr
JOIN (
    SELECT driver_age, driver_race, violation
    FROM traffic_records
    GROUP BY driver_age, driver_race, violation
) v
ON tr.driver_age = v.driver_age AND tr.driver_race = v.driver_race
GROUP BY tr.driver_age, tr.driver_race, v.violation
ORDER BY violation_count DESC;

    """,
    "Time Period Analysis of Stops": """
        SELECT
            d.year,
        d.month,
        d.hour_of_day,
        COUNT(*) AS total_stops
        FROM traffic_records tr
        JOIN (
        SELECT
        YEAR(stop_date) AS year,
        MONTH(stop_date) AS month,
        HOUR(stop_time) AS hour_of_day,
        stop_date,
        stop_time
        FROM traffic_records
        ) d
        ON YEAR(tr.stop_date) = d.year
        AND MONTH(tr.stop_date) = d.month
        AND HOUR(tr.stop_time) = d.hour_of_day
        GROUP BY d.year, d.month, d.hour_of_day
        ORDER BY d.year, d.month, d.hour_of_day;
    """,
    "Violations with High Search and Arrest Rates": """
        SELECT violation,total_stops,total_searches,total_arrests,
        ROUND(total_searches * 100.0 / total_stops, 2) AS search_rate_percent,
        ROUND(total_arrests * 100.0 / total_stops, 2) AS arrest_rate_percent,
        RANK() OVER (ORDER BY (total_searches + total_arrests) * 1.0 / total_stops DESC) AS risk_rank
        FROM (
        SELECT violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
        FROM traffic_records
        GROUP BY violation
        ) v;
    """,
    "Driver Demographics by Country (Age, Gender, and Race)": """
        SELECT
        country_name,
        driver_age,
        driver_gender,
        driver_race,
        COUNT(*) AS total_drivers
        FROM traffic_records
        GROUP BY country_name, driver_age, driver_gender, driver_race
        ORDER BY country_name, total_drivers DESC;
    """,
    "Top 5 Violations with Highest Arrest Rates": """
        SELECT violation,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
        COUNT(*) AS total_stops,
        (SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS arrest_rate
        FROM traffic_records
        GROUP BY violation
        ORDER BY arrest_rate DESC;
    """

}

selected_query_1 = st.selectbox("Choose a Query", list(queries_1.keys()))
query_result_1 = run_query(queries_1[selected_query_1])

st.write("### Query Result:")
st.dataframe(query_result_1)

# ---------------------- CONCLUSION ----------------------
st.header(" Conclusion - Key Metrics")

# --- Calculate metrics ---
total_stops = query_result_0.shape[0]

# Most common violation
violation_stats = run_query("""
    SELECT violation, COUNT(*) AS total
    FROM traffic_records
    GROUP BY violation
    ORDER BY total DESC;
""")
most_common_violation = violation_stats.iloc[0]["violation"]
peak_time = run_query("""
    SELECT
        CASE
            WHEN HOUR(stop_time) BETWEEN 5 AND 11 THEN 'Morning'
            WHEN HOUR(stop_time) BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN HOUR(stop_time) BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night' END AS time_of_day,
        COUNT(*) AS total_stops
    FROM traffic_records
    GROUP BY time_of_day
    ORDER BY total_stops DESC
    LIMIT 1;
""")
busiest_time = peak_time.iloc[0]["time_of_day"]


# Arrest rate
arrest_stats = run_query("""
    SELECT
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
        COUNT(*) AS total
    FROM traffic_records;
""")
arrest_rate = round((arrest_stats["arrests"][0] / arrest_stats["total"][0]) * 100, 2)

# Search conducted rate
search_stats = run_query("""
    SELECT
        SUM(search_conducted) AS searches,
        COUNT(*) AS total
    FROM traffic_records;
""")
search_rate = round((search_stats["searches"][0] / search_stats["total"][0]) * 100, 2)

# Drug-related stops rate
drug_stats = run_query("""
    SELECT
        SUM(drugs_related_stop) AS drug_stops,
        COUNT(*) AS total
    FROM traffic_records;
""")
drug_rate = round((drug_stats["drug_stops"][0] / drug_stats["total"][0]) * 100, 2)

# --- Display Metrics ---
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Stops Recorded", total_stops)
    st.metric("Arrest Rate", f"{arrest_rate}%")
    st.metric("Drug-Related Stops", f"{drug_rate}%")

with col2:
    st.metric("Most Common Violation", most_common_violation)
    st.metric("Search Conducted Rate", f"{search_rate}%")
    st.metric("Peak Stop Time", busiest_time)

# Below line is the command you run in your terminal to start your Streamlit dashboard.
# python -m streamlit run c:/Users/rajul/OneDrive/Documents/GUVI/Mini_project/Traffic_app.py
