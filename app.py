"""
=============================================================================
  CCTV SALES ANALYTICS DASHBOARD
=============================================================================
A Streamlit web app for exploring and forecasting CCTV camera sales data.

  1) SALES DASHBOARD -> Turns the CCTV pricing spreadsheet into easy-to-read
                        charts and numbers (revenue, profit, best products,
                        regions, channels, margins, and more).

  2) KPI FORECAST    -> Looks at how key numbers changed over the years and
                        makes simple time-series predictions for the future.

HOW TO RUN THIS FILE:
  1) Install the libraries (only needed once):
        pip install streamlit pandas plotly numpy openpyxl
  2) Put this file and "CCTV_Pricing_Data.xlsx" in the SAME folder.
  3) In a terminal, type:
        streamlit run app.py
  4) Your web browser will open the dashboard automatically.
=============================================================================
"""

# ---------------------------------------------------------------------------
# STEP 1: Import the tools (libraries) we need.
# Think of these like grabbing different boxes of LEGO before we build.
# ---------------------------------------------------------------------------
import streamlit as st          # builds the website/app
import pandas as pd             # reads and works with table data (the spreadsheet)
import plotly.express as px     # makes pretty, interactive charts
import plotly.graph_objects as go  # lets us draw custom lines (for forecasts)
import numpy as np              # does the math for our trend-line prediction

# ---------------------------------------------------------------------------
# STEP 2: Set up the page (title in the browser tab, layout, icon).
# This must be the FIRST Streamlit command we run.
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CCTV Dashboard + Helper",  # text shown on the browser tab
    page_icon="📹",                          # little icon on the browser tab
    layout="wide",                           # use the full width of the screen
)


# ---------------------------------------------------------------------------
# STEP 3: Load the spreadsheet and clean it up.
#
# @st.cache_data is a "memory helper". It tells Streamlit:
#   "Read the file once, then remember it, so the app stays fast."
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Read the Excel file into a "DataFrame" (a table, like a smart spreadsheet)
    df = pd.read_excel("CCTV_Pricing_Data.xlsx")

    # The spreadsheet left some columns blank, so we calculate them ourselves.
    # Each line below fills in one missing column using simple math.

    # Effective Selling Price = the actual price after discount.
    # If it's blank, just use the normal Selling Price.
    df["Effective Selling Price ($)"] = df["Effective Selling Price ($)"].fillna(
        df["Selling Price ($)"]
    )

    # Gross Margin ($) = money made on ONE camera = price - cost to get it here
    df["Gross Margin ($)"] = (
        df["Effective Selling Price ($)"] - df["Landed Cost ($)"]
    )

    # Gross Margin (%) = profit as a percentage of the price.
    # (We multiply by 100 to turn 0.45 into 45%.)
    df["Gross Margin (%)"] = (
        df["Gross Margin ($)"] / df["Effective Selling Price ($)"] * 100
    )

    # Total Revenue ($) = price of one camera x how many were sold
    df["Total Revenue ($)"] = (
        df["Effective Selling Price ($)"] * df["Units Sold"]
    )

    # Total Landed Cost ($) = cost of one camera x how many were sold
    df["Total Landed Cost ($)"] = df["Landed Cost ($)"] * df["Units Sold"]

    # Total Gross Profit ($) = total money in - total money spent
    df["Total Gross Profit ($)"] = (
        df["Total Revenue ($)"] - df["Total Landed Cost ($)"]
    )

    # Make the Year a whole number (e.g. 2020 not 2020.0) so it looks clean.
    df["Time Period (Year)"] = df["Time Period (Year)"].astype(int)

    return df  # hand the finished table back to whoever asked for it


# Try to load the data. If the file is missing, show a friendly message
# instead of a scary error, then stop the app politely.
try:
    df = load_data()
    DATA_LOADED = True
except FileNotFoundError:
    DATA_LOADED = False


# ---------------------------------------------------------------------------
# STEP 4: Build the sidebar menu.
# The sidebar is the panel on the left. We use it to switch between the
# different "pages" of our app (Dashboard, To-Do, Timer, etc.).
# ---------------------------------------------------------------------------
st.sidebar.title("📋 Menu")
page = st.sidebar.radio(
    "Go to:",
    [
        "📊 Sales Dashboard",
        "🔮 KPI Forecast",
    ],
)


