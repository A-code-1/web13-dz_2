from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login 
from .forms import SignupForm, LoginForm
from .models import Question, Answer, Tag, Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            profile = user.profile
            profile.nickname = form.cleaned_data.get("nickname")
            profile.avatar = form.cleaned_data.get("avatar")
            profile.save()

            login(request, user) 
            return redirect('/')  
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

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

def index(request):
    questions = Question.objects.order_by('-created_at')
    page = paginate(request, questions, per_page=5)
    return render(request, 'index.html', {'questions': page.object_list, 'page': page})

def hot(request):
    questions = Question.objects.order_by('-likes_count')  # Или метод .hot_questions()
    page = paginate(request, questions, per_page=5)
    return render(request, 'hot.html', {'questions': page.object_list, 'page': page})

def question(request, question_id):
    question_obj = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question_obj).order_by('-created_at')
    page = paginate(request, answers, per_page=5)
    return render(request, 'single_question.html', {
        'question': question_obj,
        'answers': page.object_list,
        'page': page
    })

def new_question(request):
    return render(request, 'new_question.html')

def login1(request):
    return render(request, 'login1.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')

def questions_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.questions_by_tag(tag_name).order_by('-created_at')
    page = paginate(request, questions)
    return render(request, 'tag_questions.html', {
        'questions': page.object_list,
        'page': page,
        'tag': tag,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('/')  
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()

    return render(request, 'login1.html', {'form': form})
 
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')  
