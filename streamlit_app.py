# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("My parents New healthy diner !")
st.write(
    """the new healthy dinner!
    """
)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your smoothie will be", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to five ingredients :',my_dataframe, max_selections =5)
if ingredients_list :
 #st.write(ingredients_list)
 #st.text(ingredients_list)
   ingredients_string =''
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen +' '
       st.subheader(fruit_chosen + ' Nutrition information')
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
       fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
 #st.write(ingredients_string)

 my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
 time_to_insert = st.button('Submit Order')
 st.write(my_insert_stmt)
#st.stop()
 if time_to_insert :
     session.sql(my_insert_stmt).collect()
     st.success('Your smoothie is ordered!', icon="✅")
    

