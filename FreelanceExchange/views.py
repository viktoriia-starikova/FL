from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .my_permissions import MyUserPermissions, IsAdmin
from Users.models import Profile
from Users.serializers import ProfileSerializer
from django.db.models import Q
import json
from datetime import datetime
from dateutil import parser
import logging
from enum import Enum

logger = logging.getLogger('FreelanceExchange')

import pusher

pusher_client = pusher.Pusher(
  app_id='937509',
  key='2dd5ae948f21805d7639',
  secret='4b897456327cee57001a',
  cluster='eu',
  ssl=True
)

class STATE(Enum):
    inProgress = "in progress"
    posted = "posted"
    arbitration = "arbitration"
    completed = "completed"
    resolved = "resolved"

class Messages(APIView):
    """ Tasks пользователя """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=400)

    def get(self, request):
        roomId = request.query_params.get('room')
        room = self.get_object(roomId)
        messages = Message.objects.filter(room_id=roomId)
        ser = MessageSerializer(messages, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = AddMessageSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user=request.user)
            pusher_client.trigger('my-channel'+request.data.get('room'), 'my-event', ser.data)
            return Response(ser.data['id'])
        else:
            logger.error(ser.error_messages)
            return Response(status=400)

class Rooms(APIView):
    """Комнаты чата"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        memberFirst = request.data.get("memberFirst")
        memberSecond = request.data.get("memberSecond")
        rooms = Room.objects.filter(Q(memberSecond = int(memberFirst)) & Q(memberFirst = int(memberSecond)) | Q(memberFirst = int(memberFirst)) & Q(memberSecond = int(memberSecond)))
       
        if(rooms.count()<1):
            room = AddRoomSerializers(data=request.data)
            if room.is_valid():
                room.save()
                return Response(room.data['id'])
        serializer = AddRoomSerializers(rooms[0])
        return Response(serializer.data['id'])


class TopUpBalance(APIView):
    permission_classes = [permissions.IsAuthenticated, ]


class Dialog(APIView):
    """Диалог чата, сообщение"""
    permission_classes = [permissions.IsAuthenticated, ]
    # permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        room = request.GET.get("room")
        chat = Message.objects.filter(room=room)
        serializer = ChatSerializers(chat, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        # room = request.data.get("room")
        dialog = ChatPostSerializers(data=request.data)
        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)


class AddDecision(APIView):
    permission_classes = [permissions.IsAdminUser ]
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=400)

    def get_payment(self, pk):
        try:
            return PaymentHistory.objects.get(pk=pk)
        except PaymentHistory.DoesNotExist:
            return Response(status=400)

    def updateHistory(self, pk):
        snippet = self.get_payment(pk)
        serializer = AddPaymentHistorySerializer(instance=snippet, data={}, partial=True)
        if serializer.is_valid():
            serializer.save(isSent = True)
            return Response(serializer.data)

    def post(self, request):
        ser = AddDecisionSerializer(data=request.data)
        if ser.is_valid():
            ser.save(arbitrator=request.user)
            task = self.get_object(request.data.get("dispute"))

            rightContractor = request.data.get("rightContractor")
            if(int(rightContractor) == task.contractor.id):
                profileContractor = self.get_profile(task.contractor)
                balance = profileContractor.balance + task.price
                profileSerializer = ProfileSerializer(instance=profileContractor, data={}, partial=True)
                if profileSerializer.is_valid():
                    profileSerializer.save(balance = balance)
                    self.updateHistory(task.id)
            else:
                if (int(rightContractor) == task.author.id):
                    profileSender = self.get_profile(task.author)
                    balance = profileSender.balance + task.price
                    profileSerializer = ProfileSerializer(instance=profileSender, data={}, partial=True)
                    if profileSerializer.is_valid():
                        profileSerializer.save(balance = balance)
                        paymentHistory = self.get_payment(task.id)
                        self.check_object_permissions(request, paymentHistory)
                        paymentHistory.delete()

            serializer = TaskSerializer(instance=task, data={}, partial=True)
            if serializer.is_valid():
                serializer.save(state=STATE.resolved.value)
            return Response(status=200)
        else:
            logger.error(ser.error_messages)
            return Response(status=400)


class AddDispute(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def post(self, request):
        ser = AddDisputeSerializer(data=request.data)
        if ser.is_valid():
            taskId = request.data.get("task")
            snippet = self.get_object(int(taskId))
            self.check_object_permissions(request, snippet)
            ser.save(task=snippet, author=request.user)
            serializer = ApprovedTaskSerializer(instance=snippet, data={}, partial=True)
            if serializer.is_valid():
                serializer.save(state=STATE.arbitration.value)
                return Response(serializer.data)
        else:
            logger.error(ser.error_messages)
            return Response(ser.errors, status=400)


class OneDispute(APIView):
    permission_classes = [ permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Dispute.objects.get(pk=pk)
        except Dispute.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        serializer = DisputeSerializer(request)
        return Response(serializer.data)


class AddReview(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=400)

    def post(self, request):
        ser = AddReviewSerializer(data=request.data)
        if ser.is_valid():
            ser.save(addresser=request.user)
            
            id = request.data.get("addressee")
            profile = self.get_profile(id)
            reviews = Review.objects.filter(addressee__id=id)
            sum = 0
            for review in reviews:
                sum = sum + review.estimation
            rating = sum / len(reviews)
            estimation = request.data.get("estimation")
            positiveAssessment = profile.positiveAssessment
            negativeAssessment = profile.negativeAssessment
            if(float(estimation) > 3):
                positiveAssessment += 1
            else:
                negativeAssessment += 1
            profileSerializer = ProfileSerializer(instance=profile, data={}, partial=True)

            if profileSerializer.is_valid():
                profileSerializer.save(rating = rating, positiveAssessment = positiveAssessment, negativeAssessment = negativeAssessment)
            return Response(rating, status=200)
        else:
            logger.error(ser.error_messages)
            return Response(status=400)

class AcceptJob(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)


    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=400)

    def get_payment(self, pk):
        try:
            return PaymentHistory.objects.get(pk=pk)
        except PaymentHistory.DoesNotExist:
            return Response(status=400)

    def updateHistory(self, pk):
        snippet = self.get_payment(pk)
        serializer = AddPaymentHistorySerializer(instance=snippet, data={}, partial=True)
        if serializer.is_valid():
            serializer.save(isSent = True)
            return Response(serializer.data)

    def get(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            profile = self.get_profile(snippet.contractor)
            profileDict = ProfileSerializer(profile)
            profileSerializer = ProfileSerializer(instance=profile, data={}, partial=True)

            req = Request.objects.filter(task=snippet)
            if(profile and request.user == snippet.author and req):
                serializer = ApprovedTaskSerializer(instance=snippet, data=request.data, partial=True)
                self.check_object_permissions(request, snippet)
                self.updateHistory(snippet.id)

                if profileSerializer.is_valid():
                    newBalance = profile.balance + snippet.price
                    profileSerializer.save(balance = newBalance)

                if serializer.is_valid():
                    serializer.save(state=STATE.completed.value)
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
        except:
            return Response(status=400)


class AllPaymentHistory(APIView):
    """Вывод истории платежей"""
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        payments = PaymentHistory.objects.filter((Q(recipient__id=request.user.id) & Q(isSent=True))| Q(sender__id=request.user.id))
        serializer = PaymentHistorySerializer(payments, many=True)
        return Response(serializer.data)


class AddPaymentHistory(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        ser = PaymentHistorySerializer(data=request.data)
        if ser.is_valid():
            ser.save(sender=request.user)
            return Response(ser.data['id'], status=200)
        else:
            logger.error(ser.error_messages)
            return Response(status=400)


class AllDialogs(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        rooms = Room.objects.filter(Q(memberFirst=request.user) | Q(memberSecond =request.user))
        serializer = RoomSerializers(rooms, many=True)
        return Response(serializer.data)


class AddUsersRoom(APIView):
    """Добавление юзеров в комнату чата"""
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        room = request.data.get("room")
        user = request.data.get("user")
        try:
            room = Room.objects.get(id=room)
            room.invited.add(user)
            room.save()
            return Response(status=201)
        except:
            return Response(status=400)


class ArbitrationTasks(APIView):
    permission_classes = [permissions.IsAdminUser, ]
    def get(self, request):
        tasks = Task.objects.filter(state=STATE.arbitration.value)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class AllDoneJobs(APIView):
    """ Вывод всех Request """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        allDoneJobs = DoneJob.objects.all()
        ser = DoneJobSerializer(allDoneJobs, many=True)
        logger.debug(allDoneJobs)
        return Response(ser.data)


class UserDoneJobs(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request):
        allDoneJobs = DoneJob.objects.filter(author=request.user)
        ser = DoneJobSerializer(allDoneJobs, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = AddDoneJobSerializer(data=request.data)
        if ser.is_valid():
            ser.save(author=request.user)
            return Response(ser.data['task'])
        else:
            logger.error(ser.error_messages)
            return Response(status=400)


class DoneJobFiles(APIView):
    """ Вывод, добавление, обновление одного Request """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return DoneJob.objects.get(pk=pk)
        except DoneJob.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        files = request.file_set.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class DisputeDecision(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Dispute.objects.get(pk=pk)
        except Dispute.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        decision = request.decision
        serializer = DecisionSerializer(decision)
        return Response(serializer.data)


class PortfolioWorkFiles(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return PortfolioWork.objects.get(pk=pk)
        except PortfolioWork.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        files = request.file_set.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class AddPortfolioWork(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        ser = AddPortfoliotSerializer(data=request.data)
        if ser.is_valid():
            logger.debug(ser)
            ser.save(avtor=request.user)
            if "img" in request.FILES:
                ser.save(img=request.data["img"])
            return Response(ser.data['id'])
        else:
            logger.error('Комментарий не может быть добавлен: UserPost')
            return Response(status=400)


class AllTasksByCategory(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        categories = request.children.all()
        serializerCategory = CategorySerializer(categories, many=True)

        criterion1 = Q(category=request)
        criterion2 = Q(category__in=categories)
        criterion3 = Q(approved=False)
        tasks = Task.objects.filter((criterion1 | criterion2) & criterion3)
        serializerTask = TaskSerializer(tasks, many=True)
        return Response(serializerTask.data)


class MyTasksByCategory(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        req = self.get_object(pk)
        categories = req.children.all()
        serializerCategory = CategorySerializer(categories, many=True)

        criterion1 = Q(category=req)
        criterion2 = Q(category__in=categories)
        criterion3 = Q(author=request.user)
        tasks = Task.objects.filter((criterion1 | criterion2) & criterion3)
        serializerTask = TaskSerializer(tasks, many=True)
        return Response(serializerTask.data)


class AllFilesByTask(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        files = File.objects.filter(task=request)
        fileSerializer = FileSerializer(files, many=True)
        return Response(fileSerializer.data)


class addFile(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AddFileSerializer(data=request.data)
        if serializer.is_valid():
            if "file" in request.FILES:
                serializer.save(author=request.user)
                serializer.save(file=request.data["file"])
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            logger.error('Файл не может быть загружен: addFile')
            return Response(serializer.errors, status=400)


class updateTaskFiles(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)


    def delete(self, request, pk, format=None):
        try:
            task = self.get_object(pk)
            if (task.state == STATE.posted.value):
                files = File.objects.filter(task=task)
                self.check_object_permissions(request, files)
                for file in files:
                    file.delete()
                return Response(status=204)
            return Response(status=400)
        except:
            return Response(status=400)


class DoneJobDetail(APIView):
    """ Вывод, добавление, обновление одного Request """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return DoneJob.objects.get(pk=pk)
        except DoneJob.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        serializer = DoneJobSerializer(request)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = DoneJobSerializer(
                instance=snippet, data=request.data, partial=True)
            self.check_object_permissions(request, snippet)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response(status=400)
            logger.error('job не может быть обновленa: DoneJobDetail')

    def delete(self, request, pk, format=None):
        try:
            doneJob = self.get_object(pk)
            self.check_object_permissions(request, doneJob)
            doneJob.delete()
            return Response(status=204)
        except:
            return Response(status=400)
            logger.error('job не может быть удаленa: DoneJobDetail')


class AllRequests(APIView):
    """ Вывод всех Request """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        allRequests = Request.objects.all()
        ser = RequestSerializer(allRequests, many=True)
        logger.debug(allRequests)
        return Response(ser.data)


def byRatingSort(profile):
    return profile.rating


class GetRecommendations(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        doneJobs = DoneJob.objects.filter(task__category=task.category)
        authors = []
        for job in doneJobs:
            profile = Profile.objects.get(user=job.author)
            if profile not in authors and job.author != task.author:
                authors.append(Profile.objects.get(user=job.author))
        authors = sorted(authors, key=byRatingSort, reverse=True)[:10]
        serializer = ProfileSerializer(authors, many=True)
        return Response(serializer.data)


class TaskByRequests(APIView):
    """ Requests пользователя """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        allRequests = Task.objects.filter(request__author=request.user)
        ser = TaskSerializer(allRequests, many=True)
        return Response(ser.data) 


class UserRequests(APIView):
    """ Requests пользователя """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        allRequests = Request.objects.filter(author=request.user)
        ser = RequestSerializer(allRequests, many=True)
        return Response(ser.data)

    def post(self, request):
        dataDict = json.dumps(request.data)
        dataString = json.loads(dataDict)
        criterion1 = Q(task=dataString['task'])
        criterion2 = Q(author=request.user)
        requests = Request.objects.filter(criterion1 & criterion2)
        if requests.count() > 0:
            return Response(status=400)
        ser = AddRequestSerializer(data=request.data)
        if ser.is_valid():
            ser.save(author=request.user)
            return Response(status=200)
        else:
            logger.error(ser.error_messages)
            return Response(status=400)


class RequestDetail(APIView):
    """ Вывод, добавление, обновление одного Request """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = RequestSerializer(
                instance=snippet, data=request.data, partial=True)
            self.check_object_permissions(request, snippet)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response(status=400)
            logger.error('запрос не может быть обновлен: RequestDetail')

    def delete(self, request, pk, format=None):
        try:
            task = self.get_object(pk)
            self.check_object_permissions(request, task)
            task.delete()
            return Response(status=204)
        except:
            return Response(status=400)
            logger.error('запрос не может быть удален: RequestDetail')


class AllTasks(APIView):
    """ Вывод всех портфолио """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        allTasks = Task.objects.all()
        ser = TaskSerializer(allTasks, many=True)
        logger.debug(allTasks)
        return Response(ser.data)


class UserTasks(APIView):
    """ Tasks пользователя """
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get(self, request):
        allTasks = Task.objects.filter(author=request.user)
        ser = TaskSerializer(allTasks, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = AddTaskSerializer(data=request.data)
        if ser.is_valid():
            ser.save(author=request.user)
            return Response(ser.data['id'])
        else:
            logger.error(ser.error_messages)
            return Response(status=400)


class Approved(APIView):
    """ Вывод, добавление, обновление одного Task """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)


    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=400)

    def addHistory(self, r, user, total, task):
        s = {'task': task,'sender': r, 'recipient': user, 'total': total}
        dataDict = json.dumps(s)
        dataString = json.loads(dataDict)
        ser = AddPaymentHistorySerializer(data=dataString)
        if ser.is_valid():
            ser.save()
        else:
            logger.error(ser.error_messages)
            return Response(status=400)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            dataDict = json.dumps(request.data)
            dataString = json.loads(dataDict)

            profile = self.get_profile(request.user)
            if(profile.balance<0):
                return Response("insufficient cash", status=400)
            profileDict = ProfileSerializer(profile)
            profileSerializer = ProfileSerializer( instance=profile, data={}, partial=True)

            req = Request.objects.filter(task=snippet)
            if(not snippet.approved and dataString["contractor"] and request.user == snippet.author and req):
                serializer = ApprovedTaskSerializer(
                    instance=snippet, data=request.data, partial=True)
                self.check_object_permissions(request, snippet)
                self.addHistory(request.user.id, dataString["contractor"], snippet.price, snippet.id)
                if profileSerializer.is_valid():
                    newBalance = profile.balance - snippet.price
                    profileSerializer.save(balance = newBalance)

                if serializer.is_valid():
                    serializer.save(state=STATE.inProgress.value)
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
        except:
            return Response(status=400)


class MyActiveTaskDetail(APIView):
    """ Вывод, добавление, обновление одного Task """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # allTasks = Task.objects.filter(Q(contractor=request.user) & Q(state="in progress"))
        allTasks = Task.objects.filter(Q(contractor=request.user))
        ser = TaskSerializer(allTasks, many=True)
        return Response(ser.data)


class TaskDetail(APIView):
    """ Вывод, добавление, обновление одного Task """
    permission_classes = [permissions.AllowAny, IsAdmin]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(
            instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(visits=task.visits+1)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            if(snippet.state == STATE.posted.value and snippet.author == request.user):
                dataDict = json.dumps(request.data)
                data = json.loads(dataDict)
                date = parser.parse(parser.parse(data['deadline']).strftime('%b %d %Y %I:%M%p'))
                dateSnip = parser.parse(snippet.deadline.strftime('%b %d %Y %I:%M%p'))
                if(int(data['price']) < snippet.price or date < dateSnip):
                    return Response("Can not increase the price or reduce the deadline", status=400)
                serializer = UpdateTaskSerializer(
                    instance=snippet, data=request.data, partial=True)
                self.check_object_permissions(request, snippet)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=400)
        except:
            return Response(status=400)

    def delete(self, request, pk, format=None):
        try:
            task = self.get_object(pk)
            if(task.state == STATE.posted.value and task.author == request.user):
                self.check_object_permissions(request, task)
                task.delete()
                return Response(status=204)
            return Response(status=400)
        except:
            return Response(status=400)


class UpdateTask(APIView):
    """ Вывод, добавление, обновление одного Task """
    permission_classes = [permissions.AllowAny, IsAdmin]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=400)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            if(snippet.state == STATE.posted.value and snippet.author == request.user):
                serializer = UpdateTaskSerializer(
                    instance=snippet, data=request.data, partial=True)
                self.check_object_permissions(request, snippet)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=400)
        except:
            return Response(status=400)
            

class AllPortfolio(APIView):
    permission_classes = [permissions.AllowAny, MyUserPermissions]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        avtor = self.get_object(pk)
        portfolio = PortfolioWork.objects.filter(avtor=avtor)
        portfolioSerializer = PortfolioSerializer(portfolio, many=True)
        return Response(portfolioSerializer.data)


class IntrestingPosts(APIView):
    permission_classes = [permissions.AllowAny, MyUserPermissions]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        avtor = self.get_object(pk)
        posts = Post.objects.filter(avtor=avtor).order_by('-like')[:2]
        postsSerializer = PostSerializer(posts, many=True)
        return Response(postsSerializer.data)


class UpdatePortfolioImg(APIView):
    """Редактирование аватара"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RedactIMG(instance=snippet, data=request.data, partial=True)
        if serializer.is_valid():
            if "img" in request.FILES:
                serializer.save(img=request.data["img"])
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        else:
            logger.error('Аватар не может быть обновлен: ImageView')
            return Response(serializer.errors,status=400)


