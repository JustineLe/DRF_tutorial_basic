from django.db import models


# Create your models here.
class Journalist(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Article(models.Model):
    # author = models.CharField(max_length=100)
    author = models.ForeignKey(Journalist, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    main_text = models.TextField()
    published_time = models.DateField()
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
