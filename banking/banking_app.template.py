import csv
import json
import time
import random
import os
import logging
from datetime import datetime, timedelta
from faker import Faker
from kafka import KafkaProducer
from random import choice, uniform, randint

# Initialize Logger
logging.basicConfig(filename="banking_app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Faker instance
fake = Faker()

# Define Country, Currency, and City Data
COUNTRIES_DATA = {
    "United States": {
        "currency": "USD",
        "cities": ["New York City", "Los Angeles", "Chicago", "Houston", "San Francisco"],
        "country_code": "+1"
    },
    "Canada": {
        "currency": "CAD",
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "country_code": "+1"
    },
    "United Kingdom": {
        "currency": "GBP",
        "cities": ["London", "Manchester", "Birmingham", "Glasgow", "Edinburgh"],
        "country_code": "+44"
    },
    "Australia": {
        "currency": "AUD",
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "country_code": "+61"
    },
    "Germany": {
        "currency": "EUR",
        "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"],
        "country_code": "+49"
    },
    "France": {
        "currency": "EUR",
        "cities": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
        "country_code": "+33"
    },
    "Italy": {
        "currency": "EUR",
        "cities": ["Rome", "Milan", "Florence", "Venice", "Naples"],
        "country_code": "+39"
    },
    "Japan": {
        "currency": "JPY",
        "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya"],
        "country_code": "+81"
    },
    "China": {
        "currency": "CNY",
        "cities": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
        "country_code": "+86"
    },
    "India": {
        "currency": "INR",
        "cities": ["Delhi", "Mumbai", "Hyderabad", "Pune", "Dehradun"],
        "country_code": "+91"
    },
    "Brazil": {
        "currency": "BRL",
        "cities": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
        "country_code": "+55"
    },
    "South Africa": {
        "currency": "ZAR",
        "cities": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth"],
        "country_code": "+27"
    },
    "Mexico": {
        "currency": "MXN",
        "cities": ["Mexico City", "Guadalajara", "Monterrey", "Cancún", "Puebla"],
        "country_code": "+52"
    },
    "Russia": {
        "currency": "RUB",
        "cities": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"],
        "country_code": "+7"
    },
    "Spain": {
        "currency": "EUR",
        "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
        "country_code": "+34"
    },
    "South Korea": {
        "currency": "KRW",
        "cities": ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju"],
        "country_code": "+82"
    },
    "Turkey": {
        "currency": "TRY",
        "cities": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"],
        "country_code": "+90"
    },
    "Saudi Arabia": {
        "currency": "SAR",
        "cities": ["Riyadh", "Jeddah", "Mecca", "Medina", "Khobar"],
        "country_code": "+966"
    },
    "Argentina": {
        "currency": "ARS",
        "cities": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Mar del Plata"],
        "country_code": "+54"
    },
    "Egypt": {
        "currency": "EGP",
        "cities": ["Cairo", "Alexandria", "Giza", "Luxor", "Aswan"],
        "country_code": "+20"
    },
    "Thailand": {
        "currency": "THB",
        "cities": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Krabi"],
        "country_code": "+66"
    },
    "Indonesia": {
        "currency": "IDR",
        "cities": ["Jakarta", "Bali", "Surabaya", "Bandung", "Medan"],
        "country_code": "+62"
    },
    "Vietnam": {
        "currency": "VND",
        "cities": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Haiphong", "Nha Trang"],
        "country_code": "+84"
    }
}

# Function to generate a single banking transaction record
def generate_transaction():
    country = choice(list(COUNTRIES_DATA.keys()))
    city = choice(COUNTRIES_DATA[country]['cities'])
    currency = COUNTRIES_DATA[country]['currency']
    country_code = COUNTRIES_DATA[country]['country_code']
    
    transaction = {
        "transaction_id": fake.uuid4(),
        "transaction_timestamp": fake.iso8601(),
        "ingest_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "transaction_response_time": round(random.uniform(0.1, 2.5), 3),
        "mode_of_transaction": random.choice(["credit_card", "debit_card", "online_transfer", "ATM_withdrawal"]),
        "currency": currency,
        "country": country,
        "city": city,
        "transaction_amount": round(random.uniform(5.0, 5000.0), 2),
        "transaction_type": random.choice(["deposit", "withdrawal", "transfer"]),
        "account_type": random.choice(["checking", "savings", "credit_card"]),
        "payment_method": random.choice(["cash", "card", "online_banking"]),
        "transaction_status": random.choice(["successful", "failed", "pending"]),
        "customer_info": {
            "name": fake.name(),
            "age": random.randint(18, 75),
            "occupation": fake.job(),
            "mobile_number": f"{country_code}{fake.msisdn()[len(country_code):]}",
            "email": fake.email()
        },
        "merchant_info": {
            "name": fake.company(),
            "category": random.choice(["grocery", "electronics", "fashion", "entertainment", "food"]),
            "mobile_number": f"{country_code}{fake.msisdn()[len(country_code):]}",
            "email": fake.company_email()
        }
    }
    return transaction

# Kafka setup
def create_kafka_producer():
    retries = 5
    producer = None
    while retries > 0:
        try:
            producer = KafkaProducer(bootstrap_servers=['${KAFKA_BOOTSTRAP_SERVERS}'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            logger.info("Kafka connection established")
            return producer
        except Exception as e:
            logger.warning(f"Kafka is not ready, retrying... ({5 - retries + 1}/5)")
            retries -= 1
            time.sleep(60)

    if producer is None:
        logger.error("Failed to connect to Kafka after multiple retries.")
        raise ConnectionError("Failed to connect to Kafka after multiple retries.")
    return producer

# Function to publish data to Kafka
def publish_to_kafka(producer, topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        logger.info(f"Data published to Kafka topic {topic}")
    except Exception as e:
        logger.error(f"Failed to publish message to Kafka: {str(e)}")

if __name__ == "__main__":
    producer = create_kafka_producer()

    while True:
        try:
            transactions = [generate_transaction() for _ in range(100)]
            for transaction in transactions:
                publish_to_kafka(producer, "${KAFKA_TOPIC_1}", transaction)
                time.sleep(0.5)

        except KeyboardInterrupt:
            logger.info("Script interrupted by user. Exiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
