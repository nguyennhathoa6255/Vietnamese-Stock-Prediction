# Gọi các thư viện python để sử dụng
import streamlit as st
from datetime import date
from datetime import timedelta
import vnstock as vn
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from alpha_vantage.timeseries import TimeSeries
# import json
# import requests
# from bs4 import BeautifulSoup
from vnstock import *
from vnstock.chart import *
# from st_pages import Page, show_pages, add_page_title

# Tạo khoảng thời gian để lấy dễ dữ liệu training
START = "2020-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Thêm logo và tiêu đề cho ứng dụng
st.markdown("<h1 style='font-family: Arial; font-size: 25px; color: darkblue;'>Vietnamese Stock Prediction Application</h1>", unsafe_allow_html=True)
tab1, tab2, tab3= st.tabs(["Raw Data", "Prediction Data", "Ticker Info"])


# Tạo 3 tab cho ứng dụng
with tab1:
    with st.sidebar.container():
        st.image('Design/logo1.png', width=150)
        stock_list = listing_companies()
        stock_list1 = pd.DataFrame(stock_list)
        stocks = tuple(stock_list1['ticker'])
        selected_stock = st.selectbox('Select stock', stocks) # Tạo ô nhập hoặc chọn mã chứng khoán
        index = stock_list1['ticker'].tolist().index(selected_stock)
        organ_name = stock_list1['organName'].iloc[index]


    @st.cache_data # Lưu dữ liệu khi được tải lên streamlit
    
    # Tạo hàm load_data để gọi dữ liệu từ mã cổ phiếu
    def load_data(ticker):
        data = vn.stock_historical_data(ticker, START, TODAY)    
        return data


    data = load_data(selected_stock) # Gọi dữ liệu từ hàm load_data
   
    # Thêm tên sàn vào dữ dataframe vì data không có column 'exchangeName' là tên sàn
    san = company_overview(selected_stock)
    san1 = pd.DataFrame(san)
    data['exchangeName'] = san1.loc[0, 'exchange']
  
    with st.container():
        st.subheader(f'Thông tin về {organ_name}')
        company = pd.DataFrame(company_profile (selected_stock))
        company = company.drop('id', axis=1)
        company_trans = company.transpose()
        company_trans.columns = ['Info']
        st.write(company_trans)
   
        with st.form("Filter1"):    
            st.subheader('Raw Data')
            col1, col2, col3 = st.columns([0.4, 0.45, 0.15])
            with col1:
                start_date = st.date_input("Start", min_value=date(2021, 1, 1), max_value=date.today(), key="start_date", value=date(2023, 1, 1))
            with col2:
                end_date = st.date_input("End", min_value=date(2021, 1, 1), max_value=date.today(), key="end_date")
            #plot_raw_data(start_date, end_date)
            filtered_data = data[(data['time'] >= start_date) & (data['time'] <= end_date)]
            # fig = candlestick_chart(filtered_data, show_volume=False, figure_size=(6, 8), 
            #                     title=organ_name, x_label='Date', y_label='Price', 
            #                 )
            fig = candlestick_chart(filtered_data, ma_periods=[50,200], show_volume=False, reference_period=200, figure_size=(7, 8),
                        title=organ_name, x_label='Date', y_label='Price',
                        colors=('lightgray', 'gray'), reference_colors=('black', 'blue'))
            st.plotly_chart(fig)
            with st.expander("View tabular data"):
                filtered_data_table = data[(data['time'] >= end_date - timedelta(days=15)) & (data['time'] <= end_date)]
                st.write(filtered_data_table)
            with col3:
                submitted = st.form_submit_button("Filter")

with tab2:
    with st.container():
        n_months = st.number_input("**Enter the predicted number of months:**", value=1, step=1)
        period = n_months * 30 
        df_train = data[['time', 'close']]
        df_train = df_train.rename(columns={"time": "ds", "close":"y"})
        
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(period)
        forecast = m.predict(future)

        st.subheader(f'Dữ liệu dự đoán {organ_name}')
        filtered_fig1 = plot_plotly(m, forecast)
        st.plotly_chart(filtered_fig1, use_container_width=True)

        with st.expander("View tabular data"):
            forer = pd.DataFrame(forecast)
            forer = forer.drop(['additive_terms', 'additive_terms_upper', 'additive_terms_lower', 'weekly', 'weekly_lower', 'weekly_upper', 'yearly', 'yearly_upper', 'yearly_lower', 'multiplicative_terms', 'multiplicative_terms_lower', 'multiplicative_terms_upper'], axis=1)
            forer['ds'] = pd.to_datetime(forer['ds']).dt.date

            forer = forer.rename(columns={"ds": "time", "yhat": "predicted_price", 'yhat_lower': 'pred_price_lower', 'yhat_upper': 'pred_price_upper'})
            forer = forer.reindex(columns=['time', "predicted_price", "pred_price_lower", "pred_price_upper", "trend", "trend_lower", "trend_upper"])
            st.write(forer.tail(30))


with tab3:
    st.subheader('Ticker Info')
    st.write(listing_companies())