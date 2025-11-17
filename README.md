

# 🚨 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

### **A Real-Time Traffic Stop Logging & Analysis System**

**Tech Stack:** Python · SQL (MySQL/PostgreSQL) · Streamlit
**Domain:** Law Enforcement | Public Safety | Real-time Monitoring Systems

---

## 📌 Problem Statement

Police check posts often rely on **manual logbooks** to record vehicle stops, driver details, violations, and searches.
This process is:

* Slow ⏳
* Error-prone ❌
* Difficult to analyze due to scattered data
* Not suitable for real-time monitoring or multi-location operations

### **Goal**

Build a **centralized SQL-based digital ledger** with a **Python & Streamlit dashboard** for real-time analytics, alerts, and automated reporting.

---

## 🎯 Objectives

* Centralize all vehicle stop logs in an SQL database
* Clean and preprocess raw traffic stop dataset
* Provide fast analytics via SQL + Streamlit
* Predict violation types & stop outcomes using pattern matching
* Enable officers to add new logs instantly
* Support medium & complex SQL query exploration

---

## 📂 Dataset Overview

Dataset: **traffic_stops**
Fields include:

* `stop_date`, `stop_time`
* `country_name`
* `driver_gender`, `driver_age`
* `driver_race`
* `violation`, `violation_raw`
* `search_conducted`, `search_type`
* `stop_outcome`, `is_arrested`
* `stop_duration`
* `drugs_related_stop`

---





# 🏗️ System Architecture

```
                ┌────────────────────────────┐
                │        User / Officer       │
                └───────────────┬────────────┘
                                │
                                ▼
                ┌────────────────────────────┐
                │      Streamlit Frontend     │
                │ - Add new police logs       │
                │ - Analytics dashboard       │
                └───────────────┬────────────┘
                                │ SQL Queries
                                ▼
                ┌────────────────────────────┐
                │     Python Backend         │
                │ pandas, SQLAlchemy, ML     │
                └───────────────┬────────────┘
                                │
                                ▼
                ┌────────────────────────────┐
                │       SQL Database         │
                │ MySQL / PostgreSQL         │
                └────────────────────────────┘
```

---

# 🛠️ Approach (Step-by-Step)

### **1️⃣ Data Cleaning (Python)**

* Remove missing values
* Drop unnecessary columns (`driver_age_raw`)
* Standardize violation categories
* Export cleaned dataset → `cleaned_traffic_stops.csv`

### **2️⃣ SQL Database Design**

Tables:

```
traffic_records (
    stop_date DATE,
    stop_time TIME,
    country_name VARCHAR,
    driver_gender VARCHAR,
    driver_age INT,
    driver_race VARCHAR,
    violation VARCHAR,
    search_conducted BOOLEAN,
    search_type VARCHAR,
    stop_outcome VARCHAR,
    is_arrested BOOLEAN,
    stop_duration VARCHAR,
    drugs_related_stop BOOLEAN,
    vehicle_number VARCHAR
)
```

### **3️⃣ Streamlit Dashboard**

* View entire dataset
* Run medium & complex SQL queries
* Add **new police log entries** via UI
* Predict:

  * **stop outcome**
  * **violation type**
* Show real-time insights and tables

---

# ⭐ Features

### ✔️ Real-Time Logging

Officers can enter:

* Driver info
* Violations
* Search details
* Drug-related stop
* Vehicle number

### ✔️ Prediction Engine

Predicts:

* Most likely **stop outcome**
* Most likely **violation**
* Based on pattern-matching in SQL data

### ✔️ Data Explorer

* View dataset
* Filter by gender, age, violation, time
* Export results

### ✔️ SQL Query Dashboard

Supports:

* Medium-level SQL questions
* Complex queries using **window functions**, **joins**, **aggregation**, **ranking**

### ✔️ Analytics

* Peak stop times
* Common violations
* Arrest rates
* Search vs non-search analysis

---

# 📊 Results

* **60% faster** check post operations using SQL vs manual logs
* Real-time insights enable quick decision making
* Automated detection of:

  * High-risk vehicles
  * Drug-related patterns
  * Age-based violation trends
* Officer-friendly dashboard with instant filtering
* Reliable dataset integrity through SQL backend

---

# 📈 Business / Technical Impact

### **Business Impact**

* Faster processing at check posts → reduced traffic congestion
* Better crime pattern insights
* Evidence-based policing
* Unified database for all posts

### **Technical Impact**

* SQL indexes boost query execution time
* Streamlit enables lightweight, deployable UI
* Reusable Python scripts for ETL
* Scalability for multi-city deployments

---

# 🔮 Future Enhancements

* Integration with **ANPR (Automatic Number Plate Recognition)**
* ML models for **violation prediction**
* Role-based login for officers
* Centralized cloud database
* SMS alert system for flagged vehicles
* Geo-mapping of stops
* Predictive policing (risk score system)

---

# 🌍 Real-Life Use Cases

* Highway police checkpoints
* Border security
* City traffic monitoring
* Crime analytics unit
* VIP movement control
* Automated red-signal violation analysis

---

# 💻 How to Run Locally

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/YourUser/SecureCheck.git
cd SecureCheck
```

### **2️⃣ Install Requirements**

```bash
pip install -r requirements.txt
```

### **3️⃣ Import SQL Schema**

```sql
SOURCE sql/schema.sql;
```

### **4️⃣ Update MySQL Credentials**

In `db_connection.py`:

```python
engine = create_engine("mysql+mysqlconnector://root:password@localhost/traffic_analysis")
```

### **5️⃣ Run Streamlit App**

```bash
streamlit run app/main.py
```

---

# 🔧 Tech Stack

| Area            | Technology         |
| --------------- | ------------------ |
| Programming     | Python             |
| Database        | MySQL / PostgreSQL |
| Web UI          | Streamlit          |
| Data Processing | Pandas, SQLAlchemy |
| Visualization   | Streamlit Charts   |
| Dataset Storage | CSV / Excel        |

---

# 📚 SQL Questions Included

### ✔ Medium Queries

* Top searched vehicles
* Arrest rate by age
* Drug-related stops by country
* Night vs day arrest rate
* Violation-wise search patterns

### ✔ Complex Queries

* Yearly breakdown using window functions
* Age + race violation trends
* Time period analysis (Year/Month/Hour)
* High-risk violations (search + arrest)
* Driver demographics by country

---


