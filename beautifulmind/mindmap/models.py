# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from utils.slughifi import slughifi
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class MindMapComponent(MPTTModel):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    pos_top = models.IntegerField(blank=True, null=True)
    pos_left = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % self.title


class MindMap(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255, blank=False)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=300, blank=False)
    root_component = models.ForeignKey(MindMapComponent, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('mindmap.views.map_show', [self.slug])

    def save(self, *args, **kwargs):
        # create
        if not self.pk:
            # add root component
            root_component = MindMapComponent(
                title = self.name,
            )
            root_component.save()
            self.root_component = root_component

            # slugify
            super(MindMap, self).save(*args, **kwargs)
            self.slug = '%d-%s' % (self.pk, slughifi(self.name))

            super(MindMap, self).save(*args, **kwargs)

        # modify
        else:
            super(MindMap, self).save(*args, **kwargs)