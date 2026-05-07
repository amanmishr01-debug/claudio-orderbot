# 🍕 Claudio Pizzeria - AI Order Assistant

An AI-powered ordering chatbot for Claudio Pizzeria built with Streamlit and OpenAI.

Customers can browse the full menu, select items via clickable buttons, and choose between pickup and delivery — all through a conversational interface.

## Features
- Full menu from Claudio Pizzeria (598 10th Ave, NYC)
- Clickable option buttons for easy ordering
- Pickup vs Delivery flow with ETA
- Order summary with itemized prices
- Responsive chat interface

## Setup

1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with your OpenAI API key:
   ```
   OPENAI_API_KEY = "sk-your-key-here"
   ```
4. Run: `streamlit run app.py`

## Deploy on Streamlit Community Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add your `OPENAI_API_KEY` in the Secrets section
5. Deploy!
