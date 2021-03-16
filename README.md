## Table of Contents
- [General Info](#general-info)
- [Technologies](#technologies)

## General Info
In this mini-project, I used Apache Airflow to create a data pipeline to extract online stock market data and deliver analytical results. With Airflow, I exercised the DAG creation, implemented various operators and set up order of operation of each task. The following steps were executed:

- Created the Airflow DAG
- Created a BashOperator to initialize a temporary directory for data download
- Created a PythonOperator to download market data
- Created a BashOperator to move the downloaded data to a data location
- Created a PythonOperator to run a query on both data files in the specified location
- Set job dependencies
- Scheduled the job in Airflow

## Technologies
Mini-project is created with: 
* Python
* Apache Airflow
* YFinance
* Pandas
* Requests
