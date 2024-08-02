# The DAG object; we'll need this to instantiate a DAG

from airflow import DAG

# Operators; we need this to operate!

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
'ice_breaking',
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
'depends_on_past': True,
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5)
},
description='ice breaking DAG',
schedule_interval=timedelta(days=1),
start_date=datetime(2024, 7, 10),
catchup=True,
tags=['ice'],
) as dag:
