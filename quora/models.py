from django.db import models

# Create your models here.


class User(models.Model):

    fname = models.CharField(max_length=80)
    lname = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)


class Question(models.Model):

    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_upvotes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.question


class Answers(models.Model):

    answer = models.TextField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_upvotes = models.IntegerField(default=0)
    ans_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Upvotes(models.Model):

    upvoted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvoted_answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=False)
