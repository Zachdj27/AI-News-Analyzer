import { useState } from 'react'
import { summarizeArticle } from './api';
import './App.css'
import Article from './components/Article';

function App() {
  const [tickerSymbol, setTickerSymbol] = useState('');
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState([]);

  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  const formattedToday = formatDate(today);
  const formattedYesterday = formatDate(yesterday);

  const fetchNews = async () => {
    //fetch news from api
    if (!tickerSymbol.trim()) return;

    const NEWS_API_KEY = import.meta.env.VITE_NEWS_API_KEY;
    const API_ENDPOINT = 'https://finnhub.io/api/v1';

    // const api_key = finnhub.ApiClient.instance.authentications['api_key'];
    // api_key.apiKey = NEWS_API_KEY;
    // const finnhubClient = new finnhub.DefaultApi()


    // function getCompanyNews(symbol, from, to) {
    //   return new Promise((resolve, reject) => {
    //       finnhubClient.companyNews(symbol, from, to, (error, data, response) => {
    //           if (error) {
    //               reject(error); 
    //           } else {
    //               resolve(data); 
    //           }
    //       });
    //   });
    // }

    try {
      // const response = await getCompanyNews(tickerSymbol, formattedYesterday, formattedToday);
      //console.log(`https://finnhub.io/api/v1/company-news?symbol=${tickerSymbol}&from=${formattedYesterday}&to=${formattedToday}`);
      const response = await fetch(`${API_ENDPOINT}/company-news?symbol=${tickerSymbol}&from=${formattedYesterday}&to=${formattedToday}&token=${NEWS_API_KEY}`);
      // fetch(`${API_ENDPOINT}/company-news?symbol=AAPL&from=2024-12-02&to=2024-12-03&token=${NEWS_API_KEY}`)
      //   .then(response => response.json())
      //   .then(data => console.log(data));


      const data = await response.json();

      // if (data.articles && data.articles.length > 0) {
      //   setArticles(data.articles);

      //   setLoading(true);
      //   // process each article and get summaries
      //   const articleSummaries = await Promise.all(
      //     data.articles.map(async (article) => {
      //       const articleContent = article.content || article.description || "No content available"; 
      //       // const summary = await summarizeArticle(articleContent);
      //       const summary = articleContent;
      //       return summary;
      //     })
      //   );

      setLoading(true);
      const summaries = [];
      const articles = [];
      let i = 0;
      console.log(data.length);
      while (summaries.length < 8 && i < data.length){
        const article = data[i];
        const summary = article.summary;
        if (summary.length > 0){
          articles.push(article);
          summaries.push(summary);
        }
        i++;
      }
      setArticles(articles);
      setSummaries(summaries);
      setLoading(false);
      // } else {
      //   console.log('No articles found.');
      // }
    } catch (error) {
      console.error('Error fetching news:', error);
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen flex-col p-8">
    <h1 className="text-3xl font-bold mb-4">AI News Summarizer</h1>
    <input
      rows="2"
      cols="20"
      placeholder="Type Company Name"
      value={tickerSymbol}
      onChange={(e) => setTickerSymbol(e.target.value)}
      className="input-field p-2 border rounded"
    />
    <br />
    <button onClick={fetchNews} className="fetch-button mt-4 py-2 px-4 bg-green-500 text-white rounded">
      Find Articles
    </button>
    <div className="articles-container mt-8 w-full max-w-4xl">
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Summarizing...</p>
        </div>
      )}
      {articles.length > 0 && (
        <ul className="space-y-6">
          {articles.map((article, index) => (
            <Article            
              key={index}
              summary={summaries[index]}
              url={article.url}/>
   
          ))}
        </ul>
      )}
    </div>
  </div>
  
      
  )
}

export default App
