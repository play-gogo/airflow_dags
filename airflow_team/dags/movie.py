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
'depends_on_past': False,
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5)
},
description='movie 2020 DAG',
schedule_interval=timedelta(days=1),
start_date=datetime(2020, 6, 28),
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
    
    def branch_fun(ds_nodash):
        import os
        home_dir = os.path.expanduser("~")
        month=int(ds_nodash[4:6])
        path = os.path.join(home_dir, f"code/playgogo/storage/month={month}/load_dt={ds_nodash}")
        print('*' * 30)
        print(path)
        print('*' * 30)   

        if os.path.exists(path):
            print('존재')
            return "rm.dir" #rmdir.task_id
        else:
            print('존재x')
            return "load"

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
            trigger_rule="all_done",
            requirements=["git+https://github.com/play-gogo/load.git@d2/0.1.0"],
            system_site_packages=False,
            op_args=["{{ds_nodash}}"]
    )

    branch_op = BranchPythonOperator(
            task_id="branch.op",
            python_callable=branch_fun
    )
    rm_dir = BashOperator(
            task_id='rm.dir',
            bash_command="""
                month=$(echo "{{ ds_nodash[4:6] }}" | awk '{print $1+0}');
                echo $month
                echo code/playgogo/storage/month=$month/load_dt={{ds_nodash}}
                rm -rf ~/code/playgogo/storage/month=$month/load_dt={{ds_nodash}}
            """

    )

    start >> extract >> transform 
    transform >> branch_op
    branch_op >> rm_dir
    branch_op >> load

    rm_dir >> load >> end
