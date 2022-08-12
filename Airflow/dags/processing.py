from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

zipf = "/Users/Home/Airflow/down"
unzipf = "/Users/Home/Airflow/unzip"
output = "/Users/Home/Airflow/output"
database = "worldbank"
with DAG(
    'elt',
    default_args=default_args,
    description='ELT WorldBank Data',
    schedule_interval= '* * * * *',
    start_date=datetime(2021, 11, 26),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = BashOperator(
        task_id='unzip',
        bash_command=f'/Users/Home/Airflow/tasks/unzip.py {zipf} {unzipf}',
    )

    t2 = BashOperator(
        task_id='cleaning',
        bash_command=f'/Users/Home/Airflow/tasks/cleaning.py {unzipf} {output}',
    )

    t3 = BashOperator(
        task_id='upload',
        bash_command=f'/Users/Home/Airflow/tasks/cleaning.py {output} {database}',
    )

    t1 >> t2 >> t3