# ===========================================================================
#  PAGE 1: SALES DASHBOARD
# ===========================================================================
def show_dashboard():
    st.title("📹 CCTV Sales Dashboard")
    st.write("Explore camera sales, revenue, and profit across the years.")

    # If the data file is missing, explain how to fix it and stop here.
    if not DATA_LOADED:
        st.error(
            "Could not find 'CCTV_Pricing_Data.xlsx'. "
            "Please put it in the same folder as this app, then refresh."
        )
        return

    # -------------------- FILTERS (in the sidebar) --------------------
    # Filters let the user pick what data they want to see.
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Filters")

    # Build a list of years, regions, and products to choose from.
    # sorted(...) puts them in a tidy order.
    years = sorted(df["Time Period (Year)"].unique())
    regions = sorted(df["Region"].dropna().unique())
    products = sorted(df["Product Name"].dropna().unique())

    # multiselect = a box where you can tick MANY options.
    # By default we select everything (default=...).
    chosen_years = st.sidebar.multiselect("Year", years, default=years)
    chosen_regions = st.sidebar.multiselect("Region", regions, default=regions)
    chosen_products = st.sidebar.multiselect("Product", products, default=products)

    # Apply the filters: keep only rows that match ALL the chosen options.
    # The "&" means AND, and ".isin(...)" means "is in this list".
    filtered = df[
        (df["Time Period (Year)"].isin(chosen_years))
        & (df["Region"].isin(chosen_regions))
        & (df["Product Name"].isin(chosen_products))
    ]

    # If the filters remove everything, warn the user instead of crashing.
    if filtered.empty:
        st.warning("No data matches your filters. Try selecting more options.")
        return

    # -------------------- KPI CARDS (the big numbers) --------------------
    # KPI = Key Performance Indicator = the most important numbers at a glance.
    st.subheader("Key Numbers")

    # st.columns(4) splits the row into 4 side-by-side boxes.
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = filtered["Total Revenue ($)"].sum()
    total_profit = filtered["Total Gross Profit ($)"].sum()
    total_units = filtered["Units Sold"].sum()
    avg_margin = filtered["Gross Margin (%)"].mean()

    # st.metric shows a label and a big number.
    # The f"..." with {:,.0f} adds commas and removes decimals (e.g. 1,234,567).
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
    col3.metric("📦 Units Sold", f"{total_units:,.0f}")
    col4.metric("🎯 Avg Margin", f"{avg_margin:.1f}%")

    st.markdown("---")  # draws a horizontal line to separate sections

    # -------------------- CHART 1: Revenue over the years --------------------
    st.subheader("Revenue by Year")

    # groupby = "group rows that share the same year, then add up revenue".
    # reset_index() turns the result back into a normal table.
    revenue_by_year = (
        filtered.groupby("Time Period (Year)")["Total Revenue ($)"]
        .sum()
        .reset_index()
    )

    # Make a bar chart. x = years, y = revenue.
    fig_year = px.bar(
        revenue_by_year,
        x="Time Period (Year)",
        y="Total Revenue ($)",
        text_auto=".2s",                 # show the value on each bar
        color="Total Revenue ($)",       # color bars by their height
        color_continuous_scale="Blues",  # use a blue color theme
    )
    fig_year.update_layout(showlegend=False)
    st.plotly_chart(fig_year, use_container_width=True)

    # -------------------- TWO CHARTS SIDE BY SIDE --------------------
    left, right = st.columns(2)

    # CHART 2 (left): Top products by revenue
    with left:
        st.subheader("Top Products by Revenue")
        top_products = (
            filtered.groupby("Product Name")["Total Revenue ($)"]
            .sum()
            .sort_values(ascending=False)   # biggest first
            .reset_index()
        )
        fig_prod = px.bar(
            top_products,
            x="Total Revenue ($)",
            y="Product Name",
            orientation="h",               # horizontal bars are easier to read here
            text_auto=".2s",
            color="Total Revenue ($)",
            color_continuous_scale="Teal",
        )
        fig_prod.update_layout(
            showlegend=False,
            yaxis={"categoryorder": "total ascending"},  # nicest order
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    # CHART 3 (right): Revenue share by region (a pie/donut chart)
    with right:
        st.subheader("Revenue by Region")
        region_rev = (
            filtered.groupby("Region")["Total Revenue ($)"].sum().reset_index()
        )
        fig_region = px.pie(
            region_rev,
            names="Region",
            values="Total Revenue ($)",
            hole=0.4,                      # the hole makes it a donut shape
        )
        st.plotly_chart(fig_region, use_container_width=True)

    # -------------------- CHART 4: Profit by channel --------------------
    st.subheader("Profit by Sales Channel")
    channel_profit = (
        filtered.groupby("Channel")["Total Gross Profit ($)"].sum().reset_index()
    )
    fig_channel = px.bar(
        channel_profit,
        x="Channel",
        y="Total Gross Profit ($)",
        text_auto=".2s",
        color="Channel",
    )
    fig_channel.update_layout(showlegend=False)
    st.plotly_chart(fig_channel, use_container_width=True)

    # -------------------- CHART 5 & 6: more analysis side by side --------------------
    left2, right2 = st.columns(2)

    # CHART 5 (left): Average gross margin % by camera type.
    # This shows which kinds of cameras are the most profitable to sell.
    with left2:
        st.subheader("Avg Margin % by Camera Type")
        margin_by_type = (
            filtered.groupby("Camera Type")["Gross Margin (%)"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig_type = px.bar(
            margin_by_type,
            x="Camera Type",
            y="Gross Margin (%)",
            text_auto=".1f",
            color="Gross Margin (%)",
            color_continuous_scale="Greens",
        )
        fig_type.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_type, use_container_width=True)

    # CHART 6 (right): Revenue by industry/vertical.
    # Shows which kinds of customers (Government, Retail, etc.) buy the most.
    with right2:
        st.subheader("Revenue by Industry")
        vertical_rev = (
            filtered.groupby("Vertical / Industry")["Total Revenue ($)"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        fig_vert = px.bar(
            vertical_rev,
            x="Total Revenue ($)",
            y="Vertical / Industry",
            orientation="h",
            text_auto=".2s",
            color="Total Revenue ($)",
            color_continuous_scale="Purples",
        )
        fig_vert.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_vert, use_container_width=True)

    # -------------------- CHART 7: Discount vs Margin (pricing health) --------------------
    # Each dot is one sale. The x-axis is how big a discount was given, and the
    # y-axis is the profit margin. This helps spot when big discounts are
    # eating into profit too much.
    st.subheader("Discount vs. Profit Margin (Pricing Health Check)")
    st.caption(
        "Each dot is one sale. Dots far to the right got big discounts. "
        "If those dots are also low down, the discount hurt the profit a lot."
    )
    # Turn the discount fraction (e.g. 0.21) into a percentage (21) for clarity.
    scatter_df = filtered.copy()
    scatter_df["Discount %"] = scatter_df["Discount (%)"] * 100
    fig_scatter = px.scatter(
        scatter_df,
        x="Discount %",
        y="Gross Margin (%)",
        color="Camera Type",
        size="Units Sold",
        hover_data=["Product Name", "Customer / Account Name", "Region"],
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # -------------------- INSIGHT: deals priced below target --------------------
    # The data has a "Variance to Target ($)" column. A negative number means
    # the camera was sold for LESS than the company's target price.
    st.subheader("⚠️ Deals Sold Below Target Price")
    below_target = filtered[filtered["Variance to Target ($)"] < 0]
    pct_below = (len(below_target) / len(filtered) * 100) if len(filtered) else 0

    c1, c2 = st.columns(2)
    c1.metric("Deals below target", f"{len(below_target)} of {len(filtered)}")
    c2.metric("Share below target", f"{pct_below:.0f}%")

    if not below_target.empty:
        st.caption("The 10 deals furthest below their target price:")
        worst = below_target.nsmallest(10, "Variance to Target ($)")[
            [
                "Product Name",
                "Customer / Account Name",
                "Region",
                "Time Period (Year)",
                "Variance to Target ($)",
            ]
        ]
        st.dataframe(worst, use_container_width=True, hide_index=True)

    # -------------------- THE RAW DATA TABLE --------------------
    # An expander is a section you can click to open or close.
    with st.expander("🔍 See the detailed data table"):
        st.dataframe(filtered, use_container_width=True)

        # Let the user download the filtered data as a CSV file.
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download this data as CSV",
            data=csv,
            file_name="filtered_cctv_data.csv",
            mime="text/csv",
        )


# ===========================================================================
#  PAGE: KPI FORECAST (Time Series Prediction)
#  Looks at how a number changed over the years and guesses the future.
#
#  IMPORTANT TEACHING NOTE:
#  We only have 5 years of data (2020-2024). That is VERY little. So we use
#  three SIMPLE, easy-to-understand methods instead of complicated ones.
#  We always show the prediction as a rough estimate, never as a sure thing.
# ===========================================================================
def show_forecast():
    st.title("🔮 KPI Forecast (Time Series Prediction)")
    st.write(
        "Pick an important number (a KPI), and the app will look at how it "
        "changed each year and make a simple guess about future years."
    )

    if not DATA_LOADED:
        st.error(
            "Could not find 'CCTV_Pricing_Data.xlsx'. "
            "Please put it in the same folder as this app, then refresh."
        )
        return

    # A friendly warning so the student understands the limits. Being honest
    # about uncertainty is a real data-science skill!
    st.warning(
        "⚠️ Heads up: we only have 5 years of data. That is too little for "
        "fancy forecasting, so these predictions are ROUGH ESTIMATES meant "
        "for learning — not real business promises!"
    )

    # -------------------- STEP 1: Let the user pick a KPI --------------------
    # A dictionary maps a friendly name -> the real column + how to add it up.
    # "sum" means add everything; "mean" means take the average.
    kpi_options = {
        "Total Revenue ($)": ("Total Revenue ($)", "sum"),
        "Total Gross Profit ($)": ("Total Gross Profit ($)", "sum"),
        "Units Sold": ("Units Sold", "sum"),
        "Average Gross Margin (%)": ("Gross Margin (%)", "mean"),
    }

    chosen_kpi = st.selectbox("Which KPI do you want to predict?", list(kpi_options))
    column, how = kpi_options[chosen_kpi]

    # How many future years to predict, chosen with a slider.
    years_ahead = st.slider("How many years into the future?", 1, 5, 2)

    # -------------------- STEP 2: Build the yearly history --------------------
    # Group all rows by year and either sum or average the chosen column.
    if how == "sum":
        history = df.groupby("Time Period (Year)")[column].sum()
    else:
        history = df.groupby("Time Period (Year)")[column].mean()

    history = history.sort_index()           # make sure years are in order
    years = history.index.to_numpy()          # e.g. [2020, 2021, 2022, 2023, 2024]
    values = history.to_numpy()               # the KPI value for each year

    # The future years we want to predict, e.g. [2025, 2026]
    future_years = np.array(
        [years[-1] + i for i in range(1, years_ahead + 1)]
    )

    # -------------------- STEP 3: Let the user pick a method --------------------
    st.markdown("---")
    method = st.radio(
        "Choose a prediction method:",
        ["📏 Straight-Line Trend", "📊 Moving Average", "📈 Growth Rate (CAGR)"],
        horizontal=True,
    )

    # We'll fill these in below depending on the method.
    future_values = None
    explanation = ""

    # METHOD 1: Straight-line trend (also called linear regression).
    # We draw the best straight line through the dots and extend it forward.
    if method == "📏 Straight-Line Trend":
        # np.polyfit with degree 1 finds the best-fitting straight line.
        # It gives us "slope" (how steep) and "intercept" (where it starts).
        slope, intercept = np.polyfit(years, values, 1)

        # Predict future years using the line: y = slope * year + intercept
        future_values = slope * future_years + intercept

        # R-squared tells us how well the line fits (0 = bad, 1 = perfect).
        predicted_history = slope * years + intercept
        ss_res = ((values - predicted_history) ** 2).sum()
        ss_tot = ((values - values.mean()) ** 2).sum()
        r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0

        explanation = (
            f"We drew the best straight line through the years and extended it. "
            f"The line's 'fit score' (R²) is **{r_squared:.2f}** "
            f"(closer to 1.00 means the years follow a straighter line; "
            f"a low score means the data jumps around a lot)."
        )

    # METHOD 2: Moving average. We average the last few years and assume
    # the future looks like that average.
    elif method == "📊 Moving Average":
        window = st.slider("How many recent years to average?", 2, len(years), 3)
        recent_average = values[-window:].mean()      # average of last N years
        # Every future year gets the same predicted value (the average).
        future_values = np.array([recent_average] * years_ahead)
        explanation = (
            f"We took the average of the last **{window} years** "
            f"(${recent_average:,.0f} or so) and assumed the future stays "
            f"around that level. This is good when numbers bounce up and down "
            f"with no clear direction."
        )

    # METHOD 3: Growth rate (CAGR = Compound Annual Growth Rate).
    # We figure out the average yearly % change and keep applying it.
    else:
        start, end = values[0], values[-1]
        n_steps = len(years) - 1
        # CAGR formula: (end / start) ^ (1 / number_of_years) - 1
        if start > 0:
            cagr = (end / start) ** (1 / n_steps) - 1
        else:
            cagr = 0

        # Apply the growth rate again and again for each future year.
        future_values = np.array(
            [end * (1 + cagr) ** i for i in range(1, years_ahead + 1)]
        )
        explanation = (
            f"We measured the average yearly growth from {years[0]} to "
            f"{years[-1]}, which is about **{cagr * 100:.1f}% per year**, "
            f"then kept growing by that rate. This is good for numbers that "
            f"steadily rise (or fall) over time."
        )

    # -------------------- STEP 4: Show the prediction --------------------
    st.markdown("---")
    st.subheader(f"Prediction for {chosen_kpi}")
    st.write(explanation)

    # Show the predicted future values as big metric cards.
    cols = st.columns(len(future_years))
    for i, (yr, val) in enumerate(zip(future_years, future_values)):
        # Decimals only for the percentage KPI; whole numbers otherwise.
        if "%" in chosen_kpi:
            cols[i].metric(f"{yr} (est.)", f"{val:.1f}%")
        else:
            cols[i].metric(f"{yr} (est.)", f"${val:,.0f}" if "$" in chosen_kpi else f"{val:,.0f}")

    # -------------------- STEP 5: Draw the chart --------------------
    # Blue solid line = real history. Orange dashed line = our prediction.
    fig = go.Figure()

    # The real, known history (solid blue line with dots).
    fig.add_trace(
        go.Scatter(
            x=years,
            y=values,
            mode="lines+markers",
            name="Actual (real data)",
            line=dict(color="#2E75B6", width=3),
            marker=dict(size=9),
        )
    )

    # Connect the last real point to the first prediction so the line
    # doesn't have a gap. We glue them together here.
    bridge_x = np.concatenate([[years[-1]], future_years])
    bridge_y = np.concatenate([[values[-1]], future_values])

    # The prediction (dashed orange line with dots).
    fig.add_trace(
        go.Scatter(
            x=bridge_x,
            y=bridge_y,
            mode="lines+markers",
            name="Forecast (our guess)",
            line=dict(color="#E8833A", width=3, dash="dash"),
            marker=dict(size=9, symbol="diamond"),
        )
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=chosen_kpi,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1),
    )
    # Force the x-axis to show whole years (2020, not 2020.5).
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)

    # -------------------- STEP 6: Show the numbers in a table --------------------
    with st.expander("🔍 See the history and forecast as a table"):
        hist_table = pd.DataFrame(
            {"Year": years, chosen_kpi: values, "Type": "Actual"}
        )
        fcast_table = pd.DataFrame(
            {"Year": future_years, chosen_kpi: future_values, "Type": "Forecast"}
        )
        combined = pd.concat([hist_table, fcast_table], ignore_index=True)
        st.dataframe(combined, use_container_width=True)

    # A final teaching tip comparing the methods.
    st.info(
        "💡 Tip: Try switching between the three methods above and watch how "
        "the prediction changes! When methods disagree a lot, it means the "
        "future is genuinely hard to predict — and that's okay to admit."
    )



# ===========================================================================
#  STEP 5: DECIDE WHICH PAGE TO SHOW
#  Based on what the user clicked in the sidebar menu, we call the matching
#  function from above. This is the "traffic controller" of the app.
# ===========================================================================
if page == "📊 Sales Dashboard":
    show_dashboard()
elif page == "🔮 KPI Forecast":
    show_forecast()

# A small footer shown at the bottom of the sidebar on every page.
st.sidebar.markdown("---")
st.sidebar.caption("Made using Streamlit")
