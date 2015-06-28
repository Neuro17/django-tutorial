from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Question
from .models import Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    # number of choices for each question
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question_text']
    # search function
    search_fields = ['question_text']
    date_hierarchy = 'pub_date'

admin.site.register(Question, QuestionAdmin)
