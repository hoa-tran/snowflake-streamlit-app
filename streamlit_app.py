import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


st.title("My Parents New Healthy Dinner")

st.header("Breakfast Favorites")
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Avocado Toast")


st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

fruit_list = fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)




st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:

        st.write('The user entered ', fruit_choice)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        st.dataframe(fruityvice_normalized)
except URLError as e:
    st.error()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute('select * from fruit_load_list')
my_data_row = my_cur.fetchall()
st.text("The fruit load list contains:")
st.dataframe(my_data_row)


fruit_to_add= st.text_input('What fruit would you like to add')
st.write('Thanks for adding ', fruit_to_add)
