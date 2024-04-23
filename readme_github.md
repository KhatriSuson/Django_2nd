https://github.com/ruman-metahorizon/django_12_00_march_25


https://code.jquery.com/jquery-3.2.1.min.js
https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js
https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js

https://www.markdownguide.org/
# settings.py install apps
django.contrib.humanize

https://gravatar.com/profile

## django checkeditor (visit  site)
https://dev.to/ieeecsvitc/integrating-rich-text-editor-with-django-k19

## Create post in shell

python manage.py shell
from django.contrib.auth.models import User
from boards.models import Board, Topic, Post

user = User.objects.first()

board = Board.objects.get(name='Django')

for i in range(100):
    subject = 'Topic test #{}'.format(i)
    topic = Topic.objects.create(subject=subject, board=board, starter=user)
    Post.objects.create(message='Lorem ipsum...', topic=topic, created_by=user)