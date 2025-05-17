from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator


QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question # {i}',
        'img_path': "/img/hello-3.jpeg"
    } for i in range(30)
]

ANSWERS = [
    {
        'id': i,
        'text': f'This is text for answer',
        'img_path': "/img/hello-3.jpeg"
    } for i in range(30)
]

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'questions': page.object_list, 'page': page})

def hot(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, template_name='hot.html', context={'questions': page.object_list, 'page': page})

def question(request, question_id):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(ANSWERS, 5)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    try:
        question = ANSWERS[question_id]  
    except IndexError:
       raise Http404("Question not found")
    return render(request, 'single_question.html', {'question': question, 'answers': page.object_list, 'page': page})

def new_question(request):
        return render(request, 'new_question.html')

def login(request):
        return render(request, 'login.html')

def signup(request):
        return render(request, 'signup.html')

def settings(request):
        return render(request, 'settings.html')