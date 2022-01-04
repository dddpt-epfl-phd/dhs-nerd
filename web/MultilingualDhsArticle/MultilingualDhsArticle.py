


class MultiLingualDhsArticle:
    def __init__(self, articles_by_lng):
        self.articles = dict()
        for lng, a in articles_by_lng.items():
            self.articles[lng] = a
