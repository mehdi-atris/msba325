import pandas as pd
import plotly.express as px
import streamlit as st

url1 = "https://raw.githubusercontent.com/mehdi-atris/msba325/main/sales_data_sample.csv"
url2 = "https://raw.githubusercontent.com/mehdi-atris/msba325/main/football_stadiums.csv"

# Import Data for First Visualization
data1 = pd.read_csv(url1)
# Import Data for Second Visualzation
data2 = pd.read_csv(url2)

# Title
st.title('My Two Visualizations')
# Subtitle
st.header('Mehdi Atris')


# Seperate Title and Subtitle from First Visualization
st.markdown('---')


# First Visualization
st.subheader('First Visualization: Sales Across Countries')
st.markdown("Hello! Our first Visualization here shows a pie chart of which countries asupermarket sells to. You can move the slider around to group countries whose total sales to are under less than the percentage you pick!")
# Group Data by Country + Calculate Quantity Ordered in Each Country
country_orders = data1.groupby('COUNTRY')['QUANTITYORDERED'].sum().reset_index()

# Total Quantity ordered
total_quantity_ordered = country_orders['QUANTITYORDERED'].sum()

# Slider Widget: Allow Users to Set a Threshold as a Percentage of the Total Quantity Ordered
percentage_threshold = st.slider("Threshold for Grouping Small Countries (%)", min_value=0, max_value=100, step=1, value=10, key="percentage_threshold_key")

# Convert Selected Percentage Threshold to an Absolute Threshold Value
threshold = int((percentage_threshold / 100) * total_quantity_ordered)

# Function that Updates the Chart
def update_chart(threshold):
    # Group Smaller Countries and Sum Their Quantities
    grouped_country_orders = country_orders.copy()
    grouped_country_orders.loc[grouped_country_orders['QUANTITYORDERED'] < threshold, 'COUNTRY'] = 'Other Countries'
    grouped_country_orders = grouped_country_orders.groupby('COUNTRY')['QUANTITYORDERED'].sum().reset_index()

    # Pie Chart
    fig = px.pie(grouped_country_orders, names='COUNTRY', values='QUANTITYORDERED', title='Quantity Ordered by Country')

    # Show Plot
    st.plotly_chart(fig)

# Initial Chart Display
update_chart(threshold)


# Seperate Title and Subtitle From First Visualization
st.markdown('---')


# Second Visualization
st.subheader('Second Visualization: Football Stadiums')
st.markdown("Here you can learn more about football stadiums around the world! Below is a treemap showing the number of football stadiums in each Confederation shown in a treemap.")

# Group Data by Confederation and Count the Number of Stadiums in Each Confederation
confederation_counts = data2['Confederation'].value_counts().reset_index()
confederation_counts.columns = ['Confederation', 'Stadium Count']

# Create Treemap using Plotly Express
fig_treemap = px.treemap(confederation_counts, path=['Confederation'], values='Stadium Count',
                         title='Number of Stadiums in Each Confederation')

# Display Treemap in Streamlit
st.plotly_chart(fig_treemap)

st.text("Just select the Confederation you would like to look at and another interconfederation treemap will appear showing you the countries along with how many stadiums they have!")

# Allow User to Select a Confederation
selected_confederation = st.selectbox("Select a Confederation:", confederation_counts['Confederation'].unique())

# Filter Data for Selected Confederation
selected_confederation_data = data2[data2['Confederation'] == selected_confederation]

# Group Data by Country and Count Number of Stadiums in Each Country within Selected Confederation
country_stadium_counts = selected_confederation_data['Country'].value_counts().reset_index()
country_stadium_counts.columns = ['Country', 'Stadium Count']

# Create Treemap for Stadiums in Each Country within Selected Confederation
fig_country_treemap = px.treemap(country_stadium_counts, path=['Country'], values='Stadium Count',
                                 title=f'Number of Stadiums in Each Country within {selected_confederation} Confederation')

# Display Treemap for Stadiums in Each Country within the Selected Confederation
st.plotly_chart(fig_country_treemap)