class PortfolioDetail(APIView):
    """ Вывод, добавление, обновление одной работы портфолио """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return PortfolioWork.objects.get(pk=pk)
        except PortfolioWork.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolio = self.get_object(pk)
        portfolioSerializer = PortfolioSerializer(portfolio)
        files = File.objects.filter(portfolioWork=portfolio)
        fileSerializer = FileSerializer(files, many=True)
        return Response({'portfolio': portfolioSerializer.data, 'files': fileSerializer.data})

    def post(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = UpdatePortfolioSerializer(instance=snippet, data=request.data, partial=True)
            self.check_object_permissions(request, snippet)
            if serializer.is_valid():
                serializer.save()
                if "img" in request.FILES:
                    imgSerializer = RedactPortfolioIMG(instance=snippet, data=request.data, partial=True)
                    if imgSerializer.is_valid():
                        imgSerializer.save(img=request.data["img"])
                        return Response(imgSerializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response(status=400)
            logger.error('Работа не может быть обновлена: PortfolioDetail')

    def delete(self, request, pk, format=None):
        try:
            portfolio = self.get_object(pk)
            self.check_object_permissions(request, portfolio)
            portfolio.delete()
            return Response(status=204)
        except:
            return Response(status=400)
            logger.error('Работа не может быть удалена: PortfolioDetail')


class CategoriesAll(APIView):
    """ Вывод всех категорий """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        ser = CategorySerializer(categories, many=True)
        logger.debug(categories)
        return Response(ser.data)


class CategoryChilds(APIView):
    """ Вывод, добавление, обновление одного Request """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=400)

    def get(self, request, pk, format=None):
        request = self.get_object(pk)
        categories = request.children.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """ Вывод, добавление, обновление одного поста """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = CategorySerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(status=200)
        else:
            logger.error(ser.error_messages)
            return Response(status=400)

    def delete(self, request, pk, format=None):
        try:
            post = self.get_object(pk)
            self.check_object_permissions(request, post)
            post.delete()
            return Response(status=204)
        except:
            return Response(status=400)
            logger.error('Категория не может быть удалена: CategoryDetail')


class PostsAll(APIView):
    """ Вывод всех постов """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        tweets = Post.objects.all()
        ser = PostSerializer(tweets, many=True)
        logger.debug(tweets)
        return Response(ser.data)


class CommentsDetail(APIView):
    """ Получение комментов """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk, format=None):
        com = Comment.objects.filter(post=pk)
        ser = CommentSerializer(com, many=True)
        return Response(ser.data)


