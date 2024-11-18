from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone
import requests
import psycopg2

import requests
from datetime import datetime, timezone

def extract_weather_data():
    try:
        # Get the current date and time in UTC
        
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Curitiba&appid=f3946380ac1a5d7f63b058adb10d0387")
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        print('###################################################')
        print(response)
        print('###################################################')
        
        data = response.json()
        print(data)
        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return None

    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return None

    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Transform: Process the data to extract necessary fields
def transform_weather_data(**context):
    data = context['task_instance'].xcom_pull(task_ids='extract_weather_data')
    
    if data is None:
        return None    
        
    transformed_data = {
        "City": data.get("name"),
        "Country": data.get("sys", {}).get("country"),
        "Longitude": data.get("coord", {}).get("lon"),
        "Latitude": data.get("coord", {}).get("lat"),
        "Temperature": data.get("main", {}).get("temp"),
        "Feels_Like": data.get("main", {}).get("feels_like"),
        "Temperature_Min": data.get("main", {}).get("temp_min"),
        "Temperature_Max": data.get("main", {}).get("temp_max"),
        "Pressure": data.get("main", {}).get("pressure"),
        "Humidity": data.get("main", {}).get("humidity"),
        "Visibility": data.get("visibility"),
        "Wind_Speed": data.get("wind", {}).get("speed"),
        "Wind_Direction": data.get("wind", {}).get("deg"),
        "Cloudiness": data.get("clouds", {}).get("all"),
        "Weather_Description": data.get("weather", [{}])[0].get("description"),
        "Sunrise": datetime.fromtimestamp(data.get("sys", {}).get("sunrise"), timezone.utc).isoformat(),
        "Sunset": datetime.fromtimestamp(data.get("sys", {}).get("sunset"), timezone.utc).isoformat(),
        "Timezone": data.get("timezone"),
        "DateTime": datetime.fromtimestamp(data.get("dt"), timezone.utc).isoformat()
    }
    
    print('###################################################')
    print(transformed_data)
    print('###################################################')
    
    return transformed_data

def save_to_postgres(**context):
    transformed_data = context['task_instance'].xcom_pull(task_ids='transform_weather_data')
    
    if transformed_data is None:
        return
    
    print(transformed_data)
    
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres', password='Aap7978Po', host='postgres001dev.postgres.database.azure.com'
            #dbname='airflow', user='airflow', password='airflow', host='postgres'
        )
        ##postgres001dev.postgres.database.azure.com
        print('###################################################')
        print(len(transformed_data))
        print(transformed_data.keys())
        print('###################################################')
        
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO weather_schema.weather (
                city, country, longitude, latitude, temperature, feels_like, temperature_min, temperature_max, 
                pressure, humidity, visibility, wind_speed, wind_direction, cloudiness, weather_description, sunrise, sunset, timezone, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                transformed_data['City'], transformed_data['Country'], transformed_data['Longitude'], transformed_data['Latitude'], 
                transformed_data['Temperature'], transformed_data['Feels_Like'], transformed_data['Temperature_Min'], 
                transformed_data['Temperature_Max'], transformed_data['Pressure'], transformed_data['Humidity'], 
                transformed_data['Visibility'], transformed_data['Wind_Speed'], transformed_data['Wind_Direction'], 
                transformed_data['Cloudiness'], transformed_data['Weather_Description'], transformed_data['Sunrise'], 
                transformed_data['Sunset'], transformed_data['Timezone'], transformed_data['DateTime']
            )
        )
        
        conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 31),  # Use a fixed start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_etl',
    default_args=default_args,
    description='A simple ETL DAG for weather data',
    schedule_interval=timedelta(minutes=10),
    catchup=False,  # Disable backfilling
)

fetch_task = PythonOperator(
    task_id='extract_weather_data',
    python_callable=extract_weather_data,
    dag=dag,
)


transform_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_weather_data,
    dag=dag,
)


save_task = PythonOperator(
    task_id='save_to_postgres',
    python_callable=save_to_postgres,
    provide_context=True,
    dag=dag,
)

fetch_task >> transform_task >> save_task