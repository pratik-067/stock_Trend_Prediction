from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import streamlit as st
from tensorflow.keras.models import load_model
from datetime import date
from PIL import Image


img = Image.open("stock-market-crash.png")
start = '2011-01-01'
end = date.today()


st.header('Stock Trend Prediction')
st.image(img, use_column_width='auto')
user_input = st.text_input("Enter Stock Ticker", 'AAPL')

df = data.DataReader(user_input, 'yahoo', start, end)

# Discribing
st.subheader('Data from 2011 - 2021')
st.write(df.describe())

# visualization
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
plt.plot(df.Close)
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close, 'b', label='Closing Price')
plt.plot(ma100, 'r', label='100MA')
plt.legend()
st.pyplot(fig)


st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close, 'b', label='Closing Price')
plt.plot(ma100, 'r', label='100MA')
plt.plot(ma200, 'g', label='200MA')
plt.legend()
st.pyplot(fig)

# spliting data into traning and testing
data_training = pd.DataFrame(df['Close'][0: int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

print(data_training.head())
print(data_testing.head())

scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(data_training)

# #spliting data
# x_train = []
# y_train = []

# for i in range(100 , data_training_array.shape[0]):
#     x_train.append(data_training_array[i-100:i])
#     y_train.append(data_training_array[i,0])

# x_train,y_train = np.array(x_train),np.array(y_train)

# load model
model = load_model('keras_model.h5')

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_training, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i - 100: i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# making preadiction

y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor


# Final Graph

st.subheader('Prediction vs Orignal')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
st.pyplot(fig2)
