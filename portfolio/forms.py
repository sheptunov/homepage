# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from portfolio.models import Message

class FeedbackForm(ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'email', 'message']