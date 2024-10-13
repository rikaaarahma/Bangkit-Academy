import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set seaborn style
sns.set(style='whitegrid')  # Use whitegrid for better readability

# Helper function to prepare various DataFrames
def create_monthly_orders_df(df):
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])  # Convert to datetime
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"  # Assuming price is used for total revenue
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_purchase_timestamp": "order_date",  # Rename for consistency
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return monthly_orders_df

def create_payment_method_df(df):
    payment_method_df = df.groupby('payment_type').agg(
        total_transaction_value=('payment_value', 'sum'),  # Total nilai transaksi
        transaction_count=('payment_value', 'size')  # Jumlah transaksi
    ).reset_index()
    
    return payment_method_df

# Load cleaned data from the working directory
all_df = pd.read_csv("data_merged.csv")  # Adjust this path according to your folder structure

# Ensure 'order_purchase_timestamp' is in datetime format
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Filter data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Get start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                  (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# Prepare various DataFrames
monthly_orders_df = create_monthly_orders_df(main_df)
payment_method_df = create_payment_method_df(main_df)

# Plot number of monthly orders
st.header('Monthly Order Trends and Payment Method Analysis')
st.subheader('Order Quantity Trend Over Time')

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

# Update the visual for monthly orders with better design principles
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["order_date"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#0077b6"  # Consistent color for the line
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.set_xlabel('Month', fontsize=15)
ax.set_ylabel('Order Count', fontsize=15)
ax.set_title('Monthly Order Trend', fontsize=20, fontweight='bold')

# Reduce the number of gridlines for cleaner visuals
ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.6)
ax.grid(False, axis='x')

st.pyplot(fig)

# Plot payment methods
st.subheader('Most Frequently Used Payment Methods and Transaction Amounts')

# Update visual for total transaction value by payment method
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x='payment_type', y='total_transaction_value', data=payment_method_df, ax=ax2, palette='Blues_d')
ax2.set_title('Total Transaction Value by Payment Method', fontsize=18, fontweight='bold')
ax2.set_ylabel('Total Transaction Value (in AUD)', fontsize=14)
ax2.set_xlabel('Payment Method', fontsize=14)
ax2.tick_params(axis='x', labelsize=12)
ax2.tick_params(axis='y', labelsize=12)

# Add data labels for better readability
for container in ax2.containers:
    ax2.bar_label(container, fmt='%0.0f', label_type='edge', fontsize=12)

st.pyplot(fig2)

# Plot transaction count by payment method
st.subheader('Transaction Count by Payment Method')

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(x='payment_type', y='transaction_count', data=payment_method_df, ax=ax3, palette='muted')
ax3.set_title('Transaction Count by Payment Method', fontsize=18, fontweight='bold')
ax3.set_ylabel('Transaction Count', fontsize=14)
ax3.set_xlabel('Payment Method', fontsize=14)
ax3.tick_params(axis='x', labelsize=12)
ax3.tick_params(axis='y', labelsize=12)

# Add data labels
for container in ax3.containers:
    ax3.bar_label(container, fmt='%0.0f', label_type='edge', fontsize=12)

st.pyplot(fig3)
