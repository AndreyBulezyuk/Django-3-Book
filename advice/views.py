from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Question

from .models import Advice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.utils import formats

from rest_framework import status
from .serializers import AdviceCreateSerializer


class AdviceCreateView(APIView):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            serializer = AdviceCreateSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                try:
                    question = Question.objects.get(pk=pk)
                except Question.DoesNotExist:
                    return Response({"error" : "Question does not exist!"},status=status.HTTP_400_BAD_REQUEST)
                advice = Advice.objects.create(content=serializer.validated_data["content"], author=user , question=question)
                advice.save()
                data_to_return = {
                    "username": advice.author.username,
                    "user_url": reverse('profile', args=[advice.author.pk], request=request),
                    "user_image":request.build_absolute_uri(advice.author.profile.image.url),
                    "content": advice.content,
                    "date_published":formats.date_format(advice.date_published, "SHORT_DATETIME_FORMAT")
                    }
                return Response(data_to_return, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)


class AdviceListView(APIView):
    def get(self, request, pk=None):
        queryset = Advice.objects.all().filter(question_id=pk).order_by("-date_published")
        data_to_return = []
        for advice in queryset:
            username = advice.author.username
            user_url = request.build_absolute_uri(reverse('profile', args=[advice.author.pk]))
            user_image = request.build_absolute_uri(advice.author.profile.image.url)
            content = advice.content
            date_published = formats.date_format(advice.date_published, "SHORT_DATETIME_FORMAT")
            instance = {
                'username' : username,
                'user_url': user_url,
                'user_image': user_image,
                'content': content,
                'date_published': date_published
            }
            data_to_return.append(instance)
        return Response(data_to_return)



class QuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Question
    fields = ['title']
    success_message  = "Question Created Successfully!"
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form) 

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    success_message  = "Question Deleted Successfully!"
    success_url = "/questions"
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        else: 
            return False 
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionDeleteView, self).delete(request, *args, **kwargs)


class QuestionDetailView(generic.DetailView):
    model = Question

class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 3
    ordering = ['-date_published']