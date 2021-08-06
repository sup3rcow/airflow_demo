from airflow import DAG # ovo uvijek moras importati
from airflow.operators.python import PythonOperator, BranchPythonOperator, PythonVirtualenvOperator

from datetime import datetime # potrebno za konfiguraciju dag-a

from jobs.first_job.app import run

def callable_virtualenv(dag_run, title, subtitle):
    from jobs.first_job.app import run
    # ne funkcionira sa PythonVirtualenvOperator
    # from airflow.operators.python import get_current_context
    # context = get_current_context()
    # print(context['dag_run'].conf['title'])

    # varijable iz op_kwargs
    print(title)
    print(subtitle)
    # varijable iz dag_run
    print(dag_run.conf.get('title'))
    print(dag_run.conf.get('subtitle'))
    run()

with DAG(
    "first_job", # id konvencija da se zove isto kao i fajl
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily", # cron expresion, npr okinut ce se start_date +1 = 2021-01-02
    catchup=False # nemoj izvrsiti job za prosla vremena.. ako je start_date u proslosti
) as dag: # context manager

# https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#pythonvirtualenvoperator
    app_run = PythonVirtualenvOperator(
        task_id="app_run", # svaki task mora imati unique id
        python_callable=callable_virtualenv,
        # requirements=["pandas==1.3.1"], # prepises iz Pipfile-a
        requirements=["pandas"], # prepises iz Pipfile-a
        python_version = "3.6", # prepises iz Pipfile-a - trenutno airflow podrzava do 3.6
        system_site_packages=True, # zabranis uzimanje paketa iz globalnog okruzenja (mora true kako bi mogao do custom jobs modula)
        use_dill=False,
        op_kwargs={"title": "Perica", "subtitle": "Mali"}
    )

    # app_run = PythonOperator(
    #     task_id="app_run", # svaki task mora imati unique id
    #     python_callable=run
    # )