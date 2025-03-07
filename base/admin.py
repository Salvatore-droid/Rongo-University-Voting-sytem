from django.contrib import admin
from .models import *

# from django.template.response import TemplateResponse
from django.urls import path


admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Vote)
admin.site.register(School)
