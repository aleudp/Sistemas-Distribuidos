from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from confluent_kafka import Producer
import time
import json
import datetime
import signal
import sys

def create_kafka_producer():
    return Producer({
        'bootstrap.servers': 'kafka1:9092'  # Ensure this matches your Kafka setup
    })

def handle_exit_signal(signal, frame):
    print("\nGracefully shutting down...")
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, handle_exit_signal)

def scrape_waze(producer):
    options = Options()
    options.add_argument("--headless")
    service = Service("/usr/local/bin/geckodriver")
    
    # Initialize the WebDriver outside the loop
    driver = webdriver.Firefox(service=service, options=options)

    try:
        while True:  # Infinite loop for scraping
            print("Starting scraping cycle...")
            driver.get("https://www.waze.com/live-map")

            # Wait for the incidents to load dynamically
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'leaflet-marker-icon'))
            )

            incident_elements = driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')

            for element in incident_elements:
                incident_type = element.get_attribute('class')
                position = element.get_attribute('style')

                incident = {
                    'type': incident_type,
                    'position': position,
                    'timestamp': datetime.datetime.now().isoformat()
                }

                producer.produce('waze-topic', value=json.dumps(incident).encode('utf-8'))
                print(f"Sent incident to Kafka: {incident}")

            producer.flush()
            print("Scraping cycle completed. Waiting 20 seconds before next cycle...")
            time.sleep(20)  # Wait for 20 seconds before the next cycle

    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Waiting for Kafka to be ready...")
    producer = create_kafka_producer()
    scrape_waze(producer)

