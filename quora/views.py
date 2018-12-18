import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from quora.decorators import myuser_login_required
from quora.random_string_generator import random_string_generator_c
from .forms import SignupForm, LoginForm, QuestionForm, AnswerForm
from .models import User, Question, Answers, Upvotes

# Create your views here.


def index(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect(reverse('quora:home'))
    else:

        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = User()
                user.fname = form.cleaned_data['fname'].strip()
                user.lname = form.cleaned_data['lname'].strip()
                user.email = form.cleaned_data['email'].strip()
                uspw = form.cleaned_data['password'].strip()
                ranstr = random_string_generator_c()
                userpasw = ranstr.hash_password(uspw)
                user.password = userpasw
                user.save()
                return HttpResponseRedirect(reverse('quora:login'))
                # return render(request, 'quora/base.html', {'user': user})
            else:
                return render(request, 'quora/register.html', {'form': form})
        else:
            form = SignupForm()
        return render(request, 'quora/register.html', {'form': form})


def login(request):

    if 'user_id' in request.session:
        return HttpResponseRedirect(reverse('quora:home'))
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST['username'])
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('quora:home'))
    else:
        form = LoginForm()
    return render(request, 'quora/login.html', {'form': form})


@myuser_login_required
def logout(request):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('quora:home'))


