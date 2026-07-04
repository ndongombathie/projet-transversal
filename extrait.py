import pandas as pd
from sqlalchemy import create_engine
from minio import Minio
import os

from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

engine = create_engine(
    f"mysql+pymysql://root:{PASSWORD}@localhost:3306/air_quality_db"
)


#recuperer les données donc la colonne updated_at a changé depuis la dernière 5 minutes exécution du script 
import datetime
last_run = datetime.datetime.now() - datetime.timedelta(minutes=5)
print(f"Récupération des données depuis : {last_run}")

query = """
SELECT *
FROM air_quality_data
WHERE timestamp > %s
"""""

df = pd.read_sql(query, engine, params=(last_run,))

csv_file = "air_quality.csv"

df.to_csv(csv_file, index=False)


client = Minio(
    "localhost:9000",
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

bucket = "air-quality"

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

client.fput_object(
    bucket,
    "air_quality.csv",
    csv_file,
    content_type="text/csv"
)

print("Export terminé")