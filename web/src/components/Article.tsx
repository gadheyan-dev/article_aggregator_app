// Article.js
import React from 'react';

function Article({ title, image, description }) {
  return (
    <div className="card" style={{ width: '18rem' }}>
      <img className="card-img-top" src={image} alt="Card image cap" />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{description}</p>
        <a href="#" className="btn btn-primary">
          Go somewhere
        </a>
      </div>
    </div>
  );
}

export default Article;
