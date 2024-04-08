from django.shortcuts import render,get_object_or_404
from .models import Board

from django.http import HttpResponse, Http404

# Create your views here.


def home(request):
    boards = Board.objects.all()
    # boards_names = []

    # for board in boards:
    #     boards_names.append(board.name)

    # response_html = '<br>'.join(boards_names)

    # return HttpResponse(response_html)

    return render(request, "home.html", {"boards": boards})


def about(request):
    return render(request, "about.html")


def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)

    except Board.DoesNotExist:
        raise Http404
    return render(request, "topics.html", {"board": board})


def question(request, pk):
    return HttpResponse(f"Question: {pk}")


def post(request, slug):
    return HttpResponse(f"Slug : {slug}")


def blog_post(request, slug, pk):
    return HttpResponse(f"Blog_post : {slug} and PK:{pk}")


def user_profile(request, username):
    return HttpResponse(f"User name : {username}")


def year_archive(request, year):
    return HttpResponse(f"Year : {year}")



def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'new_topic.html', {'board': board})

