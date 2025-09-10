
# 🚓 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

## 📌 Project Overview

* A **digital ledger system** for police check posts using **Python, SQL, and Streamlit**.
* Automates the process of logging, tracking, and analyzing **traffic stop records**.
* Provides **real-time monitoring, predictive insights, and interactive dashboards**.
* Centralized database system that ensures **faster operations, transparency, and efficiency** for law enforcement.

---

## 🛠 What I Did in This Project

### 🔹 Data Processing (Python + Pandas)

* Loaded raw dataset (`traffic_stops.xlsx`) and checked for **missing values**.
* Cleaned dataset: removed empty rows, dropped unnecessary columns, handled null values.
* Saved cleaned dataset as **CSV for SQL database insertion**.

### 🔹 Database Design (SQL + MySQL)

* Designed SQL schema (`traffic_records`) for traffic stop logs.
* Inserted cleaned dataset into **MySQL database** using SQLAlchemy.
* Wrote **medium-level SQL queries** (e.g., top vehicles in drug stops, age groups with highest arrest rate).
* Wrote **complex SQL queries** using **window functions, joins, and subqueries** for deep analysis.

### 🔹 Dashboard Development (Streamlit)

* Built **interactive web dashboard** for traffic data visualization.
* Implemented:

  * 🚦 **Add New Police Log** (form to enter new records).
  * 📊 **SQL Query Insights** (medium + complex queries).
  * 🔮 **Prediction Module** (predict outcome & violation based on past records).
  * 📈 **Key Metrics Summary** (arrest rate, search rate, drug stop rate, busiest stop time, most common violation).
* Added **custom UI**: background image, traffic light animation for stop simulation.

---

## 🎯 Motive

* Replace **manual police logs** with a **centralized, digital solution**.
* Enable **real-time insights** to improve law enforcement decision-making.
* Provide **data-driven analytics** for monitoring traffic violations, arrests, and search patterns.

---

## 🌍 Real-Life Use Cases

* 🚔 **Check Posts:** Officers can log and review traffic stops instantly.
* 🔎 **Criminal Detection:** Automatic flagging of suspicious or repeat offender vehicles.
* 📊 **Traffic Analysis:** Identify patterns in violations by age, gender, time of day, or location.
* 🏛 **Policy Making:** Helps authorities in **crime prevention** and **road safety improvements**.
* 🌐 **Multi-location Integration:** Centralized logs for **different states/countries** to share intelligence.

---

## ✅ Conclusion

This project successfully integrates **Python (data preprocessing), SQL (data management & analytics), and Streamlit (dashboard visualization)** into a **complete digital ledger system** for police check posts.

👉 It enhances **efficiency, transparency, and decision-making** in real-world law enforcement scenarios.
