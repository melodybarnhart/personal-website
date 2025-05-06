from django.contrib import admin
from .models import Project, Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer_text')
    search_fields = ('question_text',)

admin.site.register(Project)
admin.site.register(Question)