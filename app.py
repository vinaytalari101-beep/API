import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "1070d6a3e4c8454d83ba4de693292403"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("News Filters")

country_options = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

category_options = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

selected_country = st.sidebar.selectbox(
    "Select Location",
    list(country_options.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Topic",
    category_options
)

keyword = st.sidebar.text_input(
    "Search Keywords",
    placeholder="AI, Cricket, Tesla..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=20
)

# -----------------------------
# Fetch News Function
# -----------------------------
@st.cache_data(ttl=300)
def fetch_news(country, category, keyword, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    if keyword.strip():
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "status": "error",
            "message": f"API Error: {response.status_code}"
        }

# -----------------------------
# UI Header
# -----------------------------
st.title("📰 Advanced News Dashboard")
st.markdown(
    "Search and filter breaking news by location, topic, and keywords."
)

# -----------------------------
# Get Data
# -----------------------------
country_code = country_options[selected_country]

data = fetch_news(
    country_code,
    selected_category,
    keyword,
    article_count
)

# -----------------------------
# Display Results
# -----------------------------
if data.get("status") == "ok":

    articles = data.get("articles", [])

    st.success(f"Found {len(articles)} articles")

    # Table View Data
    records = []

    for article in articles:
        records.append({
            "Title": article.get("title"),
            "Source": article.get("source", {}).get("name"),
            "Published": article.get("publishedAt"),
            "Author": article.get("author")
        })

    if records:
        df = pd.DataFrame(records)

        st.subheader("News Summary")
        st.dataframe(
            df,
            use_container_width=True
        )

    st.divider()

    # Detailed News Cards
    for article in articles:

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                image_url = article.get("urlToImage")
                if image_url:
                    st.image(image_url)

            with col2:
                st.subheader(article.get("title"))

                source = article.get("source", {}).get("name", "Unknown")

                published = article.get("publishedAt")

                try:
                    published = datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    ).strftime("%d %b %Y %H:%M")
                except:
                    pass

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                if article.get("description"):
                    st.write(article["description"])

                if article.get("content"):
                    st.write(article["content"][:250] + "...")

                st.link_button(
                    "Read Full Article",
                    article.get("url")
                )

            st.divider()

else:
    st.error(data.get("message", "Unable to fetch news"))