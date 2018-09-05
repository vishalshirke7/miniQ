from django.urls import path

from . import views

app_name = 'quora'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('all_questions/', views.all_questions, name='all_questions'),
    path('ask_a_question/', views.addquestion, name='add'),
    path('all_question/', views.individual_questions, name='individual_questions'),
    path('all_answers/', views.individual_answers, name='individual_answers'),
    path('all_upvoted_answers/', views.individual_upvoted, name='individual_upvoted'),
    path('question_answered/', views.addanswer, name='addanswer'),
    path('all_answers/<int:qid>', views.all_answers, name='all_answers'),
    path('highest_upvoted_question/', views.past_hour_highest_votes, name='past_hour_highest_votes'),
    path('highest_upvoted_question_ever/', views.highest_upvoted_question, name='highest_upvoted_question'),
    path('highest_upvoted_answer/', views.past_hour_highest_votes_answer, name='past_hour_highest_votes_answer'),
    path('highest_upvoted_answer_ever/', views.highest_upvoted_answer, name='highest_upvoted_answer'),
    path('ajax/send_votes/', views.ans_upvotes, name='ans_upvotes'),
    path('ajax/send_upvoters_list/', views.see_all_upvoters, name='see_all_upvoters')
]