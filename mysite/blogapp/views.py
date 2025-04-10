from django.contrib.syndication.views import Feed
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Article


class ArticleListView(ListView):
    # template_name = "blogapp/article_list.html"
    # context_object_name = "articles"
    queryset = Article.objects.filter(pub_date__isnull=False).order_by(
        "-pub_date"
    )


class ArticleDetailView(DetailView):
    model = Article


class LatestArticleFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes on addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return Article.objects.filter(pub_date__isnull=False).order_by(
            "-pub_date"
        )[:5]

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]
