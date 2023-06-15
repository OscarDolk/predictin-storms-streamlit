import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import toml
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import plotly.graph_objects as go


import streamlit as st

# Define page functions
def page1():
    #st.title('Fujita(EF) Predictor')
    # Add content for page 1

    st.title('Tornado Damage Estimator')

    #image = Image.open(r'images/storm.jpg')

    #st.image(image)

    st.markdown('''
    Welcome to the Tornado-impact estimator. The predictor will estimate the severity of the damages caused by a tornado, based on its characteristics (State, Duration, Tornado width, Tornado length and Date).

    The Fujita-scale rates the intensity of a tornado based on the damage inflicted
    on buildings and vegetation.
    ''')

    #st.image(image, width=600)
    #st.caption('https://www.iccsafe.org/building-safety-journal/bsj-dives/how-damage-determines-a-tornados-rating-from-fujita-to-enhanced-fujita/')
    #df = pd.read_csv("raw_data/dataframe.csv")
    #\\wsl.localhost\Ubuntu\home\oscardolk\code\OscarDolk\chbohne99\predicting-storms

    #df = pd.DataFrame(
    #np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    #    columns=['lat', 'lon'])

    #st.map(df)

    # Set the initial center coordinates for the map
    #initial_coords = [37.0902, -95.7129]

    #Plot the map from Charlotte################################################
    merg = pd.read_csv(r'raw_data/merg.csv')

    fig = go.Figure(data = go.Choropleth(
        locations = merg.code,
        z = merg.Count,
        locationmode = 'USA-states',
        colorscale = 'Greens',
        colorbar_title = 'Number of Tornadoes',
        text = merg.text)
)
    # fig.update_traces(textposition='inside')
    fig.update_layout(
        title_text = 'Number of Tornadoes per State in total, since 1950',
        geo_scope = 'usa'
    )
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    ############################################################################

    states = ['FLORIDA', 'ILLINOIS', 'OKLAHOMA', 'CALIFORNIA', 'MINNESOTA',
           'TEXAS', 'TENNESSEE', 'ALABAMA', 'WYOMING', 'WISCONSIN', 'OHIO',
           'NEBRASKA', 'INDIANA','GEORGIA', 'VIRGINIA', 'MISSOURI',
           'NORTH CAROLINA', 'COLORADO','NORTH DAKOTA', 'KANSAS', 'NEW YORK',
           'IOWA', 'MARYLAND','ARKANSAS', 'SOUTH CAROLINA', 'MONTANA',
           'SOUTH DAKOTA', 'IDAHO','PENNSYLVANIA','MICHIGAN', 'ARIZONA',
           'MISSISSIPPI', 'LOUISIANA','NEW MEXICO']

    sorted_states = sorted(states)
    STATE = st.selectbox(
        'Which State do you want to select?', sorted_states)

    #st.write('You selected:', STATE)
    #st.markdown('####')

    #option = st.selectbox(
    #    'What is the width of the Tornado',
    #    ('0-2 meters', '2-5 meters', '> 5 meters'))

    #st.write('You selected:', option)
    #
    #option = st.selectbox(
    #    'What is the length of the Tornado',
    #    ('0-2 meters', '2-5 meters', '> 5 meters'))


    #Tornado duration selection.####################################################
    st.markdown('''
    The typical lifetime for a strong Tornado is about eight minutes.
    In exceptional cases, violent events can last more than three hours.
    Please select the duration of your Tornado:
    ''')
    DURATION= st.slider('',0, 50, 4)
    #DURATION = st.number_input(' ')
    st.write("You selected a duration of:", DURATION, 'minutes.')
    st.markdown('####')



    #Tornado width selection########################################################
    st.markdown('''
    The width of Tornadoes can vary greatly. On average, a tornado is about 45 meters wide.
    Please select the width of your Tornado:
    ''')
    TOR_WIDTH = st.slider('', 0, 500, 10)
    #TOR_WIDTH = st.number_input('  ')
    st.write("You selected a width of:", TOR_WIDTH, 'meters.')
    st.markdown('####')

    #Tornado length selection########################################################
    st.markdown('''
    The length a Tornado travels can vary greatly. On average, a tornado travels a distance of 4,5 km before dissapearing.
    Please select the travel length of your Tornado:
    ''')
    TOR_LENGTH = st.slider('', 0, 100, 15)
    #TOR_LENGTH = st.number_input('')
    st.write("Ýou selected a travel length of:", TOR_LENGTH, 'kilometers.')
    st.markdown('####')
    #The max lenght of Tornadoes from the dataset is 643,737 kilometers.

    #Convert Tornado Width to meters.
    #Width of the tornado or tornado segment while on the ground (in feet).
    TOR_WIDTH = TOR_WIDTH /0.3048

    #Convert Tornado Length to meters.
    #Length of the tornado or tornado segment while on the ground (in miles to the tenth).
    TOR_LENGTH = TOR_LENGTH / 1.6093435

    #Tornado date selection#########################################################
    st.markdown('''
    Tornadoes can happen at any time and anywhere.
    Most Tornadoes occur between March and June. Please select a date for your Tornado.
    ''')
    today = date.today()
    #min_date = '1950-01-01'
    min_date = datetime(1950, 1, 1)
    #default_date = datetime(2022, 6, 15)
    BEGIN_DATE = st.date_input(
        'Select a date:', min_value=min_date, value=today)
    #    #datetime.date(today.year, today.month, today.day))
    #st.write('You have selected this date:', BEGIN_DATE)
    #BEGIN_DATE = st.date_input(
    #   "Choose the day of the tornado",
    #      datetime.date(2019, 7, 6), min_value=min_date)

    #BEGIN_DATE = st.text_input('Input date:')

    #Prediction#####################################################################
    #st.title('Predict the Damage for your tornado')
    damage_predict = st.button('Click here for Damage Prediction')


    params = {
        'Tornado_width': TOR_WIDTH,
        'Tornado_length': TOR_LENGTH,
        'Duration': DURATION,
        'Date': BEGIN_DATE,
        'State': STATE
    }

    # Make a request to the API
    if damage_predict:
        # Make a request to the API
        url = 'https://predicting-storms-image-hxduxswubq-ew.a.run.app/predict_scale'
        response = requests.get(url, params=params)
        #data = response.json()
        #Extract the value of "f_scale" from the response
        #f_scale_value = data["f_scale"]

    # Handle the response
        if response.status_code == 200:
            data = response.json()
            f_scale_value = data["f_scale"]
            # Display the extracted value
            #st.write(f_scale_value)
            if f_scale_value == 'Light Damage (EF0)':
                st.markdown("<span style='color: green; font-size: font-size: 42px;'>Predicted Result:</span> "
                            "<span style='color: green; font-size: 42px'>{}</span>".format(f_scale_value), unsafe_allow_html=True)
                st.markdown("<span style='color: green; font-size: 48px'>{}</span>".format('Estimated Cost: Up to $25.000'
                    "</div>",
                ), unsafe_allow_html=True)
            elif f_scale_value == 'Moderate Damage (EF1)':
                st.markdown("Predicted Result: <span style='color: orange; font-size: 42px' >{}</span>".format(f_scale_value), unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100vh;'>"
                    "<span style='color: orange; font-size: 48px'>{}</span>".format('Estimated Cost: $25.000 - $250.000'
                    "</div>",
                ), unsafe_allow_html=True)
            elif f_scale_value == 'Considerable Damage (EF2-EF5)':
                st.markdown("Predicted Result: <span style='color: red; font-size: 42px'>{}</span>".format(f_scale_value), unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100vh;'>"
                    "<span style='color: red; font-size: 48px'>{}</span>".format('Estimated Cost: Up to $3 Billion'
                    "</div>",
                ), unsafe_allow_html=True)
        else:
            st.write(f"Error: {response.status_code}")



