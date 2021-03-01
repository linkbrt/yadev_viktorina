from os import stat
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Answer, Question, Quiz, QuizState


def index(request):
    """Main page with all quizs"""
    context = {}
    state = request.session.get('state')
    quiz_list = Quiz.objects.all()
    if state:
        context['state'] = state
        context['last_quiz'] = Quiz.objects.get(pk=state['quiz_pk'])
        quiz_list = quiz_list.exclude(pk=state['quiz_pk'])
    paginator = Paginator(quiz_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['quiz_list'] = quiz_list
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'index.html', context)


def play(request, slug):
    """
    Main part of service
    1) Render quiz
    2) Check answers
    3) On end redirect (url in html) to success page
    """

    """ Check for errors and if success render quiz """
    quiz = get_object_or_404(Quiz, slug=slug)
    state = request.session.get('state')

    if state and quiz.pk != state['quiz_pk']:
        return HttpResponse(status=404)

    if not quiz.questions.count():
        return render(request, 'quiz.html', {'quiz': quiz})

    if state:
        state = QuizState(**state)
    else:
        state = QuizState(quiz.pk, max_index=quiz.questions.count())

    questions = quiz.questions.all()
    context = {
        'quiz': quiz,
        'question_index': state.question_index,
        'progress': int(state.question_index / state.max_index * 100),
    }

    """ Check answers """
    if request.method == 'POST' and state.passed is True:
        question = get_object_or_404(Question, pk=state.question_index)
        answers = question.answers
        correct_answers = []
        state.user_answers = []
        for answer in answers.all():
                if answer.is_correct:
                    correct_answers.append(answer.content)
        if question.type == 'choise':
            for key, value in request.POST.items():
                if value == 'on':
                    state.user_answers.append(Answer.objects.get(pk=int(key)).content)
        else:
            user_input = request.POST.get('user_input')
            answer = answers.first()
            state.user_answers.append(user_input)

        state.result = state.user_answers == correct_answers
        context['question'] = question
        context['result'] = state.result
        context['correct_answers'] = (', '.join(correct_answers)
                                      if correct_answers else '')
        context['user_answers'] = (', '.join(state.user_answers)
                                   if state.user_answers else '')
        state.next()
        request.session['state'] = state.to_dict()
        return render(request, 'quiz.html', context)


    """ Redirect to next question """
    question = questions[state.question_index-1]
    answers = question.answers
    context['question'] = question
    if answers.count() > 1:
        context['answers'] = answers.all()
    state.step()
    request.session['state'] = state.to_dict()

    return render(request, 'quiz.html', context)


def success_page(request, slug):
    """ Render success page """
    state = request.session.get('state')
    quiz = get_object_or_404(Quiz, slug=slug)
    if not state:
        return HttpResponse(status=406)
    state = QuizState(**state)
    if quiz.pk == state.quiz_pk:
        del request.session['state']

    if quiz.success_page != '':
        return HttpResponse(quiz.success_page)
    return render(request, 'quiz_end.html', {})
