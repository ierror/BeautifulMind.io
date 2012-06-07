# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from .forms import MindMapComponentForm
from .models import MindMap
from utils.class_based_views_helper import JSONResponseMixin


class MapComponentAddView(CreateView, JSONResponseMixin):
    form_class = MindMapComponentForm
    template_name = 'mindmap/map_component_add.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(MapComponentAddView, self).get_form_kwargs(**kwargs)
        kwargs['mindmap'] = get_object_or_404(MindMap, pk=self.kwargs['mindmap_pk'])
        return kwargs

    def get_form(self, form_class):
        form = super(MapComponentAddView, self).get_form(form_class)
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        form.save()
        context_data = super(MapComponentAddView, self).get_context_data()
        context_data.update({'form': form})
        return self.render_to_response(context_data)

    def render_to_response(self, context):
        if self.kwargs.get('type') == 'json':
            return JSONResponseMixin.render_to_response(self, context)

        return super(MapComponentAddView, self).render_to_response(context)



