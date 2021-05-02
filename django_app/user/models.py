from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class CreateManager(models.Manager):
    def create(self, **kwargs):
        for key in kwargs:
            kwargs.update({key:kwargs.get(key)[0]})
        if 'password' in kwargs:
            password = kwargs.pop('password')
        obj = self.model(**kwargs)
        self._for_write = True
        obj.set_password(password)
        obj.save(force_insert=True, using=self.db)
        return obj


class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    objects = CreateManager()

    username = models.CharField(max_length=200, unique=True)
    profile_image = models.ImageField(upload_to='', )
    name = models.CharField(max_length=200)
    description = models.TextField()
    liked_posts = models.ManyToManyField('post.Post', related_name='liked_users')
    following = models.ManyToManyField('User', related_name='follower')

    def __str__(self):
        return self.name