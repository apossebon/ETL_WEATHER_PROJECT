-- init_db.sql

-- Create the schema
CREATE SCHEMA IF NOT EXISTS weather_schema;

-- Create the weather table within the schema
CREATE TABLE IF NOT EXISTS weather_schema.weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    country VARCHAR(50),
    longitude FLOAT,
    latitude FLOAT,
    temperature FLOAT,
    feels_like FLOAT,
    temperature_min FLOAT,
    temperature_max FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    visibility INTEGER,
    wind_speed FLOAT,
    wind_direction INTEGER,
    cloudiness INTEGER,
    weather_description VARCHAR(255),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    timezone INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);          


