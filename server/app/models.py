from django.db import models


class DecisionTree(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    initial_node = models.OneToOneField('DecisionNode',
                                        on_delete=models.CASCADE,
                                        null=True)


class DecisionNode(models.Model):
    text = models.CharField(max_length=200)
    yes_node = models.OneToOneField('DecisionNode',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='+')
    no_node = models.OneToOneField('DecisionNode',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   related_name='+')
