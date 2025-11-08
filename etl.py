from google.cloud import bigquery
import pandas as pd

def etl_finder_column(
    source_table="dataset.table_name",
    target_table="dataset.table_name_cleaned"
):
    client = bigquery.Client()

    # 1. EXTRACT
    query = f"SELECT * FROM `{source_table}`"
    df = client.query(query).to_dataframe()

    # 2. TRANSFORM
    # Example: assume finder = "class1,class2,class3"
    # Split into list + normalize whitespace + drop nulls
    df["finder"] = (
        df["finder"]
        .fillna("")
        .apply(lambda x: [c.strip() for c in x.split(",") if c.strip() != ""])
    )

    # Optional: explode into multiple rows
    # df = df.explode("finder")

    # Optional: enforce category type
    # df["finder"] = df["finder"].astype("category")

    # 3. LOAD
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        target_table,
        job_config=job_config
    )
    job.result()

    print("ETL complete. Cleaned table loaded to:", target_table)
