# The DAG object; we'll need this to instantiate a DAG

from airflow import DAG
from datetime import datetime, timedelta
from textwrap import dedent

# Operators; we need this to operate!

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
    PythonVirtualenvOperator,
    BranchPythonOperator,
)


with DAG(
'movie',
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
'depends_on_past': True,
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5)
},
description='movie 2020 DAG',
schedule_interval=timedelta(days=1),
start_date=datetime(2020, 1, 1),
end_date=datetime(2020, 12, 31),
catchup=True,
tags=['movie'],
) as dag:

    def fun_ext(dt):
        print('*'*30)
        print(dt)
        print('*'*30)
        from extrct.mov import list2df
        df=list2df(load_dt=dt)
        print(df)


    def fun_trans(dt):
        print('*'*30)
        print(dt)
        print('*'*30)
        from transform.transform import transform
        df=transform(load_dt=dt)
        #return df
        #print(df['month'].head(5))
        print(df.head(10))

    def fun_load(dt):
        print('*'*30)
        print(dt)
        print('*'*30)

        from load.load import load
        load(load_dt=dt)
        

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule="all_done")

    extract = PythonVirtualenvOperator(
            task_id='extract',
            python_callable=fun_ext,
            requirements=["git+https://github.com/play-gogo/Extract.git@d2/0.1.0"],
            system_site_packages=False,
            op_args=["{{ds_nodash}}"]
    )


    transform = PythonVirtualenvOperator(
            task_id='transform',
            python_callable=fun_trans,
            requirements=['git+https://github.com/play-gogo/transform.git@d2.0.0/test'],
            system_site_packages=False,
            op_args=["{{ds_nodash}}"]
    )

    load = PythonVirtualenvOperator(
            task_id='load',
            python_callable=fun_load,
            requirements=["git+https://github.com/play-gogo/load.git@d2/0.1.0"],
            system_site_packages=False,
            op_args=["{{ds_nodash}}"]
    )
    rm = BashOperator(
        task_id='rm',
        bash_command="""
            
        """
    )

    start >> extract >> transform >> load >> end
