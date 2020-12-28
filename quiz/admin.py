"""Application 'quiz' admin page configuration."""
from django.contrib import admin

from .models import Answer, Question, Quiz


class AnswersInLine(admin.StackedInline):
    model = Answer
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Manage quizes."""

    list_display = ('pk', 'title', 'slug', 'description', 'success_page')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Manage questions."""

    list_display = ('pk', 'content', 'type', 'image')
    inlines = [AnswersInLine]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Manage answers."""

    list_display = ('pk', 'content')
