# Customer Churn Analytics and Retention Prioritization System

Dashboard Link: [https://public.tableau.com/app/profile/revanth.ak/viz/ChurnAnalysis_17695521663480/Dashboard1]

## Overview

Customer churn has a direct impact on revenue and long-term growth.  
This project builds an **end-to-end churn analytics and prediction system** that combines exploratory analysis, machine learning, and business-focused scoring to support retention decisions.

The goal is not only to predict churn, but to **convert predictions into actionable insights** using dashboards and automated pipelines.

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

## Tech Stack

- **Python** – Data cleaning, feature engineering, and ML  
- **PostgreSQL** – Customer data and prediction storage  
- **Tableau** – Analytics and ML results dashboards  
- **Scikit-learn** – Logistic Regression and Random Forest 

---

## Dataset
Link: [https://www.kaggle.com/datasets/blastchar/telco-customer-churn]
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

## Machine Learning Approach

### Models
- **Logistic Regression (primary model)**  
  Used for interpretability and stable churn probabilities.
- **Random Forest (validation model)**  
  Used to validate non-linear patterns and feature importance.

### Feature Engineering
- Tenure-based features  
- Spending behavior and value proxies  
- Service engagement metrics  
- Contract and billing attributes  
- Pricing and tenure interaction features  

### Evaluation
Models were evaluated using ROC-AUC, precision/recall, and confusion matrices, with emphasis on **ranking churn risk** rather than raw accuracy.

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

## Data Storage and Integration

- Clean customer data and predictions are stored in PostgreSQL  
- Predictions are written using upsert logic keyed by `customer_id`  
- Tableau connects directly to PostgreSQL for live dashboards  

This design keeps analytics, ML outputs, and visualization cleanly separated.

---

