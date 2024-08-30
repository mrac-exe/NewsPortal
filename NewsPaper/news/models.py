from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating  = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum("rating"), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum("rating"), 0))['cr']
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum("rating"),0))['pcr']


        print(posts_rating)
        print('___________')
        print(comments_rating)
        print('____________')
        print(post_comments_rating)



        self.rating = posts_rating * 3 + comments_rating + posts_rating
        self.save()


class Category(models.Model):
    name = models.CharField(unique = True,max_length = 50)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return f'{self.name}'






class Post(models.Model):
    articles = "AR"
    news = "NW"

    POST_TYPES = [
        (news, "Новость"),
        (articles, "Статья"),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES,default=news)
    date_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    post_likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    post_dislikes = models.ManyToManyField(User, blank=True, related_name="post_dislikes")


    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        small_text = self.text[0:124] + '...'
        return small_text

    # def __str__(self):
    #     return f'{self.title.title()} {self.date_time} : {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# class CategorySubs(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_post = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


