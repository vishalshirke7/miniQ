# **mini-Quora**
### This is a web app developed in python/django which acts same as Q/A website Quora.
### _Tech stack used_
```
- python/django, sqlite
- html, css, javascript
- jquery, ajax
```
### _Application Flow_ **-->**

### Anonymous User :
1. An anonymous user can browse through all questions and answers
2. He/she can view highest upvoted question/answer in past one hour or through out the application
3. He/she can view all the upvoters of a answer
4. He/she **_cannot_** ask a question, answer a question, upvote an answer
5. On trying to upvote he'll be warned to login/register

### Registered/Logged-in User :
1. A logged in user can browse through all questions and answers
2. He/she can view highest upvoted question/answer in past one hour or through out the application
3. He/she **_can_** ask a question, answer a question, upvote an answer
4. A user can upvote an answer only **_once_**
5. A user can view **all questions asked by him/her**
6. A user can view **all answers answered by him/her**
7. A user can view **all the upvotes done by him/her**


## **Datbase Structure** :  (I have used relational sqlite database for this application)

**_Models_** : 

1. User model
```
- keeps the user information such as first,last name, email, password. Email is unique for each user
```
2. Questions model
```
- Contains all the questions and total upvotes for each question
- A foreign key reference to User is been made to track which user has asked the question
- It has a total upvotes field which contains total upvotes for a question
- A questions upvotes is the sum of upvotes of all of it's answeres
```
3. Answers model
```
- All answers are being saved using this model
- It also keeps the count of number of upvotes an answer has received
- This model makes many to one reference to User, Question model respectively
- It saves the time at which an answer has been answered
```
4. Upvotes model
```
- This model is used to keep the track of upvotes by making foreign key references to Answer and User model respectively thus knowing which user has upvoted a questions answer
- This model is helpful in calculating highest number of upvotes for a question/answer in past one hour as well as for entire application as it also make use of DateTimeField saving the time instance at which a user voted an answer
```

# Model relationships explained


![](https://github.com/vishalshirke7/mini-Quora/blob/master/P_20180904_152742%20(1).jpg)

![](https://github.com/vishalshirke7/mini-Quora/blob/master/P_20180904_152804%20(1).jpg)

![](https://github.com/vishalshirke7/mini-Quora/blob/master/P_20180904_152811%20(1).jpg)
