### config
```
[connections.snowflake]
account = "xxxxxxx-xxxxxxx"
user = "xxx"
#private_key_file = "../xxx/xxx.p8"
private_key = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqh..................
JLoWWMhqcOyAlb6XMDB7r.................
eH7/b2RE+enmO1Wno6T/Xp0=
-----END PRIVATE KEY-----
"""
role = "SYSADMIN"
warehouse = "COMPUTE_WH"
database = "SMOOTHIES"
schema = "PUBLIC"
```

### create session 

```
import streamlit as st
from snowflake.snowpark.context import  get_active_session
from snowflake.snowpark.functions import col
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import requests  
from urllib.parse import quote
import pandas as pd

def get_snowflake_session():
    # 1. Get the key string from secrets
    key_str = st.secrets["connections"]["snowflake"]["private_key"]
    
    # 2. Convert the string to bytes and load it
    # If your key has a password, replace None with st.secrets["connections"]["snowflake"]["password"].encode()
    p_key = serialization.load_pem_private_key(
        key_str.encode(),
        password=None, 
        backend=default_backend()
    )

    # 3. Convert to DER format (bytes) as required by the driver
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 4. Create the connection
    # This passes the processed 'pkb' bytes directly to the connector
    conn = st.connection("snowflake", private_key=pkb)
    return conn.session()

session = get_snowflake_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))


```
### sue snoflake connector 

```
import snowflake.connector

# Connect using your credentials
ctx = snowflake.connector.connect(
    user='SYSADMIN',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT_LOCATOR',
    warehouse='COMPUTE_WH',
    database='SMOOTHIES',
    schema='PUBLIC'
)

# Create a cursor and execute SQL
cs = ctx.cursor()
cs.execute("SELECT FRUIT_NAME, SEARCH_ON FROM FRUIT_OPTIONS")

# Fetch results
data = cs.fetchall()

```

### compare 
Library,Syntax Style,Data Return Type,Ideal Use Case
Connector,Raw SQL,Tuples / Lists,"Fast, simple scripts"
Snowpark,DataFrame API,Snowpark DataFrame,Complex logic / ML / Streamlit
SQLAlchemy,ORM / SQL Expression,Objects / Rows,Web Apps / General Backend

