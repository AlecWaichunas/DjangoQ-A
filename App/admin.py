from django.contrib import admin

# Register your models here.
from .forms import QuestionForm, ClassForm
from .models import *

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'asker']
	form = QuestionForm

	class Meta:
		model = Question

class ClassAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'description', 'id', 'owner', 'is_private', 'code']
	form = ClassForm

	class Meta:
		model = UserDefinedClass
		
class UserAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'id']
	
	class Meta:
		model = UserProfile
		
class SchoolAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'id']
	
	class Meta:
		model = School

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserDefinedClass, ClassAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Discussion)
admin.site.register(Updates)
