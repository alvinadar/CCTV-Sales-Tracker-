# 📹 CCTV Sales Analytics Dashboard

An interactive **Streamlit** web app for exploring and forecasting CCTV camera
sales data. It turns a raw pricing spreadsheet into clear, interactive charts
and makes simple time-series predictions for key business metrics.

---

## ✨ Features

### 📊 Sales Dashboard
- **Key KPI cards** — Total Revenue, Total Profit, Units Sold, and Average Margin at a glance.
- **Revenue by Year** — see how sales changed across 2020–2024.
- **Top Products by Revenue** — find the best-selling cameras.
- **Revenue by Region** — donut chart showing each country's share.
- **Profit by Sales Channel** — compare Direct, Distribution, and Online.
- **Avg Margin % by Camera Type** — which camera types are the most profitable.
- **Revenue by Industry** — which verticals (Government, Retail, etc.) spend the most.
- **Discount vs. Profit Margin scatter** — spot deals where heavy discounts hurt margins.
- **Deals Below Target Price** — counts and lists the worst under-target deals.
- **Interactive filters** for year, region, and product.
- **CSV export** of the filtered data.

### 🔮 KPI Forecast
Predicts future values for any key metric using three simple, transparent methods:
- **Straight-Line Trend** (linear regression, with an R² fit score)
- **Moving Average** (average of recent years)
- **Growth Rate / CAGR** (compound annual growth)

> ⚠️ **Note:** The dataset only contains 5 yearly data points, so forecasts are
> deliberately simple and clearly labelled as rough estimates — not business
> guarantees. Comparing the three methods shows how much uncertainty exists.

---

## 🛠️ Built With
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — web app framework
- [Pandas](https://pandas.pydata.org/) — data handling
- [Plotly](https://plotly.com/python/) — interactive charts
- [NumPy](https://numpy.org/) — forecasting math
- [openpyxl](https://openpyxl.readthedocs.io/) — reads the Excel file

---

## 🚀 Getting Started

### Prerequisites
Make sure you have **Python 3.9 or newer** installed.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cctv-sales-dashboard.git
   cd cctv-sales-dashboard
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

3. **Install the required libraries**
   ```bash
   pip install -r requirements.txt
   ```
   Or install them directly:
   ```bash
   pip install streamlit pandas plotly numpy openpyxl
   ```

### Running the App

Make sure `app.py` and `CCTV_Pricing_Data.xlsx` are in the **same folder**, then run:

```bash
streamlit run app.py
```

Your web browser will open the dashboard automatically (usually at
`http://localhost:8501`).

---

## 📁 Project Structure

```
cctv-sales-dashboard/
├── app.py                      # Main Streamlit application
├── CCTV_Pricing_Data.xlsx      # The sales dataset
├── CCTV_Dashboard_Explained.docx  # Beginner-friendly explanation of the code
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📊 About the Data

The dataset contains **174 CCTV camera sales records** spanning **2020–2024**,
across **6 regions** (Malaysia, Vietnam, Singapore, Thailand, Philippines,
Indonesia) and **10 product lines**. Each record includes pricing, discounts,
costs, customer details, sales channel, and target prices.

> Some calculated columns (Total Revenue, Gross Margin, Total Profit, etc.) are
> empty in the source file and are computed automatically by the app when it loads.

---

## 📖 Documentation

A friendly, beginner-level walkthrough of how the code works is included in
**`CCTV_Dashboard_Explained.docx`** — written so that even a complete newcomer
can follow along.

---

## 🔮 Possible Future Improvements
- Add an auto-generated "Key Insights" summary at the top of the dashboard.
- Support monthly/quarterly data for more advanced (seasonal) forecasting.
- Add confidence ranges (best-case / worst-case bands) to forecasts.
- Persist filter settings between sessions.

---

## 📝 License

This project is for educational purposes. Feel free to use and modify it.

---

*Made with ❤️ using Streamlit.*
