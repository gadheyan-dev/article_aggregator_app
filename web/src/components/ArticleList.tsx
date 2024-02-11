// ArticleList.tsx
import React, { useState } from 'react';
import axios from 'axios';
import Article from './Article';


interface ArticleListProps {
  // Add any props if needed
}

interface Author {
  name: string;
}


interface ArticleData {
  _id: string;
  url: string;
  domain: string;
  title: string;
  top_image: string;
  summary: string;
  read_time_in_minutes: number;
  publish_date: string;
  authors: Author[];
}

function ArticleList({}: ArticleListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [articles, setArticles] = useState<ArticleData[]>([]);
  const [loading, setLoading] = useState(false);
  const apiUrl = process.env.REACT_APP_ARTICLE_API_URL || 'http://localhost:8002/articles'; // Replace with your actual environment variable name


  const fetchArticles = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiUrl}/articles/?search=${searchTerm}`);
      setArticles(response.data.data);
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
          className="form-control form-control-sm"
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
          <React.Fragment key={article._id}>
            <div className="col-3" key={`spacer-left-${article._id}`}></div>
            <div className="col-6 mb-4">
              <Article
                key={`article-${article._id}`}
                url={article.url}
                domain={article.domain}
                title={article.title}
                image={article.top_image}
                summary={article.summary}
                readTime={article.read_time_in_minutes}
                publishDate={article.publish_date}
                authors={article.authors}
              />
            </div>
            <div className="col-3" key={`spacer-right-${article._id}`}></div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export default ArticleList;
