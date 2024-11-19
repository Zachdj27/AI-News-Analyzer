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
    //fetch news from api
    if (!companyName.trim()) return;

    console.log(import.meta.env.VITE_NEWS_API_KEY);
    const NEWS_API_KEY = import.meta.env.VITE_NEWS_API_KEY;

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

        setLoading(true);
        // process each article and get summaries
        const articleSummaries = await Promise.all(
          data.articles.map(async (article) => {
            const articleContent = article.content || article.description || "No content available"; 
            const summary = await summarizeArticle(articleContent);
            return summary;
          })
        );
        setSummaries(articleSummaries);
        setLoading(false);
      } else {
        console.log('No articles found.');
      }
    } catch (error) {
      console.error('Error fetching news:', error);
    }
  };


  return (
    <div className="App">
      <h1>AI News Summarizer</h1>
      <input
        rows="2"
        cols="20"
        placeholder="Type Company Name"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
        className="input-field"
      ></input>
      <br />
      <button onClick={fetchNews} className="fetch-button">Find Articles</button>
      <div className="articles-container">
        {loading && (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Summarizing...</p>
          </div>
        )}
        {articles.length > 0 && (
          <ul>
            {articles.map((article, index) => (
              <li key={index} className="article-box">
                <h3 className="article-title">{article.title}</h3>
                <p className="article-summary">{summaries[index]}</p>
                <a href={article.url} target="_blank" rel="noopener noreferrer" className="article-link">Read more</a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
      
  )
}

export default App
