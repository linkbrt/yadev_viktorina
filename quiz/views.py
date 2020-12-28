from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Question, Quiz, QuizState


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
        'progress': int(state.question_index / questions.count() * 100),
    }

    """ Check answers """
    if request.method == 'POST' and state.passed:
        question = get_object_or_404(Question, pk=state.question_index)
        user_answers = []
        correct_answers = []
        result = None
        answers = question.answers
        if question.type == 'choise':
            answers = answers.all()
            for key, value in request.POST.items():
                if 'answer-' in key and value == 'on':
                    user_answers.append(answers[int(key[7:])-1])
            for answer in answers:
                if answer.is_correct:
                    correct_answers.append(answer)
            result = user_answers == correct_answers
            correct_answers = [answer.content for answer in correct_answers]
            user_answers = [answer.content for answer in user_answers]
        else:
            user_input = request.POST.get('user_input')
            answer = answers.first()
            result = answer.content == user_input
            correct_answers = [answer.content]
            user_answers = [user_input]

        context['question'] = question
        context['result'] = result
        context['correct_answers'] = (', '.join(correct_answers)
                                      if correct_answers else '')
        context['user_answers'] = (', '.join(user_answers)
                                   if user_answers else '')
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
    """ Success page """
    state = request.session.get('state')
    quiz = get_object_or_404(Quiz, slug=slug)
    if not state:
        return HttpResponse(status=406)
    if quiz.pk == state['quiz_pk']:
        del request.session['state']

    if quiz.success_page != '':
        return HttpResponse(quiz.success_page)
    return render(request, 'quiz_end.html', {})
