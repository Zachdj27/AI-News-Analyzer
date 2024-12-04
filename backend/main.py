from fastapi import FastAPI, Query
from pydantic import BaseModel
from transformers import pipeline, BartTokenizer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import finnhub
import os
from dotenv import load_dotenv


app= FastAPI()

load_dotenv()
API_KEY = os.getenv("API_KEY")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/company-news")
def get_data(
    symbol: str = Query(..., alias="symbol"),
    from_date: str = Query(..., alias="from"),
    to_date: str = Query(..., alias="to")
):
    finnhub_client = finnhub.Client(api_key=API_KEY)
    data = finnhub_client.company_news(symbol.upper(), _from=from_date, to=to_date)
    return data

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class Article(BaseModel):
    content: str
    
@app.post("/summarize")
def summarize_article(article: Article):
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    summary = summarizer(article.content, max_length=150, min_length=75, do_sample=False)
    return {"summary": summary[0]['summary_text']}

if __name__ == "__main__":
    print()
    uvicorn.run(app, host="127.0.0.1", port=8000)