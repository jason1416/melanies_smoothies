# Import python packages.
import streamlit as st
from snowflake.snowpark.context import  get_active_session
from snowflake.snowpark.functions import col
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

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
st.success("Connected to Snowflake!")
# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your cusom Smoothie!
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on Smoothie will be:", name_on_order)


#session = get_active_session()
#conn = st.connection("snowflake")
#session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        

    
