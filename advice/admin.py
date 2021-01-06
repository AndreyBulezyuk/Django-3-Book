from django.contrib import admin
from .models import Question, Advice

admin.site.register(Question)
admin.site.register(Advice)