from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Room(models.Model):
    """Модель комнаты чата"""
    memberFirst =  models.ForeignKey(User, related_name='memberFirst', on_delete=models.CASCADE)
    memberSecond =  models.ForeignKey(User, related_name='memberSecond', on_delete=models.CASCADE)
    createdDate = models.DateTimeField(default=timezone.now)

    class MPTTMeta:
        ordering = ['-createdDate']

    def __str__(self):
        return "room"


class Message(models.Model):
    """Модель чата"""
    room = models.ForeignKey(Room, verbose_name="room", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    text = models.TextField("message", max_length=500)
    createdDate = models.DateTimeField(default=timezone.now)

    class MPTTMeta:
        ordering = ['-createdDate']

    def __str__(self):
        return self.text


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=50)
    state = models.CharField(max_length=30, default="posted")
    description = models.TextField()
    createdDate = models.DateTimeField(default=timezone.now)
    price = models.IntegerField(default=0)
    deadline = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractor', blank=True, null=True)
    visits = models.IntegerField(default=0)

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return self.title


class Service(models.Model):
    createdDate = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    minTerm = models.IntegerField(default=0)
    minCost = models.IntegerField(default=0)
    minRate = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['createdDate']

    def __str__(self):
        return self.text


class PaymentHistory(models.Model):
    createdDate = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    total = models.IntegerField(default=0)
    isSent = models.BooleanField(default=False)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return "PaymentHistory"


class Request(models.Model):
    message = models.TextField(blank=True, null=True)
    createdDate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['createdDate']

    def __str__(self):
        return "Request"


class Dispute(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return self.message


class Decision(models.Model):
    rightContractor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='rightContractor')
    message = models.TextField()
    arbitrator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arbitrator')
    dispute = models.OneToOneField(Dispute, on_delete=models.CASCADE, primary_key=True)
    createdDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class DoneJob(models.Model):
    message = models.TextField(blank=True)
    createdDate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)
    
    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return self.message


def content_file_name(instance, filename):
    return '/'.join(['user_files', instance.author.username, instance.createdDate.strftime('%Y-%m-%d'), filename])


class PortfolioWork(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    avtor = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='portfolio_images', default='portfolio_default.png',)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "PortfolioWork"


class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=content_file_name)
    createdDate = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    doneJob = models.ForeignKey(DoneJob, on_delete=models.CASCADE, blank=True, null=True)
    portfolioWork = models.ForeignKey(PortfolioWork, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return "File"


class Review(models.Model):
    message = models.TextField(default="")
    createdDate = models.DateTimeField(default=timezone.now)
    estimation = models.FloatField(default=0)
    addressee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addressee')
    addresser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresser')

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return self.message


class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    avtor = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    user_like = models.ManyToManyField(User, verbose_name="Кто лайкнул", related_name="users_like")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    avtor = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.text
