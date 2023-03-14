import logging

from google.cloud import bigquery

from app.api.config_loader import AuditConfig

client = bigquery.Client()
config = AuditConfig()


def get_audit_logs(app: str):

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("app_name", "STRING", app)
        ]
    )
    query_job = client.query(
        config.properties["GET_APP_AUDIT_LOGS"], job_config=job_config
    )
    rows = query_job.result()
    if rows.total_rows > 0:
        df = rows.to_dataframe()
        return df.to_json(orient="records", force_ascii=False)

    return {"detail": {"status": "success", "message": "no data found"}}


def get_all_audit_logs():

    query_job = client.query(config.properties["GET_ALL_AUDIT_LOGS"])
    rows = query_job.result()
    if rows.total_rows > 0:
        df = rows.to_dataframe()
        return df.to_json(orient="records", force_ascii=False)

    return {"detail": {"status": "success", "message": "no data found"}}


def insert_audit_log(json_rows):
    table = client.get_table(config.properties["AUDIT_LOGS_TABLE"])
    errors = client.insert_rows_json(table, json_rows)

    if errors:
        logging.exception(
            "Error during saving rows to the BigQuery...", errors
        )
        return {
            "detail": {
                "status": "error",
                "message": "Oops, something went wrong. \
                    Try again in a moment.",
            }
        }

    return {"detail": {"status": "error", "message": "log successfully saved"}}
