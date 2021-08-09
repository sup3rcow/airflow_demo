from airflow import DAG # ovo uvijek moras importati
from airflow.operators.python import PythonOperator, BranchPythonOperator, PythonVirtualenvOperator

from datetime import datetime # potrebno za konfiguraciju dag-a

from jobs.first_job.app import run

def callable_virtualenv(dag_run, default_conf):
    from jobs.first_job.app import run

    if not dag_run.conf: # ako se dag ne pozove sa config-om koristi defaultni
        dag_run.conf = default_conf

    print(dag_run.conf.get('title'))
    print(dag_run.conf.get('subtitle'))
    run()
    
    # dinamicki import joba (npr preko dag_run, defniramo ""jobs.first_job"", a po konvenciji da se package mora zvati app.py, a ulazna metoda run)
    # package = __import__("jobs.first_job", fromlist=["app"])
    # module = getattr(package, 'app')
    # module.run()

def eee(aa):
    print(aa)

with DAG(
    "first_job", # id konvencija da se zove isto kao i fajl
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily", # cron expresion, npr okinut ce se start_date +1 = 2021-01-02
    catchup=False # nemoj izvrsiti job za prosla vremena.. ako je start_date u proslosti
) as dag: # context manager

    conf = dag.get_last_dagrun(include_externally_triggered=True).conf # iz konfiguracije mozes uzeti parametre potrebne za dinamicko pozivanje
    image_id = conf.get('image_id')

    def zzz():
        print(conf)
        print(image_id)
        eee('muuu')

    if image_id:
        app_run = PythonOperator(
            task_id="app_run", # svaki task mora imati unique id
            python_callable=zzz
        )
    else:
        # https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#pythonvirtualenvoperator
        app_run = PythonVirtualenvOperator(
            task_id="app_run", # svaki task mora imati unique id
            python_callable=callable_virtualenv,
            # requirements=["pandas==1.3.1"], # prepises iz Pipfile-a
            requirements=["pandas", "geopandas"], # prepises iz Pipfile-a
            python_version = "3.6", # prepises iz Pipfile-a - trenutno airflow podrzava do 3.6
            system_site_packages=True, # zabranis uzimanje paketa iz globalnog okruzenja (mora true kako bi mogao do custom jobs modula)
            use_dill=False,
            #vop_kwargs={"title": "Perica", "subtitle": "Mali"}
            op_kwargs={"default_conf": {"title": "Perica", "subtitle": "Mali"}}
        )
