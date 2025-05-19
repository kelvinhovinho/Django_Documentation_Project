from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect

from .models import Question, Choice
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list":latest_question_list}
    return render(request, 'polls/index.html', context)


def details(request, question_id):
    question = Question.objects.get(pk=question_id)
    context = {"question":question} 
    return render(request, 'polls/detail.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{"question":question, "error_message":"You dint"})
    
    else:
        selected_choice.votes = F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})