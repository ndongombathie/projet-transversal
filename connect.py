from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092"
)

future = producer.send(
    "air-quality",
    b"hello"
)

print(future.get(timeout=10))