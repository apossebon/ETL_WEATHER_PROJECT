# ETL Weather Project

This project is an ETL (Extract, Transform, Load) pipeline that collects weather data from an API and saves it into a PostgreSQL database. The ETL process is orchestrated using Apache Airflow and the project is containerized using Docker Compose.

## Project Structure
etl-weather-project/ ├── dags/ │ └── weather_etl.py ├── docker-compose.yml ├── pyproject.toml ├── README.md └── tests/ └── test_sample.py

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+
- Poetry

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/etl-weather-project.git
    cd etl-weather-project
    ```

2. **Install dependencies using Poetry:**

    ```sh
    poetry install
    ```

3. **Set up environment variables:**

    Create a `.env` file in the project root and add your environment variables:

    ```env
    AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key
    WEATHER_API_KEY=your_weather_api_key
    ```

4. **Start Docker Compose:**

    ```sh
    docker-compose up -d
    ```

5. **Initialize Airflow:**

    ```sh
    docker-compose run --rm init
    ```

## Usage

1. **Access the Airflow web interface:**

    Open your browser and go to `http://localhost:8080`. Log in with the default credentials (`admin` / `admin`).

2. **Trigger the DAG:**

    In the Airflow web interface, trigger the `weather_etl` DAG to start the ETL process.

## Testing

Run tests using `pytest`:

```sh
poetry run pytest

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request.

Authors
Alysson Possebon - apossebon@wiley.com


This [README.md](http://_vscodecontentref_/4) file provides an overview of the project, setup instructions, usage details, and other relevant information. Adjust the content as needed to fit your specific project requirements.