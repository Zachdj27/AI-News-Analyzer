import { useState } from 'react'
import { summarizeArticle } from './api';
import './App.css'

function App() {
  const [article, setArticle] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!article.trim()) return;
    setLoading(true);
    setSummary('');
    const result = await summarizeArticle(article);
    setSummary(result);
  };

  return (
    <div className="App">
      <h1>AI News Summarizer</h1>
      <textarea
        rows="10"
        cols="50"
        placeholder="Paste your article here..."
        value={article}
        onChange={(e) => setArticle(e.target.value)}
      ></textarea>
      <br />
      <button onClick={handleSummarize}>Summarize</button>
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Summarizing...</p>
        </div>
      )}
      {summary && (
        <div>
          <h2>Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
      
  )
}

export default App
