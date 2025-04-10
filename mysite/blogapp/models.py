from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    bio = models.TextField(blank=True, null=False)


class Category(models.Model):
    name = models.CharField(max_length=40, null=False)


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False)


class Article(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(blank=True, null=False)
    pub_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tags")

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk": self.pk})
