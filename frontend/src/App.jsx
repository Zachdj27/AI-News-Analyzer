import { useState } from 'react';
import axios from 'axios';
import Article from './components/Article'; // Assuming Article is in components folder

function App() {
  const [tickerSymbol, setTickerSymbol] = useState('');
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetching news from the backend API
  const fetchNews = async () => {
    if (!tickerSymbol.trim()) {
      alert("Please enter a ticker symbol.");
      return;
    }

    setLoading(true);
    setError(null); // Reset error before fetching new data

    try {
      const response = await axios.post('http://127.0.0.1:8000/process-news', {
        ticker_symbol: tickerSymbol.toUpperCase().trim(),
      });

      // Ensure the response structure matches what you're expecting
      console.log(response.data);

      setArticles(response.data.articles || []);
      setLoading(false);
    } catch (error) {
      console.log(error)
      setError("Error fetching news. Please try again later.");
      setLoading(false);
      console.error("Error fetching news:", error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen flex-col p-8">
      <h1 className="text-3xl font-bold mb-4">AI News Summarizer</h1>
      <textarea
        rows="2"
        cols="20"
        placeholder="Enter Ticker Symbol (e.g., AAPL)"
        value={tickerSymbol}
        onChange={(e) => setTickerSymbol(e.target.value)}
        className="input-field p-2 border rounded w-full max-w-md"
      />
      <button
        onClick={fetchNews}
        className="fetch-button mt-4 py-2 px-4 bg-green-500 text-white rounded hover:bg-green-600"
      >
        Find Articles
      </button>
      <div className="articles-container mt-8 w-full max-w-4xl">
        {loading && (
          <div className="loading-spinner flex flex-col items-center">
            <div className="spinner mb-2"></div>
            <p className="text-gray-600">Summarizing...</p>
          </div>
        )}
        {error && <p className="text-red-500 mt-4">{error}</p>}
        {articles.length > 0 && (
          <ul className="space-y-6">
            {articles.map((article, index) => (
              <Article
                key={index}
                title={article.article_name}
                summary={article.summary}
                sentiment={article.sentiment}
                sentiment_score={article.sentiment_score} 
                url={article.link}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
