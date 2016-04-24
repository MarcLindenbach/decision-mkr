from django.db import models


class Tree(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    root_node = models.OneToOneField('Node', null=True)


class Node(models.Model):
    parent = models.ForeignKey('self', null=True)
    predicate = models.CharField(max_length=200, blank=True)
    criteria = models.CharField(max_length=200)