def page2():
    st.title('Tornado Frequency Predictor')
    # Add content for page 2
    #Frequency Prediction#####################################################################
    st.title('Predict the frequency of Tornadoes')

    YEAR = st.selectbox('Choose a Year:', ('2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033'))

    frequency_predict = st.button('Click here for Frequency Prediction')


    YEAR = int(YEAR)

    params_frequency = {
        'year': YEAR
    }

    # Make a request to the API
    if frequency_predict:
        # Make a request to the API
        url = 'https://predicting-storms-image-hxduxswubq-ew.a.run.app/predict_frequency'
        response = requests.get(url, params=params_frequency)


    # Handle the response
        if response.status_code == 200:
            data = response.json()
            # Extract the value of "f_scale" from the response
            frequency = data["frequency"]

            # Create an empty placeholder
            #result_placeholder = st.empty()

            # Conditionally write the result based on frequency_predict
            if frequency_predict:
                # Display the extracted value
                # Write the text using Markdown
                st.markdown("Prediction Result: " + str(frequency))

                merg = pd.read_csv(r'raw_data/past_frequency.csv')

                X = merg['YEAR']
                y = merg['BEGIN_DATE_TIME']

                ##Calculate the trendline using numpy's polyfit
                coefficients = np.polyfit(X, y, 1)
                trendline = np.polyval(coefficients, X)
