// ArticleList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Article from './Article'; // Make sure to adjust the path

function ArticleList() {
  const [searchTerm, setSearchTerm] = useState('');
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8002/articles/?search=${searchTerm}`);
      setArticles(response.data.data); // Assuming the articles are nested under the 'data' property
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchTerm) {
      fetchArticles();
    }
  };

  return (
    <div className="container-fluid bg-dark p-4 min-vh-100 ">
      <div className="input-group mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search articles..."
          className="form-control form-control-sm" // Smaller input
        />
        <div className="input-group-append">
          <button
            onClick={handleSearch}
            className={`btn btn-primary ${loading ? 'disabled' : ''}`}
            type="button"
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>
      </div>

      {articles.length === 0 && !loading && (
        <p className="text-light text-center">No articles found. Try a different search term.</p>
      )}

      <div className="row">
        {articles.map((article) => (
          <>
            <div className="col-3" key={`spacer-left-${article._id}`}></div>
            <div key={article._id} className="col-6 mb-4">
              <Article
                key={`article-${article._id}`}
                url={article.url}
                title={article.title}
                image={article.top_image}
                summary={article.summary}
                readTime={article.read_time_in_minutes}
                publishDate={article.publish_date}
                authors={article.authors}
              />
            </div>
            <div className="col-3" key={`spacer-right-${article._id}`}></div>
          </>
        ))}
      </div>
    </div>
  );
}

export default ArticleList;
