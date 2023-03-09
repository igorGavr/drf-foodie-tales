from django.db import models


class BlogManager(models.Manager):

    def last_blogs(self, count):
        # фільтруємо queryset
        return self.all()[0:count]