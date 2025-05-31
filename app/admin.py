from django.contrib import admin
from .models import Question  
from .models import Answer 
from .models import Profile 
from .models import Tag


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Tag)
