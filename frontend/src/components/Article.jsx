import './Article.css'

function Article(props){
    return (
        <li className="article-box">
        <h3 className="article-title">{props.title}</h3>
        <p className="article-summary">{props.summary}</p>
        <a
            href={props.url}
            target="_blank"
            rel="noopener noreferrer"
            className="article-link"
        >
            Read more
        </a>
        </li>
    );
};

export default Article;
