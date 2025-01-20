import './Article.css';

function Article(props) {
  const sentimentScore = Math.round(props.sentiment_score * 100); // Convert sentiment score to percentage

  return (
    <li
      key={props.index}
      className="article-box p-4 bg-gray-800 rounded-lg shadow-md"
    >
      <h3 className="article-title text-xl font-semibold mb-2">
        {props.title}
      </h3>
      <p className="article-summary text-gray-400 mb-4">
        {props.summary}
      </p>
      <a
        href={props.url}
        target="_blank"
        rel="noopener noreferrer"
        className="article-link text-blue-400 hover:text-blue-300"
      >
        Read more
      </a>

      {/* Sentiment Score Section */}
      <div className="sentiment-score mt-4">
        <p className="text-sm text-gray-400 mb-1">
          Sentiment Score: {sentimentScore}%
        </p>
        <div className="w-full bg-gray-700 rounded-full h-3">
          <div
            className="bg-green-500 h-3 rounded-full"
            style={{ width: `${sentimentScore}%` }}
          ></div>
        </div>
      </div>
    </li>
  );
}

export default Article;
