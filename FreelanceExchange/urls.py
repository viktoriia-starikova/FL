from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path('', PostsAll.as_view()),
    path('posts/<int:pk>/', PostsDetail.as_view()),
    path('intrestingPosts/<int:pk>/', IntrestingPosts.as_view()),

    path('paymentHistory/', AllPaymentHistory.as_view()),
    path('addPaymentHistory/', AddPaymentHistory.as_view()),

    path('myActiveTasks/', MyActiveTaskDetail.as_view()),
    path('tasks/', AllTasks.as_view()),
    path('arbitrationTasks/', ArbitrationTasks.as_view()),
    path('requests/tasks/', TaskByRequests.as_view()),
    path('task/<int:pk>/', TaskDetail.as_view()),
    path('task/detail/<int:pk>/', UpdateTask.as_view()),
    path('files/task/<int:pk>/', updateTaskFiles.as_view()),
    path('approved/<int:pk>/', Approved.as_view()),

    path('portfolio/<int:pk>/', AllPortfolio.as_view()),
    path('portfolioDetail/<int:pk>/', PortfolioDetail.as_view()),
    path('addPortfolio/', AddPortfolioWork.as_view()),

    path('my/', UserPost.as_view()),
    path('my/tasks/', UserTasks.as_view()),
    path('my/requests/', UserRequests.as_view()),
    path('requestsForTask/<int:pk>/', RequestForTask.as_view()),
    path('requests/', AllRequests.as_view()),
    path('request/<int:pk>/', RequestDetail.as_view()),

    path('my/doneJobs/', UserDoneJobs.as_view()),
    path('doneJobFiles/<int:pk>/', DoneJobFiles.as_view()),
    path('doneJobs/', AllDoneJobs.as_view()),
    path('doneJob/<int:pk>/', DoneJobDetail.as_view()),
    path('acceptJob/<int:pk>/', AcceptJob.as_view()),
    
    path('recommendations/<int:pk>/', GetRecommendations.as_view()),

    path('comment/<int:pk>/', CommentsDetail.as_view()),
    path('comment/', CommentsDetail2.as_view()),
    path('like/', Like.as_view()),

    path('categories/', CategoriesAll.as_view()),

    path('cat/', CategoryDetail.as_view()),
    
    path('file/', addFile.as_view()),
    path('categoryChilds/<int:pk>/', CategoryChilds.as_view()),
    path('allTasksByCategory/<int:pk>/', AllTasksByCategory.as_view()),
    path('myTasksByCategory/<int:pk>/', MyTasksByCategory.as_view()),
    path('allFilesByTask/<int:pk>/', AllFilesByTask.as_view()),
    path('room/', Rooms.as_view()),
    path('dialog/', Dialog.as_view()),
    path('messages/', Messages.as_view()),
    
    path('rooms/', AllDialogs.as_view()),
    path('room/user/', AddUsersRoom.as_view()),

    path('review/', AddReview.as_view()),
    path('my/reviews/<int:pk>/', UsersReview.as_view()),
    path('dispute/', AddDispute.as_view()),
    path('dispute/<int:pk>/', OneDispute.as_view()),
    path('decision/', AddDecision.as_view()),
    path('dispute/decision/<int:pk>/', DisputeDecision.as_view()),

]
