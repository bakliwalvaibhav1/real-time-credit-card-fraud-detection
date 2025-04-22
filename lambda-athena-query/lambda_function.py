import boto3
import time

ATHENA_DATABASE = 'fraud_data'
ATHENA_OUTPUT_BUCKET = 's3://fraud-pipeline-results/athena/'

QUERY = """
SELECT year, COUNT(*) AS txn_count
FROM fraud_data.historical
GROUP BY year
"""

def lambda_handler(event, context):
    athena = boto3.client('athena')

    response = athena.start_query_execution(
        QueryString=QUERY,
        QueryExecutionContext={'Database': ATHENA_DATABASE},
        ResultConfiguration={'OutputLocation': ATHENA_OUTPUT_BUCKET}
    )

    query_execution_id = response['QueryExecutionId']
    print(f"Started query: {query_execution_id}")

    # Optional: wait for it to finish and return status
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)

    if status == 'SUCCEEDED':
        result_path = f"{ATHENA_OUTPUT_BUCKET}{query_execution_id}.csv"
        return {"status": "success", "output": result_path}
    else:
        return {"status": "failed", "reason": status}
