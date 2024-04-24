from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.db.models import Count

## Class based View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from .models import Board
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse


# Create your views here.


class BoardListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = "home.html"


# def home(request):
#     boards = Board.objects.all()
# boards_names = []

# for board in boards:
#     boards_names.append(board.name)

# response_html = '<br>'.join(boards_names)

# return HttpResponse(response_html)

# return render(request, "home.html", {"boards": boards})


def about(request):
    return render(request, "about.html")


class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"
    template_name = "topics.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs["board"] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get("pk"))
        queryset = self.board.topics.order_by("-last_update").annotate(
            replies=Count("posts") - 1
        )
        return queryset


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by("-last_update").annotate(
#         replies=Count("posts") - 1
#     )
#     page = request.GET.get("page", 1)

#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # probably the user tried to add a page number
#         # in the url, so we fallback to the last page
#         topics = paginator.page(paginator.num_pages)

#     return render(request, "topics.html", {"board": board, "topics": topics})


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     topics = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
#     return render(request, 'topics.html', {'board': board, 'topics': topics})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True           # <-- until here

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('create_at')
        return queryset


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


# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == "POST":
#         subject = request.POST["subject"]
#         message = request.POST["message"]

#         user = User.objects.first()  #     TODO: GET the currently logged in user

#         topic = Topic.objects.create(subject=subject, board=board, starter=user)

#         post = Post.objects.create(message=message, topic=topic, create_by=user)
#         return redirect(
#             "board_topics", pk=board.pk
#         )  # TODO:  redirect to the created topic page

#     return render(request, "new_topic.html", {"board": board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                create_by=request.user,
            )
            return redirect(
                "topic_posts", pk=pk, topic_pk=topic.pk
            )  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, "new_topic.html", {"board": board, "form": form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, "topic_posts.html", {"topic": topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.create_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# Class  based views


class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post_list")
    template_name = "new_post.html"


@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ("message",)
    template_name = "edit_post.html"
    pk_url_kwarg = "post_pk"
    context_object_name = "post"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(create_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.update_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", pk=post.topic.board.pk, topic_pk=post.topic.pk)



