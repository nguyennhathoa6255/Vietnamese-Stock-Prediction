# Gọi các thư viện python để sử dụng
from datetime import date, timedelta
import vnstock as vn
from vnstock.chart import *
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly

# Thiết lập page
st.set_page_config(
    layout="wide",  
    page_title="Vietnamese Stock Prediction",      
    page_icon="🧊"  
)

# Thêm logo và tiêu đề cho ứng dụng
st.markdown("<h1 style='font-family: Arial; font-size: 25px; color: darkblue;'>Vietnamese Stock Prediction</h1>", unsafe_allow_html=True)

# Tạo ô chọn cổ phiếu
stock_list = pd.DataFrame(vn.listing_companies())
stocks = tuple(stock_list['ticker'])
selected_stock = st.selectbox('Select stock', stocks) # Tạo ô nhập hoặc chọn mã chứng khoán
index = stock_list['ticker'].tolist().index(selected_stock)
organ_name = stock_list['organName'].iloc[index]

@st.cache_data # Lưu dữ liệu khi được tải lên streamlit
    
# Tạo hàm load_data để gọi dữ liệu từ mã cổ phiếu
def load_data(ticker):
    # Tạo khoảng thời gian để lấy dễ dữ liệu training
    START = "2020-01-01"
    TODAY = date.today().strftime("%Y-%m-%d") # Lấy realtime
    data = vn.stock_historical_data(ticker, START, TODAY)    
    return data

# Gọi dữ liệu từ hàm load_data
data = load_data(selected_stock)

# Thêm tên sàn vào dataframe vì dữ liệu không có cột tên sàn
add_exchange = pd.DataFrame(vn.company_overview(selected_stock))
data['exchange'] = add_exchange.loc[0, 'exchange']

# Tạo 3 tab cho ứng dụng:
tab1, tab2= st.tabs(["Real-time Data", "Prediction Data"])

with tab1: 
    st.subheader('Real-time Data')
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        start_date = st.date_input("Start", min_value=date(2021, 1, 1), max_value=date.today(), key="start_date", value=date(2023, 1, 1))
    with col2:
        end_date = st.date_input("End", min_value=date(2021, 1, 1), max_value=date.today(), key="end_date")

    filtered_data = data[(data['time'] >= start_date) & (data['time'] <= end_date)]
    
    fig = candlestick_chart(filtered_data, show_volume=True,
                title=organ_name, x_label='Time', y_label='Close Price',
                colors=('#99FFCC', '#FF6666'))
    st.plotly_chart(fig)

    with st.expander("**View tabular data**"):
        filtered_data_table = data[(data['time'] >= end_date - timedelta(days=15)) & (data['time'] <= end_date)]
        st.write(filtered_data_table)

with tab2:
    st.subheader('Prediction Data')
    n_months = st.number_input("**Enter the predicted number of months:**", value=1, step=1)
    period = n_months * 30 
    df_train = data[['time', 'close']]
    df_train = df_train.rename(columns={"time": "ds", "close":"y"})
    
    # Train model
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(period)
    forecast = m.predict(future)

    st.write(f'**Dữ liệu dự đoán {organ_name}**')
    filtered_fig = plot_plotly(m, forecast)
    st.plotly_chart(filtered_fig, use_container_width=True)

    with st.expander("**View tabular data**"):
        forer = pd.DataFrame(forecast)
        forer = forer.drop(['additive_terms', 'additive_terms_upper', 'additive_terms_lower', 'weekly', 'weekly_lower', 'weekly_upper', 'yearly', 'yearly_upper', 'yearly_lower', 'multiplicative_terms', 'multiplicative_terms_lower', 'multiplicative_terms_upper'], axis=1)
        forer['ds'] = pd.to_datetime(forer['ds']).dt.date

        forer = forer.rename(columns={"ds": "time", "yhat": "predicted_price", 'yhat_lower': 'pred_price_lower', 'yhat_upper': 'pred_price_upper'})
        forer = forer.reindex(columns=['time', "predicted_price", "pred_price_lower", "pred_price_upper", "trend", "trend_lower", "trend_upper"])
        st.write(forer.tail(30))
