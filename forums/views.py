from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import user

# Create your views here.
def detail(request, question_id):
    question = get_object_or_404(user, pk=question_id)
    return HttpResponse("You're looking at question %s." % question.userDob)

def index(request):
    return HttpResponse("You're looking at question")
