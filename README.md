# Website Article Aggregator App

## Introduction

This project facilitates the discovery and aggregation of RSS feeds from diverse websites and makes them searchable. It has a simple(incomplete) front end web ui with a fairly robust backend. The backend crawler, when given a set of seed urls, finds feeds from it and extracts all links to be given back to the crawler inorder continue the process infinitely.

![Web UI.](/assets/img/web_ui_with_results.png)


## Installation

This app can easily be installed using docker-compose command. Make sure docker is installed on your system before installing the app, you can view instructions [here](https://docs.docker.com/engine/install/).
To install go to the root directory where docker-compose.yml is present and do the following.
```bash
docker compose up --build
```
This would build and start 5 containers. **web** service is the gui container which is a simple react app that talks with backend to fetch articles according to user's query. **article_service** provides apis relating to artcles and domains. **crawler_service** takes care of crawling websites, finding rss feeds and retrieving feed details. **summarizer_service** uses NLP libraries to find relevant keywords in an article. **tasks_service** is responsible for managing long running tasks by adding it to redis queue.

You can run just **web** and **article_service** if articles are already populated. To do it type in the following command.
```bash
docker compose up --build web article_service
```

## Usage
Following command will start neccessary services for accessing web ui for the app. 
```bash
docker compose up web article_service
```
![Command to start web ui.](/assets/img/compose_up_for_web.png)

You can access the web ui by visiting [http://localhost:3000](localhost:3000). 
![Web UI.](/assets/img/web_ui_without_results.png)

<!-- To crawl websites, fire up all services and use API endpoint provided in the postman collection -->


The above command will fire up all containers required for running the frontend of the app. Namely, **article_service**, **web**, **article_db** containers. 

Now to find feeds and crawl them, 4 services are required. **article_service**, **crawler_service**, **task_service**, **summarizer_service** will take care of all crawling and saving to database tasks. You can edit the above command with name of containers based on the task you need to do.



## Architecture

### Frontend
![Architecture for just the frontend and the article_service.](/assets/img/frontend.webp)

Upon receiving a user's keyword input, the web service communicates with the article_service to identify all articles containing the specified keyword. The article_service then selects relevant articles and organizes them based on factors such as website popularity, article read time, categories, and keyword rank. The web service subsequently presents the ranked articles to the user. You can view the pipeline code in this [file](/article_service/articles/views/article.py).


### Backend
![Architecture for backend services.](/assets/img/full.webp)

Here, initially a set of seed URLs are given to the crawler_service. Using libraries like Beautiful Soup, crawler service crawls the urls provided and finds rss feeds in them. Along with the feeds, all links are parsed and are given to task_service to further process them to find rss feeds in them. 
These feeds are then parsed to get articles. The articles received are then sent to summarizer service to determine it's quality and find keywords in the article. Then articles along with the keywords are added to a queue to be saved later. The task_service obtains the articles from the queue and sends it to article_service to be saved. 
