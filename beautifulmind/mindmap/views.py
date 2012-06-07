# -*- coding: utf-8 -*-
from django.db.models.expressions import F
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.utils import simplejson
from .models import MindMap, MindMapComponent
from .forms import MindMapForm, MindMapComponentForm


def map_show(request, mindmap_slug):
    mindmap = get_object_or_404(MindMap, slug=mindmap_slug)
    return render_to_response('mindmap/mindmap.html',
            {
                'mindmap': mindmap
            },
            context_instance=RequestContext(request))


def map_new(request):
    if request.method == 'POST':
        form = MindMapForm(data=request.POST)
        if form.is_valid():
            root_component = form.save().root_component
            root_component.pos_left = form.cleaned_data['root_component_pos_left']
            root_component.pos_top = form.cleaned_data['root_component_pos_top']
            root_component.save()
    else:
        form = MindMapForm()

    return render_to_response('mindmap/map_new.html',
            { 'form': form },
            context_instance=RequestContext(request))


def map_components(request, mindmap_pk):
    mindmap = get_object_or_404(MindMap, pk=mindmap_pk)
    components = mindmap.root_component.get_descendants(include_self=True)
    return HttpResponse(simplejson.dumps(
        serializers.serialize('json', components or [], fields=('pk','title', 'pos_top', 'pos_left', 'level', 'parent'))
    ), 'application/json')

def map_component_update_pos(request, mindmap_pk, component_pk):
    component = get_object_or_404(MindMapComponent, pk=component_pk)

    response_data = {'success' : False}
    if request.method == 'POST' and ('pos_left' and 'pos_top' in request.POST):
        component.pos_left = request.POST['pos_left']
        component.pos_top = request.POST['pos_top']
        component.save()
        response_data = {'success' : True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_components_add_offset(request, mindmap_pk):
    mindmap = get_object_or_404(MindMap, pk=mindmap_pk)
    response_data = {'success' : False}

    if request.method == 'POST' and ('offset_left' and 'offset_top' and 'component_exclude_pk' in request.POST):
        mindmap.root_component.get_descendants(include_self=True).exclude(pk=request.POST['component_exclude_pk']).update(
            pos_left = F('pos_left') + int(request.POST['offset_left']),
            pos_top = F('pos_top') + int(request.POST['offset_top'])
        )
        response_data = {'success' : True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_component_update_title(request, mindmap_pk, component_pk):
    component = get_object_or_404(MindMapComponent, pk=component_pk)

    response_data = {'success' : False}
    if request.method == 'POST' and 'title' in request.POST:
        component.title = request.POST['title']
        component.save()
        response_data = {'success' : True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')