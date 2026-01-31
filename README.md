# Customer Churn Analytics and Retention Prioritization System

Dashboard Link: [Tableau Public Dashboard](https://public.tableau.com/app/profile/revanth.ak/viz/ChurnAnalysis_17695521663480/Dashboard1)

## Overview

Customer churn has a direct impact on revenue and long-term growth.  
This project builds an **end-to-end churn analytics and prediction system** that combines exploratory analysis, machine learning, **risk scoring**, and **model monitoring** to support data-driven retention decisions.

The focus is not only on predicting churn, but on **ranking customers by risk and value**, tracking model stability over time, and converting predictions into **actionable insights** through dashboards and automated scoring pipelines.

---

> **Project Status**
>  
> This repository currently contains the full data analytics and machine learning pipeline for customer churn analysis, including data preprocessing, feature engineering, model training, scoring, and monitoring metrics.
>  
> Containerization and orchestration (Docker-based batch scoring) are planned as the next phase and are not included in this version.

---

## Key Questions Addressed

Every business wants to understand its customers, retain them longer, and reduce churn.  
This project focuses on answering the following questions using analytics and machine learning:

1. **How do customers behave over time?**  
   Analyze customer lifecycle patterns based on tenure, services, and spending.

2. **How can customers be segmented by engagement and value?**  
   Segment customers using tenure, service usage, and spending behavior.

3. **Who is likely to churn and why?**  
   Identify high-risk customers and the key factors driving churn.

4. **Which customers should be prioritized for retention?**  
   Rank customers by combining churn risk with revenue impact to guide retention efforts.

---

## Project Architecture (Current)

1. Raw customer data is cleaned and stored in PostgreSQL.
2. Monthly customer snapshots are simulated to represent time-based behavior.
3. Machine learning models are trained using historical churn data.
4. Each monthly snapshot is scored to generate:
   - Churn probability
   - Retention priority score
5. Model outputs and monitoring metrics are stored back in PostgreSQL.
6. Tableau connects directly to PostgreSQL for analytics and visualization.

This design separates analytics, modeling, and visualization while keeping PostgreSQL as the central data layer.

---

## Tech Stack

- **Python** – Data preprocessing, feature engineering, model training, and scoring
- **PostgreSQL** – Source of truth for customer data, predictions, and monitoring metrics
- **Tableau** – Analytics and ML results dashboards
- **Scikit-learn** – Logistic Regression and Random Forest models
- **Pandas / NumPy** – Data manipulation and simulation

---

## Dataset
Link: [Dataset Link](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)<br>
Telecom customer churn dataset containing:
- Tenure and contract information  
- Monthly and total charges  
- Service usage and payment methods  
- Churn indicator  

---

## Data Cleaning and Preprocessing

- Standardized categorical values  
- Corrected data types for numeric fields  
- Handled missing and invalid values  
- Created tenure buckets to capture customer lifecycle stages  
- Stored cleaned data in PostgreSQL as the analytics source of truth  

---

## Exploratory Analytics (Tableau)

An analytics dashboard was built to understand churn patterns before modeling, including:
- Churn rate by contract and tenure bucket  
- Revenue impact of churned customers  
- Churn behavior by payment method and service usage  
- Customer engagement depth vs churn  

This step ensures the ML model is grounded in business context.

<img width="1600" height="871" alt="image" src="https://github.com/user-attachments/assets/d164c072-0a11-4252-901f-33e21e8d52c0" />

<img width="1600" height="874" alt="image" src="https://github.com/user-attachments/assets/9323293c-9e43-47d7-bfc2-d2a4f502ccf4" />

---

## Machine Learning

- **Primary Model:** Logistic Regression  
  Chosen for interpretability and stable probability outputs.

- **Challenger Model:** Random Forest  
  Used to validate patterns and compare performance.

### Evaluation Metrics
- ROC-AUC
- Precision / Recall for churned customers
- Confusion matrix analysis

### Monitoring Metrics
- Average churn probability per month
- High-risk customer percentage
- Revenue at risk
- Month-over-month prediction stability (Spearman and Pearson correlation)

The focus is on ranking customers by churn risk rather than maximizing raw accuracy.

---

## Churn Probability and Retention Scoring

Each customer is assigned a churn probability using the logistic regression model.

A **retention priority score** is calculated as:

```bash
  retention_priority_score = churn_probability × monthly_charges
```
This score highlights customers who are both high-risk and high-value, enabling targeted retention efforts.

---

## ML Results Dashboard (Tableau)

The ML dashboard focuses on actionability:
- Churn risk distribution (Low / Medium / High)  
- Average churn risk by key segments  
- Revenue at risk by customer group  
- High-risk, high-value customers ranked by priority  

Navigation buttons connect analytics and ML dashboards.

---

## Model Monitoring

Monthly monitoring metrics are computed after each scoring run and stored in PostgreSQL to track model behavior over time.

Tracked metrics include average churn probability, high-risk customer percentage, revenue at risk, and a **rank stability score** based on month-over-month correlation of churn predictions. These metrics help assess prediction consistency and detect potential drift, ensuring the model remains reliable as customer behavior changes.

<img width="873" height="164" alt="image" src="https://github.com/user-attachments/assets/540f5c47-0c27-4697-8a78-d3d3c23f6865" />

---

## Data Storage and Integration

- Clean customer data and predictions are stored in PostgreSQL  
- Predictions are written using upsert logic keyed by `customer_id`  
- Tableau connects directly to PostgreSQL for live dashboards  

This design keeps analytics, ML outputs, and visualization cleanly separated.

---

## Current Limitations

- Model scoring is executed via Python scripts and is not yet containerized.
- No automated scheduler is used in the current version.
- Monitoring metrics are computed offline rather than through a managed orchestration system.

These limitations are intentional for this phase and will be addressed in future iterations.

---


