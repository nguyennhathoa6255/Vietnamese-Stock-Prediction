# Vietnamese Stock Prediction Application

Step by step: [Vietnamese Stock Prediction](https://nguyennhathoa6255.wixsite.com/hoasportfolio/about-1-3)
<br>
[App](https://vn-stock-prediction.streamlit.app/)

## The Summary

### Conclusion
Through the implementation of the Prophet algorithm, this project successfully generated predictions for stock prices with reasonable accuracy. The system analyzed historical patterns and trends in the stock market to forecast future price movements. The predictions can serve as a valuable tool for investors, aiding them in making informed decisions.
### Challenges
During the development process, several challenges were encountered. One of the main challenges was obtaining and preprocessing the relevant historical stock data. Ensuring data quality and consistency was crucial to obtaining accurate predictions. Additionally, interpreting and understanding the results of the predictions required domain knowledge and expertise in the stock market.
### Techniques
**Data Retrieval:** The project utilized the "Vnstock" library to fetch stock data. This library provided a convenient way to access and retrieve historical stock data for analysis and prediction.

**Data Cleaning and Transformation:** The "pandas" and "numpy" libraries were employed to clean and transform the retrieved data. These libraries offered powerful tools for handling missing values, removing duplicates, and performing necessary data manipulations to prepare the dataset for analysis.

**Prophet Algorithm:** The project utilized the "Prophet" algorithm for stock price prediction. Prophet is a time series forecasting algorithm developed by Facebook's Core Data Science team. It is designed to handle various components of time series data, such as trends, seasonality, and holidays.

**Streamlit Deployment:** The project leveraged the "streamlit" framework to deploy the code as a web application. Streamlit simplified the process of converting the code into an interactive web interface, allowing users to easily access and utilize the stock price prediction system. The deployment was done from a GitHub repository, ensuring seamless integration and version control.