@myuser_login_required
def addquestion(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_ip = form.cleaned_data['question'].strip()
            question_text = " ".join(question_ip.split())
            print(question_text)
            userid = request.session['user_id']
            user = User.objects.get(pk=userid)
            question = Question(question=question_text, user=user)
            question.save()
            return HttpResponseRedirect(reverse('quora:home'))
    else:
        form = QuestionForm()
    return render(request, 'quora/question.html', {'form': form})


@myuser_login_required
def addanswer(request):

    questions = Question.objects.order_by('-date')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_ip = form.cleaned_data['answer'].strip()
            ques_id = request.POST.get('xyz')
            question = Question.objects.get(pk=ques_id)
            answer_text = " ".join(answer_ip.split())
            userid = request.session['user_id']
            user = User.objects.get(pk=userid)
            answer = Answers(answer=answer_text, question_id=question,
                             user_id=user)
            answer.save()
            return HttpResponseRedirect(reverse('quora:home'))
    else:
        form = AnswerForm()
    args = {
        'questions': questions,
        'form': form
    }
    return render(request, 'quora/questionList.html', args)


def home(request):
    questions = Question.objects.order_by('-date')
    return render(request, 'quora/dashboard.html', {'questions': questions})


def all_questions(request):
    questions = Question.objects.order_by('-date')
    args= {
        'all_que': True,
        'questions': questions
    }
    return render(request, 'quora/dashboard.html', args)


def all_answers(request, qid):

    question = Question.objects.get(pk=qid)
    answer_list = question.answers_set.all()
    args = {
            'answer_list': answer_list,
            'question': question
        }
    return render(request, 'quora/allanswers.html', args)


@myuser_login_required
def individual_questions(request):
    userid = request.session['user_id']
    user = User.objects.get(pk=userid)
    questions = Question.objects.filter(user=user)
    args = {
            'questions': questions,
         }
    # print(questions)
    return render(request, 'quora/individual_ques.html', args)


@myuser_login_required
def individual_answers(request):
    userid = request.session['user_id']
    user = User.objects.get(pk=userid)
    answers = Answers.objects.filter(user_id=user)
    args = {
            'answers': answers,
         }
        # print(questions)
    return render(request, 'quora/individual_ans.html', args)


def ans_upvotes(request):
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        ansid = request.GET.get('ansid', None)
        answer = Answers.objects.get(pk=ansid)
        is_voted = Upvotes.objects.filter(upvoted_user=user,
                                          upvoted_answer=answer).exists()
        if is_voted is False:
            answer.answer_upvotes += 1
            answer.save()
            send_upvotes = answer.answer_upvotes
            question = Question.objects.get(pk=answer.question_id.id)
            # print(question)
            question.total_upvotes += 1
            question.save()
            now = datetime.datetime.now()
            upvotes = Upvotes(upvoted_user=user, upvoted_answer=answer, vote_date=now)
            upvotes.save()
        data = {
                'is_voted': is_voted,
                }
        if data['is_voted']:
            data['error_message'] = 'You have already upvoted this answer!'
        else:
            data['upvotes'] = send_upvotes
    else:
        data = {
            'not_loggedin': True,
            'notify':  'You have to log in to upvote any answer!'
        }
    # print(data)
    return JsonResponse(data)


@myuser_login_required
def individual_upvoted(request):
    userid = request.session['user_id']
    user = User.objects.get(pk=userid)
    upvotes = Upvotes.objects.filter(upvoted_user=user)
    args = {
            'upvotes': upvotes,
            'individual': True,
         }
    # print(questions)
    return render(request, 'quora/individual_ans.html', args)


def past_hour_highest_votes(request):

    past_one_hour = True
    now = datetime.datetime.now()
    then = now-datetime.timedelta(hours=1)
    votes = Upvotes.objects.filter(vote_date__range=[then, now])
    dict_ans = {}
    for vote in votes:
        if vote.upvoted_answer.question_id in dict_ans:
            dict_ans[vote.upvoted_answer.question_id] += 1
        else:
            dict_ans[vote.upvoted_answer.question_id] = 1
    max = 0
    qun_id = None
    # print(votes)
    for i in dict_ans:
        if dict_ans[i] > max:
            max = dict_ans[i]
            qun_id = i

    args= {
        'qun_id': qun_id,
        'past_one_hour': past_one_hour
    }
    return render(request, 'quora/highest_upvotes.html', args)


def highest_upvoted_question(request):
    questions = Question.objects.all()
    max_votes = 0
    qun_id = None
    for qun in questions:
        if qun.total_upvotes > max_votes:
            max_votes = qun.total_upvotes
            qun_id = qun
    args = {
        'qun_id': qun_id,
    }
    return render(request, 'quora/highest_upvotes.html', args)


def past_hour_highest_votes_answer(request):
    past_one_hour = True
    now = datetime.datetime.now()
    then = now - datetime.timedelta(hours=1)
    votes = Upvotes.objects.filter(vote_date__range=[then, now])
    dict_ans = {}
    for vote in votes:
        if vote.upvoted_answer in dict_ans:
            dict_ans[vote.upvoted_answer]+=1
        else:
            dict_ans[vote.upvoted_answer] = 1
    ans_id = None
    max = 0
    for i in dict_ans:
        if dict_ans[i] > max:
            max = dict_ans[i]
            ans_id = i

    args = {
        'ans_id': ans_id,
        'past_one_hour': past_one_hour
    }
    return render(request, 'quora/highest_upvotes_answer.html', args)


def highest_upvoted_answer(request):
    answers = Answers.objects.all()
    max_votes = 0
    ans_id = None
    for qun in answers:
        if qun.answer_upvotes > max_votes:
            max_votes = qun.answer_upvotes
            ans_id = qun
    args = {
        'ans_id': ans_id,
    }
    return render(request, 'quora/highest_upvotes_answer.html', args)


def see_all_upvoters(request):
    ansid = request.GET.get('ansid', None)
    answer = Answers.objects.get(pk=ansid)
    upvotes = Upvotes.objects.filter(upvoted_answer=answer)
    upvoters = []
    for i in upvotes:
        upvoters.append(i.upvoted_user.fname + " " + i.upvoted_user.lname)
    data = {
        'upvoters': upvoters
    }
    return JsonResponse(data)


def handler404(request):
    return render(request, 'quora/error_404.html', status=404)


def handler500(request):
    return render(request, 'quora/error_500.html', status=500)
