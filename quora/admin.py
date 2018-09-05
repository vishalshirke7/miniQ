from django.contrib import admin
from .models import User, Question, Answers, Upvotes
# Register your models here.


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Upvotes)