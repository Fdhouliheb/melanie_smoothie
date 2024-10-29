# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input('Name on Smothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

# Process ingredients selection
    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)  # Join selected ingredients into a single string
        for fruit_chosen in ingredients_list:
            try:
                # Make API request to get details about each fruit
                fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
                fruityvice_response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
                
                if fruityvice_response.status_code == 200:
                    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
                else:
                    st.warning(f"Failed to fetch details for {fruit_chosen}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch details for {fruit_chosen}: {str(e)}")

    my_insert_stmt = """ insert into smoothies.public.orders
    (ingredients, name_on_order)
    values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
