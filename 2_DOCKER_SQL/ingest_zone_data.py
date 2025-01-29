import os
import pandas as pd
from sqlalchemy import create_engine

df=pd.read_csv("taxi_zone_lookup.csv")
engine=create_engine("postgresql://postgres:postgres@localhost:5433/ny_taxi")
df.to_sql(name="zones",con=engine,if_exists="replace")
