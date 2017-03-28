from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
	question_text = models.CharField(blank=False, null=False, max_length=5000)
	question_title = models.CharField(blank=False, null=False, max_length=60)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	asker = models.ForeignKey('UserProfile', default=0)
	views = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	is_anon = models.BooleanField(default = False)
	parent_class = models.ForeignKey('UserDefinedClass', default=0, related_name='%(class)s_parent_class')
	answers = models.ManyToManyField('Answer', default=0, related_name='%(class)s_answers')
	votes = models.ManyToManyField('QVote', default=0, related_name='%(class)s_votes')
	def obj_type(self):
		return 'q'
	
	def __unicode__(self):
		return self.question_title
		
class Answer(models.Model):
	text = models.CharField(blank=False, null=False, max_length=5000)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	answerer = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_answerer')
	points = models.IntegerField(default=0)
	is_anon = models.BooleanField(default = False)
	question = models.ForeignKey(Question, default=0, related_name='%(class)s_parent_question')
	comments =  models.ManyToManyField('Comments', default=0, related_name='%(class)s_comments')
	votes =  models.ManyToManyField('Vote', default=0, related_name='%(class)s_votes')

	def __unicode__(self):
		return self.text

class UserDefinedClass(models.Model):
	name = models.CharField(blank=False, null=False, max_length=60)
	description = models.CharField(blank=False, null=False, max_length=400)
	owner = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_owner')
	members = models.ManyToManyField('UserProfile', default=0, related_name='%(class)s_members')
	is_private = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	school_name = models.CharField(blank=False, max_length=50, default=0)
	questions = models.ManyToManyField(Question, default=0, related_name='%(class)s_questions')
	discussions = models.ManyToManyField('Discussion', default=0, related_name='%(class)s_discussions')
	code = models.CharField(blank=False, max_length=9, default=0)
	assignments = models.ManyToManyField('Assignments', default=0, related_name='%(class)s_Assignments')
	school = models.ForeignKey('School', default=0, related_name='%(class)s_school')
	member_count = models.IntegerField(default=0)
	
	# tags = models.CharField(blank=False, null=False, max_length=20)
	
	def __unicode__(self):
		return self.name

class Tag(models.Model):
	slug = models.SlugField(max_length=100, unique=True)
	class Meta:
		ordering = ('slug',)

	def __unicode__(self):
		return self.slug

# For user profiles
class UserProfile(models.Model):
	user = models.OneToOneField(User, default=0, related_name='%(class)s_user')
	is_confirmed = models.BooleanField(blank=False, null=False, default=False)
	website = models.URLField(blank=True)
	classes = models.ManyToManyField(UserDefinedClass, default=0, related_name='%(class)s_classes')
	points = models.IntegerField(default=0, null=True, blank=True)
	
	first_name = models.CharField(blank=True, default='NULL', max_length=20)
	last_name = models.CharField(blank=True, default='NULL', max_length=20)

	def __unicode__(self):
		return self.user.username
		
class Vote(models.Model):
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	user = models.ForeignKey(UserProfile, default=0, related_name='%(class)s_user')
	is_negative = models.BooleanField(default=False)
    
	def __unicode__(self):
		return self.user
		
class QVote(models.Model):
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	user = models.ForeignKey(UserProfile, default=0, related_name='%(class)s_user')
	question = models.ForeignKey(Question, default=0, related_name='%(class)s_question')
    
	def __unicode__(self):
		return self.user
    
class Viewer(models.Model):
	# session = models.CharField(max_length=40, default=0)
	ip = models.CharField(default=0, max_length=50)
	question = models.ForeignKey(Question, default=0, related_name='%(class)s_question')
	discussion = models.ForeignKey('Discussion', default=0, related_name='%(class)s_discussion')
	
	def __unicode__(self):
		return self.ip
		
class Notifications(models.Model):
	message = models.CharField(blank=False, null=False, max_length=100)
	url = models.CharField(blank=False, null=False, max_length=100)
	is_viewed = models.BooleanField(default=False)
	user = models.ForeignKey(UserProfile, default=0, related_name='%(class)s_user')
	date = models.DateTimeField(auto_now_add = True, null=True)
	
	def __unicode__(self):
		return self.message

class Comments(models.Model):
	text = models.CharField(blank=False, null=False, max_length=3000)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	commenter = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_comenter')
	points = models.IntegerField(default=0)
	is_anon = models.BooleanField(default = False)
	answer = models.ForeignKey(Answer, default=0, related_name='%(class)s_parent_answer')
		
class Discussion(models.Model):
	text = models.CharField(blank=False, null=False, max_length=6000)
	title = models.CharField(blank=False, null=False, max_length=60)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	creator = models.ForeignKey('UserProfile', default=0)
	views = models.IntegerField(default=0)
	is_anon = models.BooleanField(default = False)
	parent_class = models.ForeignKey('UserDefinedClass', default=0, related_name='%(class)s_parent_class')
	replies = models.ManyToManyField('Replies', default=0, related_name='%(class)s_replies')
	def obj_type(self):
		return 'd'
	
	def __unicode__(self):
		return self.title
		
class Replies(models.Model):
	text = models.CharField(blank=False, null=False, max_length=5000)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	replier = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_answerer')
	is_anon = models.BooleanField(default = False)
	discussion = models.ForeignKey(Discussion, default=0, related_name='%(class)s_discussion')

	def __unicode__(self):
		return self.text
		
class School(models.Model):
	school_name = models.CharField(blank=False, null=False, max_length=100)
	classes = models.ManyToManyField('UserDefinedClass', default=0, related_name='%(class)s_questions')
	state = models.CharField(blank=False, null=False, max_length=2)
	
	def __unicode__(self):
		return self.school_name
	
class Assignments(models.Model):
	assignment = models.CharField(blank=False, null=False, max_length=200)
	details = models.CharField(blank=False, null=False, max_length=2000, default = 0) 
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	poster = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_poster')
	is_anon = models.BooleanField(default = False)
	parent_class = models.ForeignKey('UserDefinedClass', default=0, related_name='%(class)s_parent_class')
	def obj_type(self):
		return 'a'
		
	def __unicode__(self):
		return self.assignment

class Updates(models.Model):
	title = models.CharField(blank=False, null=False, max_length=200)
	body = models.CharField(blank=False, null=False, max_length=500)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	
	def __unicode__(self):
		return self.title
		
class PasswordLink(models.Model):
	url = models.CharField(blank=False, null=False, default=0, max_length=128)
	user = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_user')
	is_active = models.BooleanField(blank=False, null=False, default=True)
	
	def __unicode__(self):
		return self.url

class ConfirmLink(models.Model):
	url = models.CharField(blank=False, null=False, default=0, max_length=128)
	user = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_user')
	is_active = models.BooleanField(blank=False, null=False, default=True)
	
	def __unicode__(self):
		return self.url
		
class ClassConfirmLink(models.Model):
	url = models.CharField(blank=False, null=False, default=0, max_length=128)
	user = models.ForeignKey('UserProfile', default=0, related_name='%(class)s_user')
	is_active = models.BooleanField(blank=False, null=False, default=True)
	single_class = models.ForeignKey('UserDefinedClass', default=0, related_name='%(class)s_class')
	
	def __unicode__(self):
		return self.url