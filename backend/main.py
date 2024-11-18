from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, BartTokenizer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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
    summary = summarizer(article.content, max_length=75, min_length=25, do_sample=False)
    return {"summary": summary[0]['summary_text']}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)