from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
    page = paginate(request, QUESTIONS, per_page=5)
    return render(request, template_name='index.html', context={'questions': page.object_list, 'page': page})

def hot(request):
    page = paginate(request, QUESTIONS, per_page=5)
    return render(request, template_name='hot.html', context={'questions': page.object_list, 'page': page})

def question(request, question_id):
    page = paginate(request, ANSWERS, per_page=5)

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

def paginate(request, items_list, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page