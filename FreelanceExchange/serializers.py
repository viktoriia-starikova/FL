# posts/serializers.py
from rest_framework import serializers
from . import models
from .models import *
from Users.models import Profile
from django.contrib.auth.models import User


class UserSerialiser(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class AddPortfoliotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioWork
        fields = ('id','title','text')


class PortfolioSerializer(serializers.ModelSerializer):
    """Серилизация portfolio"""
    avtor=UserSerialiser()
    class Meta:
        model = PortfolioWork
        fields = ('id', 'title','text', 'date', 'avtor', 'img')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.avtor = validated_data.get('avtor', instance.avtor)
        instance.date = validated_data.get('date', instance.date)
        instance.img = validated_data.get('img', instance.date)
        instance.save()
        return instance


class RedactPortfolioIMG(serializers.ModelSerializer):
    """Серилизация portfolio"""
    class Meta:
        model = PortfolioWork
        fields = ('id','img')

    def update(self, instance, validated_data):
        instance.img = validated_data.get('img', instance.img)
        instance.save()
        return instance


class UpdatePortfolioSerializer(serializers.ModelSerializer):
    """Серилизация portfolio"""
    class Meta:
        model = PortfolioWork
        fields = ('id','title','text')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    """Серилизация поста"""
    avtor=UserSerialiser()
    class Meta:
        model = Post
        fields = ('id', 'title','text', 'date', 'avtor','like', 'user_like')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.avtor = validated_data.get('avtor', instance.avtor)
        instance.like = validated_data.get('like', instance.like)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


class AddCommentSerializer(serializers.ModelSerializer):
    """Добавление коммента"""
    # post=PostSerializer()
    class Meta:
        model = Comment
        fields = ("text","post",)


class CategorySerializer(serializers.ModelSerializer):
    """Серилизация категории"""
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def get_parent(self, obj):
        if obj.parent is not None:
            return CategorySerializer(obj.parent).data
        else:
            return None


class CommentSerializer(serializers.ModelSerializer):
    """Серилизация коммента"""
    avtor=UserSerialiser()
    class Meta:
        model = Comment
        fields = ('id', 'text', 'date', 'avtor','post')

class AddTweetSerializer(serializers.ModelSerializer):
    """Добавление поста"""
    class Meta:
        model = Post
        fields = ("title","text",)


class AddTaskSerializer(serializers.ModelSerializer):
    """Добавление поста"""
    class Meta:
        model = Task
        fields = ('id','title','description', 'price', 'deadline', 'category')

class ApprovedTaskSerializer(serializers.ModelSerializer):
    """Серилизация поста"""
    class Meta:
        model = Task
        fields = ('state', 'approved', 'contractor')

    def update(self, instance, validated_data):
        instance.state = validated_data.get('state', instance.state)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.contractor = validated_data.get('contractor', instance.contractor)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    """Серилизация поста"""
    author=UserSerialiser()
    contractor=UserSerialiser()
    category= CategorySerializer()
    class Meta:
        model = Task
        fields = ('id','title','state', 'description', 'author','createdDate', 'price', 'deadline', 'category', 'approved', 'contractor', 'visits')


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Серилизация поста"""
    class Meta:
        model = Task
        fields = ('title', 'description', 'price', 'deadline', 'category')


class PaymentHistorySerializer(serializers.ModelSerializer):
    """Серилизация платежа"""
    sender = UserSerialiser()
    recipient = UserSerialiser()
    class Meta:
        model = PaymentHistory
        fields = ('createdDate', 'sender', 'recipient', 'total', 'isSent')

class AddPaymentHistorySerializer(serializers.ModelSerializer):
    """Серилизация платежа"""
    class Meta:
        model = PaymentHistory
        fields = ('sender', 'recipient', 'total', 'task')

class AddRequestSerializer(serializers.ModelSerializer):
    """Серилизация Request"""
    class Meta:
        model = Request
        fields = ('message', 'task')


class RequestSerializer(serializers.ModelSerializer):
    """Серилизация Request"""
    author=UserSerialiser()
    task=TaskSerializer()
    class Meta:
        model = Request
        fields = ('message','accepted', 'createdDate', 'author', 'task')

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.createdDate = validated_data.get('createdDate', instance.createdDate)
        instance.author = validated_data.get('author', instance.author)
        instance.task = validated_data.get('task', instance.task)
        instance.save()
        return instance


class AddDoneJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneJob
        fields = ('message','task')


class DoneJobSerializer(serializers.ModelSerializer):
    """Серилизация Request"""
    author=UserSerialiser()
    task=TaskSerializer()
    class Meta:
        model = DoneJob
        fields = ('message', 'createdDate', 'author', 'task')

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.createdDate = validated_data.get('createdDate', instance.createdDate)
        instance.author = validated_data.get('author', instance.author)
        instance.task = validated_data.get('task', instance.task)
        instance.save()
        return instance


class DisputeSerializer(serializers.ModelSerializer):
    """Серилизация Dispute"""
    class Meta:
        model = Dispute
        fields = ('message', 'task')


class AddDisputeSerializer(serializers.ModelSerializer):
    """Серилизация Dispute"""
    class Meta:
        model = Dispute
        fields = ('message', 'task')


class DecisionSerializer(serializers.ModelSerializer):
    """Серилизация Dispute"""
    rightContractor=UserSerialiser()
    dispute=DisputeSerializer()
    arbitrator=UserSerialiser()

    class Meta:
        model = Decision
        fields = ('message', 'dispute', 'rightContractor', 'arbitrator', 'createdDate')


class AddDecisionSerializer(serializers.ModelSerializer):
    """Серилизация Dispute"""
    class Meta:
        model = Decision
        fields = ('message', 'dispute', 'rightContractor')


class FileSerializer(serializers.ModelSerializer):
    """Серилизация File"""
    author=UserSerialiser()
    task=TaskSerializer()
    doneJob= DoneJobSerializer()
    portfolioWork=PortfolioSerializer()

    class Meta:
        model = File
        fields = ('id', 'file','doneJob', 'createdDate', 'author', 'task', 'portfolioWork')


class AddFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file','doneJob', 'task', 'portfolioWork')


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизация Review"""
    addressee=UserSerialiser()
    addresser=UserSerialiser()

    class Meta:
        model = Review
        fields = ('id', 'message', 'estimation','createdDate', 'addresser', 'addressee')

class AddReviewSerializer(serializers.ModelSerializer):
    """Серилизация Review"""
    class Meta:
        model = Review
        fields = ('message', 'estimation', 'addressee')


class RoomSerializers(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    memberFirst = UserSerialiser()
    memberSecond = UserSerialiser()
    class Meta:
        model = Room
        fields = ("id", "memberFirst", "memberSecond", "createdDate")


class MessageSerializer(serializers.ModelSerializer):
    """Сериализация сообщений"""
    user=UserSerialiser()
    room=RoomSerializers()
    class Meta:
        model = Message
        fields = ("id", "room", "user", "createdDate", "text")


class AddMessageSerializer(serializers.ModelSerializer):
    """Сериализация сообщений"""
    class Meta:
        model = Message
        fields = ("id", "room", "text")


class AddRoomSerializers(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    class Meta:
        model = Room
        fields = ("id", "memberFirst", "memberSecond")


class ChatSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    user = UserSerialiser()
    class Meta:
        model = Message
        fields = ("user", "text", "date")


class ChatPostSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    class Meta:
        model = Message
        fields = ("room", "text")