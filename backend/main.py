from fastapi import FastAPI, Query
from pydantic import BaseModel
from transformers import pipeline, BartTokenizer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import finnhub
import os
from dotenv import load_dotenv
from polygon import RESTClient
from web_scraping import fetch_article_content
from yfinance import Ticker


app= FastAPI()

load_dotenv()
API_KEY = os.getenv("API_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("text-classification", model="ProsusAI/finbert")

# @app.get("/company-news")
# def get_data(
#     symbol: str = Query(..., alias="symbol"),
#     from_date: str = Query(..., alias="from"),
#     to_date: str = Query(..., alias="to")
# ):
#     finnhub_client = finnhub.Client(api_key=API_KEY)
#     data = finnhub_client.company_news(symbol.upper(), _from=from_date, to=to_date)
#     return data

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/company-news")
def get_news(url):
    return fetch_article_content(url)

@app.post("/post-news")
def post_company_news(ticker_symbol):
    ticker = Ticker(ticker_symbol.upper().strip())
    news = ticker.get_news()
    
    i = 0
    articles = []
    while i < len(news) and len(articles) < 2:
        if news[i]['type'] == 'STORY':
            url = news[i]['link']
            content = get_news(url=url)
            if content:
                articles.append(content)
    return articles

@app.get("/company-data")
def get_data(ticker_symbol):
    ticker = Ticker(ticker_symbol)

class Article(BaseModel):
    content: str
    
@app.post("/analyze")
def analyze_article(sumarized_article: str):
    analysis = sentiment_analyzer(summarize_article)
    return analysis
    
@app.post("/summarize")
def summarize_article(news_article: str):
    max_input_length = 4096
    news_article = news_article[:max_input_length]
    
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    summary = summarizer(news_article, max_length=350, min_length=250, do_sample=False)
    return {"summary": summary[0]['summary_text']}


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    news = post_company_news("AAPL")
    summary = summarize_article(news[0])
    analysis = analyze_article(summary)
    print(analysis)
