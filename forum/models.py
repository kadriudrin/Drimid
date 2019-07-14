from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    total_votes = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    total_votes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    total_votes = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)


class PostUpVotes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.post.up_votes += 1
            self.post.total_votes += 1
            self.post.save()
        super(PostUpVotes, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.up_votes -= 1
        self.post.total_votes -= 1
        self.post.save()
        super(PostUpVotes, self).delete(*args, **kwargs)

class PostDownVotes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.post.total_votes -= 1
            self.post.save()
        super(PostDownVotes, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.total_votes += 1
        self.post.save()
        super(PostDownVotes, self).delete(*args, **kwargs)


