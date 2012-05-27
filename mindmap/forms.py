# -*- coding: utf-8 -*-
from django import forms
from .models import MindMap


class MindMapForm(forms.ModelForm):
    class Meta:
        model = MindMap
        fields = ('name',)
