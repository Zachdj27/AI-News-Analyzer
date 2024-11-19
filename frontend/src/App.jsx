import { useState } from 'react'
import { summarizeArticle } from './api';
import './App.css'


function App() {
  const [companyName, setCompanyName] = useState('');
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState([]);

  const today = new Date();
  const formatter = new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  const formattedDate = formatter.format(today);

  const fetchNews = async () => {
    if (!companyName.trim()) return;
    const NEWS_API_KEY = process.env.REACT_APP_NEWS_API_KEY;

    const NEWS_API_URL = 'https://newsapi.org/v2/everything?' +
    `q=${companyName}&` +
    `from=${formattedDate}&` +
    'sortBy=popularity&' +
    'pageSize=5&' +
    `apiKey=${NEWS_API_KEY}`;

    try {
      const response = await fetch(NEWS_API_URL);
      const data = await response.json(); 
      if (data.articles && data.articles.length > 0) {
        setArticles(data.articles);
      } else {
        console.log('No articles found.');
      }
    } catch (error) {
      console.error('Error fetching news:', error);
    }
  };

  const handleSummarize = async () => {
    setLoading(true);
    for(let i = 0; i < articles.length; i++){
      setSummaries([]);
      const result = await summarizeArticle(article);
      setSummary(result);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>AI News Summarizer</h1>
      <textarea
        rows="2"
        cols="20"
        placeholder="Type Company Name"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
      ></textarea>
      <br />
      <button onClick={fetchNews}>Find Articles</button>
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Summarizing...</p>
        </div>
      )}
      {summaries && (
        <div>
          <h2>Summaries:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
      
  )
}

export default App
