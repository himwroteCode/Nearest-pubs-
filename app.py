import pandas as pd
import numpy as np
import os
import folium

#Load data
org_df = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "open_pubs.csv"))
cleaned_df = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "data_cleaned_pub.csv"))

# Load the laptop details data from the csv file
open_pubs = pd.read_csv(org_df)
df = pd.read_csv(cleaned_df)


import streamlit as st

#Now making option menu
from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu(
         menu_title="The Pubs Guide",
         options=['About Pubs in  UK', 'Pubs Location',"Find Nearest Pub", 'About me'])


if selected=="About Pubs in  UK":
    st.title(":blue[Hello Night's lover]")
    st.write("In this pubs guide you'll get to know about some interesting facts about pubs.")
    st.write("And I'll also let you know about the data sets that I used to suggest you some nearest pubs location based on your current location")
    st.header(":red[Pubs in UK]")
    st.write(""" Here are some interesting facts about pubs in the UK:""")
    st.write(""":red[The] pub with the longest name in the UK is The Old Thirteenth Cheshire Astley Volunteer Rifleman Corps Inn in Stalybridge, Greater Manchester1.""")
    st.write(""":blue[The] largest pub in the UK is the Moon Under the Water; this Wetherspoon pub was originally built as the Regal cinema in 1937 and seated 1,300 people1.""")

    st.write(":red[The] most expensive pint served in London was a Leffe beer that cost £5.80 at the Coach and Horses in 20102.")
    st.write(":blue[The] most expensive cocktail served in London was at the Dukes Hotel in St. James. The £5,500 drink contained vintage bitters, 19th Century cognac, and 18th Century curacao2.")
    st.write(":red[Pub] culture is an integral part of British life, especially student life. Pubs are a place to go to socialise, relax and have a drink3.")
    "I hope you find these facts interesting!"

    st.header(":blue[About the dataset]")
    
    st.subheader(":green[Original data]")
    st.write(open_pubs)

    st.subheader(":orange[Cleaned data]")
    st.write(df)
##########################################################################################
if selected=="Pubs Location":
    st.title("See the  names and address of pubs of your desired city or postal codes.")
    # Allow user to choose between searching by postal code or local authority
    search_type = st.radio("Search by:", ('Postal Code', 'Local Authority'))

# Create a list of unique postal codes or local authorities to display in the dropdown menu
    if search_type == 'Postal Code':
        search_list = sorted(df['postcode'].unique())
    else:
        search_list = sorted(df['local_authority'].unique())

# Allow user to select a postal code or local authority from the dropdown menu
    search_value = st.selectbox(f"Select a {search_type}:", search_list)

# Filter the dataset based on the selected postal code or local authority
    if search_type == 'Postal Code':
        filtered_data = df[df['postcode'] == search_value]
    else:
        filtered_data = df[df['local_authority'] == search_value]

# Display the filtered dataset
    st.write(f"Displaying {len(filtered_data)} pubs in {search_value}:")
    st.dataframe(filtered_data)
# Create a map centered on the chosen location
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=13)



if selected=="Find Nearest Pub":
    st.title(":blue[Find the  nearest pub from your current location], :red[here!]")
    #Take input -latitude and longitude
    col1,col2=st.columns(2)
    with col1:
        lat=st.number_input(label=":blue[Enter Latitude Here]", min_value=49.892485, max_value=60.764969)
    with col2:
        lon=st.number_input(label=":red[Enter Longitude Here]", min_value=-7.384525, max_value=1.757763)

    #Entered location
    search_location=np.array((lat,lon))
#Original/available Location
    original_location=np.array([df['latitude'],df['longitude']]).T
#Finding Euclidean distance
    dist=np.sum((original_location-search_location)**2, axis=1)
#Adding Distance column to dataframe
    df['Distance']=dist

#Asking user that how many nearest Pub they want to see
#nearest=st.slider(label="How Many Nearest Pub You Want to See",
 #                  min_value=1, max_value=50, value=5)
    data=df.sort_values(by='Distance', ascending=True)[:5]

#List of Bar Names
#st.subheader( Nearest Pubs:")

    st.subheader("See in the map below, Nearest Pubs to your current location")
    st.map(data=data, zoom=None, use_container_width=True)

    st.subheader(":blue[Here] are the Names and Address of Nearby Pubs found to near your current location")
    st.table(data[['name','address','local_authority']])

if selected=="About me":
    st.header("About myself")
    st.write("""I am :blue[Himanshu Vaish], I have given a task to make a pubs suggesting google map kind of web app, that suggest the pub based on current location of user. 
    If you have any  question/suggestion/query then please connect me anywhere in the links given below.
    :blue[Thank you]
    
    """)
    st.write(":red[My GitHub profile is] [here](https://github.com/himwroteCode).")
    st.write(":blue[My Linkedin profile is] [here](https://www.linkedin.com/in/vaishhimanshu/).")
