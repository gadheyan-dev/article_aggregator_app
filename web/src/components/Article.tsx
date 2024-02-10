// Article.js
import React from 'react';

function Article({ url, title, image, summary, readTime, publishDate, authors }) {
  const formatReadTime = (minutes) => {
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
      <img className="card-img-top" src={image} alt="Card image cap" />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
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
        <a href="#" className="btn btn-primary">
          Go somewhere
        </a>
      </div>
    </div>
  );
}

export default Article;
