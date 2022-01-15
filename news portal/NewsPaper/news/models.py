from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user_relation = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user_relation.username}'


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat +=postRat.get('postRating')

        commentRat = self.user_relation.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Нвовсть'),
        (ARTICLE, 'Статья')
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    time_creation = models.DateTimeField(auto_now_add=True) # автоматичиски запоминает время создания
    title = models.CharField(max_length=256, verbose_name= 'заглавие') #обезательный аргумент в CharField (обозначает макс количество символов, имя в админке
    text = models.TextField(blank=True, editable=True) #blank - позволяет оставить поле пустым, editable - в дефолте True если False запрещает изменять значение в админке
    rating = models.SmallIntegerField(default=0)
    author_relation = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category_relation = models.ManyToManyField(Category, through='PostCategory')


    class Meta: # Класс дозволяє в адмінці прописати назви моделей в однині і в множині
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self): # функція виводить замість model.object(1) назву обєкта
        return self.title

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_relation = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    timeCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    post_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_relation = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


# Команды в консоль:

# py manage.py makemigrations
# py manage.py migrate
# py manage.py shell
#
# from news.models import *
# u1 = User.objects.create_user(username = 'Vlad')
# u2 = User.objects.create_user(username = 'Masha')
# Author.objects.create(user_relation = u1)
# Author.objects.create(user_relation = u2)
# Category.objects.create(name='IT')
# Category.objects.create(name='photo')
# Category.objects.create(name='politics')
# Category.objects.create(name='technology')
#
# author = Author.objects.get(id=1)
# Post.objects.create(author_relation=author, category_type='AR', title = 'sometitle about IT', text = 'somebigtext about IT')
# Post.objects.create(author_relation=author, category_type='AR', title = 'sometitle about photo', text = 'somebigtext about photo')
# Post.objects.create(author_relation=author, category_type='NW', title = 'sometitle about politics', text = 'somebigtext about politics')
#
# Post.objects.get(id=2).post_category_relation.add(Category.objects.get(id=1))
# Post.objects.get(id=2).post_category_relation.add(Category.objects.get(id=2))
# Post.objects.get(id=1).post_category_relation.add(Category.objects.get(id=1))
# Post.objects.get(id=3).post_category_relation.add(Category.objects.get(id=1))
#
# Comment.objects.create(post_relation=Post.objects.get(id=1), user_relation = Author.objects.get(id=1).user_relation, text = 'somecommenttext')
# Comment.objects.create(post_relation=Post.objects.get(id=2), user_relation = Author.objects.get(id=1).user_relation, text = 'somecommenttext')
# Comment.objects.create(post_relation=Post.objects.get(id=3), user_relation = Author.objects.get(id=2).user_relation, text = 'somecommenttext')
# Comment.objects.create(post_relation=Post.objects.get(id=1), user_relation = Author.objects.get(id=2).user_relation, text = 'best comment text')
#
# Comment.objects.get(id=1).like()
# Comment.objects.get(id=2).like()
# Comment.objects.get(id=3).dislike()
# Comment.objects.get(id=2).like()
#
# a = Author.objects.get(id=1)
# a.update_rating()
# a.ratingAuthor
#
# best = Author.objects.all().order_by('-ratingAuthor').values('user_relation', 'ratingAuthor')
# best
# best_post = Post.objects.all().order_by('-rating').values('time_creation', 'rating', 'title', 'author_relation')[0]
# preview_best_post = Post.objects.get(id=1).preview()
# print(f'{best_post}, {preview_best_post}')
#
# post.comment_set.all().values('timeCreation', 'user_relation', 'rating', 'text')