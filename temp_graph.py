#!/usr/bin/env python3
import time
import datetime
from sense_hat import SenseHat
import requests
import matplotlib.pyplot as plt
import pandas as pd
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# Setup logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
if "OPEN_WEATHER_KEY" not in os.environ:
    logging.error("OPEN_WEATHER_KEY is not set")
    print("OPEN_WEATHER_KEY is not set")
    exit(1)
# Constants
API_KEY = os.getenv('OPEN_WEATHER_KEY')
PARIS_LAT = 48.8566
PARIS_LON = 2.3522
MEASUREMENT_INTERVAL = 5 * 60  # 5 minutes in seconds
NUM_MEASUREMENTS = 24 * 60 // 5  # 24 hours of measurements

def get_temperature_in_paris():
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={PARIS_LAT}&lon={PARIS_LON}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        return data['main']['temp']
    except Exception as e:
        logging.error(f"Error getting temperature in Paris: {e}")
        return None

def main():
    sense = SenseHat()
    while True:
        # Data storage
        timestamps = []
        ambient_temps = []
        paris_temps = []

        for _ in range(NUM_MEASUREMENTS):
            # Record timestamp
            timestamps.append(pd.Timestamp.now())

            try:
             # Record ambient temperature
                ambient_temp = sense.get_temperature()
                ambient_temps.append(ambient_temp)

                # Get temperature in Paris
                paris_temp = get_temperature_in_paris()
                if paris_temp is not None:
                    paris_temps.append(paris_temp)
                else:
                    paris_temps.append(float('nan'))
            except Exception as e:
                logging.error(f"Error getting temperature: {e}")

            # Wait for the next measurement
            time.sleep(MEASUREMENT_INTERVAL)

        # Create a DataFrame with the collected data
        try:
            data = pd.DataFrame({'Timestamp': timestamps, 'Ambient': ambient_temps, 'Paris': paris_temps})
            data['Difference'] = data['Ambient'] - data['Paris']

            # Plot the data
            plt.figure(figsize=(15, 6))
            plt.plot(data['Timestamp'], data['Ambient'], label='Ambient Temperature')
            plt.plot(data['Timestamp'], data['Paris'], label='Temperature in Paris')
            plt.plot(data['Timestamp'], data['Difference'], label='Difference')
            plt.xlabel('Time')
            plt.ylabel('Temperature (°C)')
            plt.title('Temperature Comparison: Ambient vs. Paris')
            plt.legend()
            timestamp_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'/home/pi/Documents/temperature_comparison_{timestamp_str}.png'
            plt.savefig(filename)
            #clear the data storage
            timestamps.clear()
            ambient_temps.clear()
            paris_temps.clear()
            plt.close()
        except Exception as e:
            logging.error(f"Error creating the file: {e}")

if __name__ == '__main__':
    main()
