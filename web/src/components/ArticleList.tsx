// ArticleList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Article from './Article'; // Make sure to adjust the path

function ArticleList() {
  const [searchTerm, setSearchTerm] = useState('');
  const [articles, setArticles] = useState([]);

  const fetchArticles = async () => {
    try {
      const response = await axios.get(`http://localhost:8002/articles/?search=${searchTerm}`);
      setArticles(response.data.data); // Assuming the articles are nested under the 'data' property
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  const handleSearch = () => {
    if (searchTerm) {
      fetchArticles();
    }
  };

  return (
    <div className="container-fluid bg-dark p-4">
      <div className="input-group mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search articles..."
          className="form-control"
        />
        <div className="input-group-append">
          <button onClick={handleSearch} className="btn btn-primary" type="button">
            Search
          </button>
        </div>
      </div>

      <div className="row">
        {articles.map((article) => (
          <div key={article._id} className="col-md-4 mb-4">
            <Article title={article.title} image={article.top_image} description={article.summary} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArticleList;
