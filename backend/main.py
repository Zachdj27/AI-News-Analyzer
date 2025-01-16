from fastapi import FastAPI, Query
from pydantic import BaseModel
from transformers import pipeline, BartTokenizer
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

@app.post("/process-news")
def process_news(ticker_symbol: str):
    # Fetch news for the ticker symbol
    ticker = Ticker(ticker_symbol.upper().strip())
    news = ticker.get_news()
    
    i = 0
    articles = []

    if not news: 
        print("No news available.")
    else:
        while i < len(news) and len(articles) < 2:
            try:
                item = news[i]
                if item.get("type") == "STORY": 
                    url = item.get("link")
                    if not url:
                        print(f"Skipping news item at index {i}: Missing URL.")
                        i += 1
                        continue

                    print("Fetching article content")
                    content = fetch_article_content(url)
                    print("Summarizing")
                    if content:
                        if len(content) <= 40 :
                            i += 1
                            continue
                        if len(content) < 110:
                            summary_text = content
                        else:
                            summary = summarizer(content, max_length=350, min_length=100, do_sample=False)
                            summary_text = summary[0]["summary_text"]

                        print("Analyzing")
                        sentiment_result = sentiment_analyzer(summary_text)[0]
                        sentiment_label = sentiment_result["label"]
                        sentiment_score = sentiment_result["score"]

                        # Add the article data to the list
                        new_article = {
                            "article_name": item.get("title", "No Title"),
                            "summary": summary_text,
                            "link": url,
                            "sentiment": sentiment_label,
                            "sentiment_score": sentiment_score
                        }
                        print(new_article)
                        articles.append(new_article)
                i += 1
            except IndexError as e:
                print(f"IndexError at index {i}: {e}")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                i += 1  

    # Calculate overall sentiment score
    if articles:
        total_score = sum(article["sentiment_score"] for article in articles)
        overall_sentiment_score = total_score / len(articles)
    else:
        overall_sentiment_score = 0.0

    return{
        "articles": articles,
        "overall_sentiment_score": overall_sentiment_score
    }

    
if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    news = process_news("AAPL")
    print(news)

# @app.get("/company-news")
# def get_news(url):
#     return fetch_article_content(url)

# @app.post("/post-news")
# def post_company_news(ticker_symbol):
#     ticker = Ticker(ticker_symbol.upper().strip())
#     news = ticker.get_news()
    
#     i = 0
#     articles = []
#     while i < len(news) and len(articles) < 2:
#         if news[i]['type'] == 'STORY':
#             url = news[i]['link']
#             content = get_news(url=url)
#             if content:
#                 articles.append(content)
#         i += 1
#     return articles

# @app.get("/company-data")
# def get_data(ticker_symbol):
#     ticker = Ticker(ticker_symbol)

# class Article(BaseModel):
#     content: str
    
# @app.post("/analyze")
# def analyze_article(summarized_article: str):
#     analysis = sentiment_analyzer(summarized_article)
#     return analysis
    
# @app.post("/summarize")
# def summarize_article(news_article: str):
#     if len(news_article) < 120:
#         return news_article
#     max_input_length = 4096
#     news_article = news_article[:max_input_length]
    
#     tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
#     summary = summarizer(news_article, max_length=350, min_length=100, do_sample=False)
#     return str(summary[0]['summary_text'])


# if __name__ == "__main__":
#     # uvicorn.run(app, host="127.0.0.1", port=8000)
#     news = post_company_news("AAPL")
#     summary = summarize_article(news[0])
#     analysis = analyze_article(summary)
#     print(analysis)
