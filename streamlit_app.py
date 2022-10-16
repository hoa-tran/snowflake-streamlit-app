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

def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:

        fruityvice_normalized = get_fruityvice_data(fruit_choice)
        st.dataframe(fruityvice_normalized)
except URLError as e:
    st.error()

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute('select * from fruit_load_list')
        return my_cur.fetchall()


if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    st.text("The fruit load list contains:")
    st.dataframe(my_data_row)

#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +" ')")
        return 'Thanks for adding ' + new_fruit

fruit_to_add= st.text_input('What fruit would you like to add')
if st.button('Add Fruit to the List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    text_from_insert_row_snfl = insert_row_snowflake(fruit_to_add)
    st.write(text_from_insert_row_snfl)
