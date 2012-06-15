# -*- coding: utf-8 -*-
import os
from tempfile import NamedTemporaryFile
from subprocess import call
from django.conf import settings
from django.db.models.expressions import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from .models import MindMap, MindMapComponent
from .forms import MindMapForm, MindMapExportForm


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
            {'form': form},
        context_instance=RequestContext(request))


def map_components(request, mindmap_pk):
    mindmap = get_object_or_404(MindMap, pk=mindmap_pk)
    components = mindmap.root_component.get_descendants(include_self=True)
    return HttpResponse(simplejson.dumps(
        serializers.serialize('json', components or [],
            fields=('pk', 'title', 'pos_top', 'pos_left', 'level', 'parent'))
    ), 'application/json')


def map_component_update_pos(request, mindmap_pk, component_pk):
    component = get_object_or_404(MindMapComponent, pk=component_pk)

    response_data = {'success': False}
    if request.method == 'POST' and ('pos_left' and 'pos_top' in request.POST):
        component.pos_left = request.POST['pos_left']
        component.pos_top = request.POST['pos_top']
        component.save()
        response_data = {'success': True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_components_add_offset(request, mindmap_pk):
    mindmap = get_object_or_404(MindMap, pk=mindmap_pk)
    response_data = {'success': False}

    if request.method == 'POST' and ('offset_left' and 'offset_top' and 'component_exclude_pk' in request.POST):
        mindmap.root_component.get_descendants(include_self=True).exclude(
            pk=request.POST['component_exclude_pk']).update(
            pos_left=F('pos_left') + int(request.POST['offset_left']),
            pos_top=F('pos_top') + int(request.POST['offset_top'])
        )
        response_data = {'success': True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_component_update_title(request, mindmap_pk, component_pk):
    component = get_object_or_404(MindMapComponent, pk=component_pk)

    response_data = {'success': False}
    if request.method == 'POST' and 'title' in request.POST:
        component.title = request.POST['title']
        component.save()
        response_data = {'success': True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_component_delete(request, mindmap_pk, component_pk):
    component = get_object_or_404(MindMapComponent, pk=component_pk)

    response_data = {'success': False}
    if request.method == 'POST':
        # don't delete root component
        if component.level == 0:
            component.get_descendants().delete()
        else:
            component.delete()
        response_data = {'success': True}

    return HttpResponse(simplejson.dumps(response_data), 'application/json')


def map_export_form(request, mindmap_pk):
    from datetime import datetime
    from .settings import EXPORTS_SAVE_PATH
    from pyxvfb.command import XvfbRun
    from django.core.files.base import ContentFile

    mindmap = get_object_or_404(MindMap, pk=mindmap_pk)
    global_form_errors = []
    export_file = None

    if request.method == 'POST' and ('export_format' in request.POST):
        form = MindMapExportForm(data=request.POST)
        if form.is_valid():
            # export image as png
            export_format = form.cleaned_data['export_format']
            if export_format == 'image':
                export_format = 'png'

            tmpfile = NamedTemporaryFile(suffix='.%s' % (export_format))

            phantomjs_command = 'phantomjs %s/bin/export.js %s %s' % (
                os.path.dirname(__file__),
                request.build_absolute_uri(reverse('mindmap_map_export', args=[mindmap_pk])),
                tmpfile.name
            )

            # on production systems there is no xserver installed (i hope so ^^) => use xvfb
            if not settings.ENVIRONMENT.IS_FOR_DEVELOPMENT:
                exit_code = XvfbRun().run_xcommand_and_wait(phantomjs_command)['exit_code']
            else:
                exit_code = call(phantomjs_command, shell=True)

            if exit_code:
                global_form_errors.append(_('Unable to generate %s' % (export_format)))
            else:
                export_file = default_storage.save('%s%s-%s.%s' % (
                    EXPORTS_SAVE_PATH,
                    datetime.now().strftime("%Y-%m-%d_%H%M%S"),
                    mindmap.slug, export_format),
                    ContentFile(tmpfile.file.read())
                )
    else:
        form = MindMapExportForm()

    return render_to_response('mindmap/export_form.html',
            {
                'mindmap': mindmap,
                'components': map_components(request, mindmap_pk).content,
                'form': form,
                'export_file': export_file,
                'global_form_errors': global_form_errors
            },
        context_instance=RequestContext(request))


def map_export(request, mindmap_pk):
    get_object_or_404(MindMap, pk=mindmap_pk)
    return render_to_response('mindmap/export.html',
            {'components': map_components(request, mindmap_pk).content},
        context_instance=RequestContext(request))


def map_export_download(request, mindmap_pk):
    get_object_or_404(MindMap, pk=mindmap_pk)
    file_to_download = request.GET.get('file', None)

    if not file or not default_storage.exists(file_to_download):
        raise Http404

    return HttpResponseRedirect('%s%s' % (settings.MEDIA_URL, file_to_download))