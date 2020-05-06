from django.contrib import admin
from .models import *

admin.site.register(Post) ## регистрация сущностей в админ панели
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Task)
admin.site.register(DoneJob)
admin.site.register(File)
admin.site.register(PortfolioWork)
admin.site.register(Dispute)
admin.site.register(Decision)
admin.site.register(Request)
admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PaymentHistory)
