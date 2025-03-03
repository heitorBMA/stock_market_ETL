# ETL Pipeline for Currency and Stock Price Data

Welcome to my portfolio project! This repository demonstrates an end-to-end ETL pipeline that collects, processes, and visualizes financial data.

This project is still in development, so this file and the overall structure may have some eventual changes if I see that something can be done in a better way, if you have any questions about the project or have any sugestions for improvments feel free to send me an email on heitorbragalves@gmail.com or connect with me on linkedin (https://www.linkedin.com/in/heitor-braga/).

## Project Overview

This project is focused on:
- **Extracting** financial data on currency exchange rates and stock prices from Alpha Vantage free API.
- **Transforming** the raw data by cleaning and preparing it for analysis.
- **Loading** the processed data into a MySQL database for structured storage.
- **Visualizing** the data using Power BI to generate actionable insights.

## Repository Structure

```
.
├── etl_scripts/
│   ├── extract.py                  # Script for extracting data from the API
│   ├── transform_and_load.py       # Script for process the data and load it into a MySQL database
│
├── dictionary_of_names/        
│   ├── digital_currency_list.csv   # csv file with the list of available crypto currencies to collet data
│   ├── physical_currency_list.csv  # csv file with the list of available physical currencies to collet data
│
├── collected_data/            # Folder containing the collected data
│
├── power_bi_dashboard.pbix         # Power BI file for data visualization
│
├── follow_list.json                # json file containing the list of stocks and currencies to collect the data
│
├── .gitgnore                       # gitgnore file to make the .env file be ignored by git
│
├── .env                            # File containing the API credentials (not included in the public repository for data security reasons)
│
├── requirements.txt                # txt file withe the python dependencies
│
└── README.md                       # Project documentation
```

## Key Features

1. **Data Extraction**
   - Uses a public financial API to fetch real-time currency exchange rates and stock price data.
   - Supports custom date ranges for historical data retrieval.

2. **Data Transformation**
   - Cleans and formats raw data.
   - Handles missing values and ensures consistency.
   - Prepares data for loading into the database.

3. **Data Loading**
   - Loads transformed data into a MySQL database.
   - Includes database schema creation and data validation steps.

4. **Data Visualization**
   - Power BI dashboard provides insights into trends and performance metrics.
   - Interactive visualizations for exploring currency and stock price data.

## Getting Started

### Prerequisites

- **Python 3.8+**
- **MySQL** (Server and client tools)
- **Power BI Desktop**
- API key for the financial data source (e.g., Alpha Vantage, Yahoo Finance, or similar).

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/heitorBMA/stock_market_ETL.git
   cd stock_market_ETL
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Create a database and user in MySQL.
   - Create a .env file with your database credentials.

4. Configure the API:
   - Obtain a free API key from Alpha Vantage.
   - Update the .env file with your API key.

### Usage

1. Run the ETL pipeline:
   ```bash
   python etl_scripts/extract.py
   python etl_scripts/transform_and_load.py
   ```


## Future Enhancements

- Continue development of the ETL pipeline
- Automate the pipeline using a scheduler like **Apache Airflow** or **pentaho**.
- Develop the Power BI dashboard.

## Contributing

Contributions are welcome! If you have suggestions for improving the project, feel free to send me an email on heitorbragalves@gmail.com or connect with me on linkedin (https://www.linkedin.com/in/heitor-braga/).

## License

This project is not licensed so the code is free to use in any way you want.

## Contact

For any questions or inquiries, please reach out to me:
- **Email**: heitorbragalves@gmail.com
- **LinkedIn**: [Heitor Braga](https://www.linkedin.com/in/heitor-braga/)
- **GitHub**: [heitorBMA](https://github.com/heitorBMA)

---

Thank you for visiting this project! I hope it demonstrates my skills and expertise effectively. Feedback is always appreciated!