class UsersReview(APIView):
    """ Получение отзывов """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk, format=None):
        reviews = Review.objects.filter(addresser__id=pk)
        ser = ReviewSerializer(reviews, many=True)
        return Response(ser.data)


class RequestForTask(APIView):
    """ Получение комментов """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk, format=None):
        criterion1 = Q(task=pk)
        criterion2 = Q(author=request.user)
        criterion3 = Q(task__author=request.user)
        requests = Request.objects.filter(
            criterion1 & (criterion2 | criterion3))
        ser = RequestSerializer(requests, many=True)
        return Response(ser.data)


class CommentsDetail2(APIView):
    """Добавление комментов"""
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        ser = AddCommentSerializer(data=request.data)
        if ser.is_valid():
            logger.debug(ser)
            ser.save(avtor=request.user)
            return Response(status=200)
        else:
            logger.error('Комментарий не может быть добавлен: UserPost')
            return Response(status=400)


class UserPost(APIView):
    """ Посты пользователя """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        tweets = Post.objects.filter(avtor=request.user)
        ser = PostSerializer(tweets, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = AddTweetSerializer(data=request.data)
        if ser.is_valid():
            logger.debug(ser)
            ser.save(avtor=request.user)
            return Response(status=200)
        else:
            logger.error('Пост не может быть добавлен: UserPost')
            return Response(status=400)


class Like(APIView):
    """ Ставим лайк """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            pk = request.data.get("pk")
            post = Post.objects.get(id=pk)
            logger.debug(post)
            if request.user in post.user_like.all():
                post.user_like.remove(User.objects.get(id=request.user.id))
                post.like -= 1
            else:
                post.user_like.add(User.objects.get(id=request.user.id))
                post.like += 1
            post.save()
        except:
            logger.error('Лайк не может быть поставлен: Like')
        else:
            logger.debug('Лайк поставлен: Like')
            return Response(status=201)


class PostsDetail(APIView):
    """ Вывод, добавление, обновление одного поста """
    permission_classes = [permissions.AllowAny, MyUserPermissions]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            serializer = PostSerializer(
                instance=snippet, data=request.data, partial=True)
            self.check_object_permissions(request, snippet)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response(status=400)
            logger.error('Пост не может быть обновлен: PostsDetail')

    def delete(self, request, pk, format=None):
        try:
            post = self.get_object(pk)
            self.check_object_permissions(request, post)
            post.delete()
            return Response(status=204)
        except:
            return Response(status=400)
            logger.error('Пост не может быть удален: PostsDetail')
