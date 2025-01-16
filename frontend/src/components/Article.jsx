import './Article.css'

function Article(props){
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
      </li>
    );
};

export default Article;
