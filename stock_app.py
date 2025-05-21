import streamlit as st
import yfinance as yf
import openai
import os

# Load API key from Streamlit secret
openai.api_key = os.getenv("openai_api_key")

st.set_page_config(page_title="GPT-4 Stock Advisor", page_icon="📈")
st.title("📈 GPT-4 Stock Investment Advisor")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA)", value="AAPL")

def fetch_and_analyze(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="7d")
    info = stock.info

    price_summary = hist[['Close']].tail(5).to_string()
    pe_ratio = info.get('trailingPE', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    summary = info.get('longBusinessSummary', 'No summary available.')

    prompt = f"""
You are a financial analyst. Analyze the following stock and provide an investment recommendation (Buy / Hold / Avoid). Include reasoning based on market cap, PE ratio, company summary, and price trend.

Ticker: {ticker}
PE Ratio: {pe_ratio}
Market Cap: {market_cap}

Company Summary:
{summary}

Recent Price Trend:
{price_summary}

Respond with a concise investment thesis and a clear recommendation.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert financial advisor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

if ticker:
    if st.button("Analyze with GPT-4"):
        with st.spinner("Analyzing..."):
            try:
                result = fetch_and_analyze(ticker)
                st.success("Analysis Complete ✅")
                st.markdown("### 📊 GPT-4 Investment Recommendation")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
