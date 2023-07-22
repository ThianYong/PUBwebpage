import streamlit as st
import pandas as pd
from datetime import datetime

# Define the placeholder for the GitHub data directory URL
data_dir_url = "https://raw.githubusercontent.com/ThianYong/PUBwebpage/446d43ad09ad5c32b24e53954375f4d2499121c8/data/"

# Load existing data or create an empty DataFrame if no data exists
try:
    data = pd.read_csv(data_dir_url + 'plc_cpu_data.csv')
except FileNotFoundError:
    data = pd.DataFrame(columns=['Brand', 'Model', 'CPU Speed (MHz)', 'RAM (MB)', 'Ethernet Ports', 'Price (SGD)', 'Timestamp'])

# Set the title of the app
st.title("PLC CPU Data Entry")

# Input fields
brand = st.text_input("Enter the brand of the PLC CPU:")
model = st.text_input("Enter the model of the PLC CPU:")
cpu_speed = st.number_input("Enter the CPU speed (MHz):", min_value=0, step=1)
ram = st.number_input("Enter the RAM (MB):", min_value=0, step=1)
ethernet_ports = st.number_input("Enter the number of Ethernet ports:", min_value=0, step=1)
price = st.number_input("Enter the price (SGD):", min_value=0, step=1)

# Add a divider between data entry and display
st.markdown("---")

def save_data_to_csv(brand, model, cpu_speed, ram, ethernet_ports, price, data):
    # Capture current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_entry = {
        'Brand': brand,
        'Model': model,
        'CPU Speed (MHz)': cpu_speed,
        'RAM (MB)': ram,
        'Ethernet Ports': ethernet_ports,
        'Price (SGD)': price,
        'Timestamp': timestamp
    }

    # Append the data entry to the existing data
    new_data = pd.DataFrame(data_entry, index=[0])
    data = pd.concat([data, new_data], ignore_index=True)

    # Save the updated data to CSV on GitHub
    data.to_csv(data_dir_url + 'plc_cpu_data.csv', index=False)
    return data

if st.button("Save Data"):
    data = save_data_to_csv(brand, model, cpu_speed, ram, ethernet_ports, price, data)
    st.success("Data saved successfully!")

# Display the entered data in a table
st.subheader("Entered Data:")
st.table(data)

# Select brand and model for trend plotting
st.subheader("Select Brand and Model for Trend Plotting:")
selected_brand = st.selectbox("Select Brand:", data['Brand'].unique())
selected_model = st.selectbox("Select Model:", data[data['Brand'] == selected_brand]['Model'].unique())

# Filter data based on selected brand and model
selected_data = data[(data['Brand'] == selected_brand) & (data['Model'] == selected_model)]

# Plot the trend of price changes for the selected brand and model using native Streamlit line chart
if not selected_data.empty:
    st.subheader("Price Trend:")
    st.line_chart(selected_data['Price (SGD)'])
else:
    st.warning("No data available for the selected brand and model.")