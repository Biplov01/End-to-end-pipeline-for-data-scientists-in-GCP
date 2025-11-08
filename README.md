# ML-Ops and Lifecycle Management on GCP  
End-to-End Automated Model Training Using BigQuery ML, Vertex AI, and Python ETL

This repository demonstrates a full ML-Ops workflow for a **deal-duplication detection model** that automatically retrains itself using fresh data loaded into BigQuery. The project uses a combination of BigQuery ML, Python ETL pipelines, Vertex AI Model Registry, and GCP’s orchestration tools to deliver a continuous training and deployment lifecycle.

For a more detailed write-up, see the accompanying Medium article:  
👉 https://medium.com/@biplov001/ml-ops-and-life-cycle-management-in-gcp-for-data-scientists-6e4256b3e63d

---

## Overview

The system follows a continuous training loop:

1. **Daily Data Ingestion**
   - New deal data lands in BigQuery (`dataset.raw_deals`).
   - A Python ETL job (via Cloud Composer / Cloud Run / Cloud Functions) cleans, processes, and writes features into `dataset.training_features`.

2. **Automatic Retraining Trigger**
   - Cloud Scheduler sends a Pub/Sub message each day.
   - A Cloud Function checks for new data and triggers training only if fresh data exists.

3. **Model Training Using BigQuery ML**
   - SQL-based training makes the pipeline simple, transparent, and fast.
   - Example:
     ```sql
     CREATE OR REPLACE MODEL `dataset.deal_duplicate_model`
     OPTIONS(
       model_type='LOGISTIC_REG',
       input_label_cols=['is_duplicate'],
       DATA_SPLIT_METHOD='AUTO_SPLIT'
     ) AS
     SELECT * FROM `dataset.training_features`;
     ```

4. **Model Evaluation**
   - Evaluation metrics are generated using:
     ```sql
     SELECT * FROM ML.EVALUATE(
       MODEL `dataset.deal_duplicate_model`,
       (SELECT * FROM `dataset.validation_set`)
     );
     ```
   - A Cloud Function compares metrics to previous versions and decides whether to promote or reject the new model.

5. **Model Registry & Deployment (Vertex AI)**
   - Trained BigQuery ML models are exported and registered in Vertex AI Model Registry.
   - The best-performing version is deployed to a Vertex AI Endpoint for inference.

6. **Real-Time or Batch Inference**
   - Incoming requests hit the deployed endpoint.
   - Predictions, metadata, and confidence scores are logged back into BigQuery.

7. **Continuous Feedback Loop**
   - Inference logs feed future training cycles.
   - The system improves automatically as new data accumulates.

---

## Architecture Diagram (Conceptual)

BigQuery (Raw Data)
↓
Python ETL → dataset.training_features
↓
Cloud Scheduler → Pub/Sub → Training Trigger
↓
BigQuery ML (Training / Evaluation)
↓
Vertex AI Model Registry → Endpoint Deployment
↓
Prediction Service (Cloud Run / Cloud Functions)
↓
Inference Logs → BigQuery
↓
Retraining Loop (Continuous)

yaml
Copy code

---

## Key GCP Components Used

- **BigQuery**
  - Storage, feature repository, model training (BQ ML)

- **Vertex AI**
  - Model registry, deployment, endpoints

- **Cloud Composer / Cloud Run / Cloud Functions**
  - ETL, training trigger logic, orchestration

- **Cloud Scheduler + Pub/Sub**
  - Automated daily retraining

---

## Repository Structure (example)

.
├── etl/
│ └── etl_pipeline.py
├── training/
│ └── train_bqml.sql
├── evaluation/
│ └── evaluate_bqml.sql
├── deployment/
│ └── register_and_deploy.py
└── README.md

yaml
Copy code

---

## Medium Article

Read the full explanation here:  
👉 **ML-Ops and Lifecycle Management in GCP for Data Scientists**  
https://medium.com/@biplov001/ml-ops-and-life-cycle-management-in-gcp-for-data-scientists-6e4256b3e63d

---

If you want, I can add:
- badges  
- a license section  
- GIF diagrams  
- code samples for each component  
- or a step-by-step setup guide for GCP.
