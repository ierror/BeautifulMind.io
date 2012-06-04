# -*- coding: utf-8 -*-
from django.forms.forms import BaseForm
from django.http import HttpResponse
from django.utils import simplejson as json


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        for field, value in context.items():

            # collect special form elemenst
            if isinstance(value, BaseForm):
                instance_pk = None
                if context[field].instance:
                    instance_pk = context[field].instance.pk

                context[field] = {
                    'is_bound': value.is_bound,
                    'is_valid': value.is_valid(),
                    'data': value.data,
                    'instance_pk': instance_pk,
                    'errors': value.errors
                }

        return json.dumps(context)