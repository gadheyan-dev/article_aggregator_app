
class Article:
    title = ""
    url = ""
    top_image = ""
    authors = []
    summary = ""
    publish_date = ""
    description = ""

    def __init__(self, title = "", url = "", top_image = "", summary = "", description = "", publish_date = None, authors = []) -> None:
        self.title = title
        self.url = url
        self.top_image = top_image
        self.summary = summary
        self.description = description
        self.publish_date = publish_date
        self.authors = authors

class Author:
    name = ""
    avatar = ""
    email = ""
    def __init__(self, name, avatar = "", email = "") -> None:
        self.name = name
        self.avatar = avatar
        self.email = email
