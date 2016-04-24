from django.db import models


class DecisionTree(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    root_node = models.OneToOneField('Node',
                                     on_delete=models.CASCADE,
                                     null=True)


class Node(models.Model):
    predicate = models.CharField(max_length=200, blank=True)
    criteria = models.CharField(max_length=200)
    children = models.ManyToManyField('Node')