#
                ## Plot existing data as scatter plot
                #fig, ax = plt.subplots()
                #ax.scatter(X, y, label='Existing Data')
                #ax.plot(X, trendline, color='red', label='Trendline')
                #ax.set_xlabel('Year')
                #ax.set_ylabel('Frequency')
#
                ## Add the new value to the plot as a red dot
                #ax.scatter(YEAR, frequency, color='red', label='New Value')
                ##Display the plot in Streamlit
                #st.pyplot(fig)
#
                #plt.plot(X, y)
                #plt.title('Tornado Frequency US')
                #plt.xlabel('Year')
                #plt.ylabel('Frequency')
                #plt.show()

                # Plot existing data
                fig, ax = plt.subplots()
                ax.plot(X, y)
                ax.set_xlabel('Year')
                ax.set_ylabel('Frequency')
                #st.pyplot(fig)
                #
                ## Add the new value to the plot
                ax.plot(YEAR, frequency, 'ro')  # Assuming the new value corresponds to the last x-value
                # Add your own line with custom intercept and slope
                custom_intercept = -30000.89  # Replace with your own value
                custom_slope = 15.6458  # Replace with your own value

                # Calculate the line using custom intercept and slope
                custom_line = custom_intercept + custom_slope * X

                # Plot the custom line
                ax.plot(X, custom_line, color='red', label='Custom Line')

                # Display the plot
                #plt.legend()
                #plt.show()
                st.pyplot(fig)
#

                ##Using Streamlit's line_chart to plot the existing data##########
                #chart_data = pd.DataFrame({'Year': X, 'Frequency': y})
                #chart_data = chart_data.set_index('Year')
#
                #chart_data_with_labels = chart_data.copy()
                #chart_data_with_labels.columns = ['Frequency']
#
#
                ## Plot the line chart with labels
                #chart = st.line_chart(chart_data_with_labels)
#
                ## Add the new value to the plot
                #new_value_x = YEAR  # Assuming the new value corresponds to the last x-value
                #new_value_y = frequency  # Replace 'frequency' with the actual value you want to plot
#
#
                ## Add the red dot for the new value
                #chart.add_rows(pd.DataFrame({'Frequency': [new_value_y]}, index=[new_value_x]))
                #################################################################


        else:
            st.write(f"Error: {response.status_code}")

# Create page navigation
pages = {
    'Tornado Damage Estimator': page1,
    'Future Frequency Predictor': page2
}

# Add a sidebar for page selection
st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', list(pages.keys()))

# Run the selected page function
pages[selection]()

# Read the config file
config = toml.load("streamlit/config.toml")
theme = config.get("theme", {})

# Access theme values
primary_color = theme.get("primaryColor")
background_color = theme.get("backgroundColor")
secondary_background_color = theme.get("secondaryBackgroundColor")
text_color = theme.get("textColor")
font = theme.get("font")
