interface Author {
  name: string;
}

interface ArticleProps {
  url: string;
  domain: string;
  title: string;
  image: string;
  summary: string;
  readTime: number;
  publishDate: string; // Assuming publishDate is a string, adjust if necessary
  authors?: Author[];
}

function Article({ url, domain, title, image, summary, readTime, publishDate, authors }: ArticleProps) {
  const formatReadTime = (minutes: number) => {
    if (minutes < 60) {
      return `${Math.round(minutes)} min read`;
    } else {
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = Math.round(minutes % 60);
      return `${hours}h ${remainingMinutes}min read`;
    }
  };

  return (
    <div className="card">
      <img className="card-img-top" src={image} alt="Card image cap" style={{ height: '400px', objectFit: 'cover' }}/>
      <div className="card-body">
        <h5 className="card-title">
          <a href={url} target="_blank" rel="noopener noreferrer">{title}</a>
        </h5>
        <div className="card-text">
          {authors && authors.length > 0 && (
            <span className="text-muted">
              <i className="bi bi-person"></i> {authors[0].name}
            </span>
          )}
          <span className="text-muted ms-2">
            <i className="bi bi-clock"></i> {formatReadTime(readTime)}
          </span>
          <span className="text-muted ms-2">
            <i className="bi bi-calendar"></i> {new Date(publishDate).toLocaleDateString('en-GB', {
              day: 'numeric',
              month: 'long',
              year: 'numeric',
            })}
          </span>
        </div>
        <p className="card-text mt-3">{summary}</p>
        <a href={url} className="btn btn-primary">
          Full Article
        </a>
        <a href={domain} className="btn btn-primary"  style={{ marginLeft: '10px' }}>
          Website
        </a>
      </div>
    </div>
  );
}

export default Article;
