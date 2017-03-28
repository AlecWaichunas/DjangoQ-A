from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import date
import operator

from .forms import *
from .models import *
from Website import settings
from operator import attrgetter

from random import randint
import json



# Global Variables


site_slogan = 'For Students, By Students'
site_name = 'Clask'


# User profile stuff

@login_required
def profile_view(request, messages_show):
	if messages_show == unicode('1'):
		message_boolean = True
	else:
		message_boolean = False
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	notifications = Notifications.objects.filter(user=user_profile).order_by('-date')[:10]
	title = str(user_profile.user.username) + '\'s profile | ' + site_name
	classes = user_profile.classes.all()
	question_count = Question.objects.filter(asker = user_profile).count()
	answer_count = Answer.objects.filter(answerer = user_profile).count()
	context = {
		'messages_show': message_boolean,
		'profile_notifications': notifications,
		'user_profile': user_profile,
		'classes': classes,
		'title': title,
		'answer_count': answer_count,
		'question_count': question_count,
	}
	return render(request, 'profile.html', context)


def register(request):
	error_messages = []
	registered = False
	title = 'Register for ' + site_name
	if request.method == 'POST':
		user_form = UserForm(request.POST or None)
		profile_form = UserProfileForm(request.POST or None)
		emails = []
		for user in UserProfile.objects.all():
			emails.append(user.user.email)
		if not user_form.is_valid() or not profile_form.is_valid():
			alert = 'Username is aleady taken'
			return HttpResponseRedirect('/register/?error_messages=' + alert)
		elif request.POST.get('email') in emails:
			alert = 'Email is aleady in use'
			return HttpResponseRedirect('/register/?error_messages=' + alert)
		elif not request.POST.get('conditions_check', False):
			alert = 'Please check terms of agreement'
			return HttpResponseRedirect('/register/?error_messages=' + alert)
		else:
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.id = user.id
			
			# if 'picture' in request.FILES:
			# 	profile.picture = request.FILES['picture']  # for adding a profile picture for users

			profile.save()
			
			confirm_url = gen_random_url()
			unique = True
			while not unique:
				for i in ConfirmLink.objects.all():
					if confirm_url == i.url:
						unique = False
						confirm_url = gen_random_url()
			link_ob = ConfirmLink.objects.create(url=confirm_url, user=profile)
			link_ob.save()
			send_mail('Confirm Email', 'Username: ' + str(user.username) + '\n http://django-website-zacode11.c9.io/confirm_account/' + str(link_ob.url) + '/\n', 'service@clask.io', [user.email], fail_silently=False)
			
			registered = False
			print(user.username + ' registered')
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context = {
		'user_form': user_form,
		'profile_form': profile_form,
		'registered': registered,
		'title': title,
		'error_messages': request.GET.get('error_messages', False),
	}

	return render(request, 'register.html', context)

def terms_of_service(request):
	context = {'title': 'Terms of agreement' + ' | ' + site_name}
	return render(request, 'terms_of_service.html')

# if called 'login' will create a recursion error because of the default django 'logout()' method #### optional for redirect #### return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
def login_view(request):
    next = request.GET.get('next')
    title = 'Login to ' + site_name
    error_message = request.GET.get('error_message', '')
    message = request.GET.get('error_message', '')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(username=username, password=password)
        try:
        	user_profile = UserProfile.objects.get(user=user)
        except:
        	return HttpResponseRedirect('/login/?error_message=Incorrect Username or Password!')
        
        if not remember_me:
        	request.session.set_expiry(0)
        	
        if user is not None:
            if user.is_active:
                login(request, user)
                print(user.username + ' logged in')
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Inactive User!')
        else:
            messages.add_message(request, messages.ERROR, 'Username or password is invalid')

    return render(request, 'login.html', { 'redirect_to': next, 'title': title, 'error_message': error_message, 'message': message })

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
	
# This page sends an email to remake password
def forgot_password(request):
	context = {}
	if request.method == 'POST':
		username = request.POST.get('username', False)
		results = User.objects.filter(username=username)
		if results is not None and len(results) == 1:
			reset_url = gen_random_url()
			unique = True
			while not unique:
				for i in PasswordLink.objects.all():
					if reset_url == i.url:
						unique = False
						reset_url = gen_random_url()
			link = PasswordLink()
			link.url = reset_url
			link.user = UserProfile.objects.get(user=results[0])
			link.save()
			
			send_mail('Forgot Password', 'Username: ' + str(results[0]) + '\n http://django-website-zacode11.c9.io/reset_password/' + str(link.url) + '/\n', 'service@clask.io', [results[0].email], fail_silently=False)
			success_message = 'Sent link via email to ' + username
			context = { 'success_message': success_message }
		else:
			error_message = 'There is no user with the username ' + username
			context = { 'error_message': error_message }
	return render(request, 'forgot_password.html', context)
	
def reset_password(request, url_code):
	context = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		new_password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		if username and new_password and confirm_password:
			user_ob = User.objects.get(username=username)
			if user_ob.email == email:
				user_profile = UserProfile.objects.get(user=user_ob)
				link_ob = PasswordLink.objects.get(url=url_code)
				if link_ob.user == user_profile and link_ob.is_active:
					if new_password == confirm_password:
						link_ob.is_active = False
						link_ob.save()
						user_ob = User.objects.get(username=username)
						user_ob.set_password(new_password)
						user_ob.save()
						context = { 'success_message': 'Changed password!' }
						link_ob.is_active = False
						link_ob.save()
		else:
			error_message = 'Error broh'
			context = { 'error_message': error_message }
	return render(request, 'reset_password.html', context)
	
def confirm_account(request, url_code):
	link_ob = ConfirmLink.objects.get(url=url_code)
	if link_ob != None and link_ob.is_active:
		link_ob.user.is_confirmed = True
		link_ob.user.save()
		
		link_ob.is_active = False
		link_ob.save()
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponse('This ip address and account will be frozen and banned if you continue to try this. ')
	return HttpResponseRedirect('/')
	

# def gen_random_pass():
# 	letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
# 	temp_pass = ''
# 	for i in range(0, 13):
# 		temp_pass += letters[randint(0, len(letters)-1)]
# 	return temp_pass
	
def gen_class_code():
	letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
	temp_code = ''
	for i in range(0, 8):
		temp_code += letters[randint(0, len(letters)-1)]
	return temp_code
	
def gen_random_url():
	letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
	url = ''
	for i in range(0, 64):
		url += letters[randint(0, len(letters)-1)]
	return url

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def filter_profanity(words):
	blocked_words = { 'fuck', 'rape', 'abuse', 'hell', 'shit', 'dick', 'faggot', 'fucker', 'cunt', 'nigger', 'nigga' , 'pussy', 'fucking', 'fucktard', 'shitbasket', 'assgoblin' }
	for i in words:
		individual = str(i).split( )
		if i == None:
			continue
		for string in individual:
			for blocked in blocked_words:
				if string.lower() == blocked:
					return True
	return False

# Normal site functions ( NOT user functions )


def index_view(request):
	context = { 'title': site_name }
	if not request.user.is_authenticated():
		print('not logged in')
		return render(request, 'about_us.html', context)
	else:
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		has_classes = False
		updates = Updates.objects.order_by('-date_created')[:4]
		if user_profile.classes.count() == 0:
			has_classes = False
			popular_classes = UserDefinedClass.objects.order_by('-member_count')[:6]
			context = {
				'popular_classes': popular_classes,
				'title': site_name,
				'updates': updates,
				'has_classes': has_classes
			}
		else:
			has_classes = True
			stream = []
			for c in user_profile.classes.all():
				for q in c.questions.order_by('-date_created')[:20]:
					stream.append(q)
				for a in c.assignments.order_by('-date_created')[:20]:
					stream.append(a)
				for d in c.discussions.order_by('-date_created')[:20]:
					stream.append(d)
			stream = sorted(stream, key=attrgetter('date_created'), reverse=False)[:20]
			context = {
				'stream': stream,
				'has_classes': has_classes,
				'updates': updates
			}
		return render(request, 'home.html', context)


def search_view(request):
	schools = []
	classes = []
	questions = []
	answers = []
	if 'query_text' in request.GET:
		query_text = request.GET.get('query_text', False)
		if query_text.strip() != '' and query_text.strip() != '\n':
			search_terms = query_text.split(' ')
			
			# for i in search_terms:
			# 	i = i.lower()
			
			for c in UserDefinedClass.objects.filter(name__icontains=query_text):
				if not c in classes:
					classes.append(c)
			for c in UserDefinedClass.objects.filter(description__icontains=query_text):
				if not c in classes:
					classes.append(c)
			for q in Question.objects.filter(question_text__icontains=query_text):
				if not q in questions:
					questions.append(q)
			for q in Question.objects.filter(question_title__icontains=query_text):
				if not q in questions:
					questions.append(q)
			for a in Answer.objects.filter(text__icontains=query_text):
				if not a in answers:
					answers.append(a)
			for s in School.objects.filter(school_name__icontains=query_text):
				if not s in schools:
					schools.append(s)
		else:
			query_text = 'No query entered!'
	else:
		query_text = 'No query entered'
	title = 'Search for ' + str(query_text) + ' | ' + site_name
	class_length = len(classes)
	question_length = len(questions)
	answer_length = len(answers)
	school_length = len(schools)
	totalResults = class_length + question_length + answer_length + school_length;
	# paginator_classes = Paginator(classes, 2)
	# page = request.GET.get('page')
	# try:
	# 	classes_p = paginator_classes.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	classes_p = paginator_classes.page(1)
	context =  {
		'query': query_text,
		'classes': classes,
		'questions': questions,
		'answers': answers,
		'schools': schools,
		'class_results': class_length,
		'question_results': question_length,
		'answer_results': answer_length,
		'school_results': school_length,
		'total_results': totalResults,
		'title': title,
	}
	print(schools)
	return render(request, 'search.html', context)


def classes(request):
	context = {
		'classes_set': UserDefinedClass.objects.all(),
	}
	return render(request, 'get_classes.html', context)


# if 'picture' in request.FILES:
# profile.picture = request.FILES['picture']  # for adding a profile picture for usersregistered = True
@login_required
def create_class_view(request):
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	
	registered = False
	if request.method == 'POST':
		if user_profile.is_confirmed:
			return HttpResponseRedirect('/create_class/?error_message=Please verify your account before creating classes.')
		if filter_profanity({ request.POST.get('description'), request.POST.get('school_name') }):
			return HttpResponseRedirect('/create_class/?error_message=Don\'t use that kind of language on our site.')
		form = ClassForm(request.POST or None)
		school_form = SchoolForm(request.POST or None)
		if request.POST['name'].strip() == '' or request.POST['description'].strip() == '' or request.POST['school_name'].strip() == '':
			return HttpResponseRedirect('/create_class/?error_message=You left a field blank')
		if form.is_valid():
			Class = form.save(commit=False)
			Class.save()
			Class.owner = user_profile
			print(Class.owner.user.username)
			Class.members.add(user_profile)
			is_new = True
			for school in School.objects.all():
				if school.school_name == request.POST['school_name'].strip() and school.state == request.POST['state'].strip():
					is_new = False
					break
			if not is_new:
				# switch to lowercase to keep from more of the same school being created
				# school.lower()
				school = School.objects.get(school_name=request.POST['school_name'].strip(), state = request.POST['state'].strip())
			else:
				school = school_form.save(commit=False)
				school.save()
			school.classes.add(Class)
			school.save()
			Class.school = school
			Class.save()
			
			confirm_url = gen_random_url()
			unique = True
			while not unique:
				for i in ClassConfirmLink.objects.all():
					if confirm_url == i.url:
						unique = False
						confirm_url = gen_random_url()
			link_ob = ClassConfirmLink.objects.create(url=confirm_url, user=user_profile, single_class=Class)
			link_ob.save()
			send_mail('Confirm Class Creation', 'Username: ' + str(request.user.username) + '\n http://django-website-zacode11.c9.io/confirm_account/' + str(link_ob.url) + '/\n', 'service@clask.io', [request.user.email], fail_silently=False)
			
			if Class.is_private:
				print("Generating code")
				is_unique = False
				while not is_unique:
					code = gen_class_code()
					for single_class in UserDefinedClass.objects.all():
						if single_class.code == code:
							is_unique = False
						else:
							is_unique = True
				Class.code = code
				Class.save()
			print('%s created %s' % (request.user.username, Class.name))
			user_profile.classes.add(Class)
			user_profile.save()
			
			return HttpResponseRedirect('/c/' + str(Class.id))
		else:
			print(form.errors)
	else:
		form = ClassForm()
		school_form = SchoolForm()
	
	context = {
		'form': form,
		'registered': registered,
		'error_message': request.GET.get('error_message', False),
		'title': 'Create a class ' + '| ' + site_name
	}
	return render(request, 'create_class.html', context)
	
def school_autocomplete(request):
	if request.is_ajax():
		q = request.GET.get('school_name', '')
		schools = School.objects.filter(school_name__icontains = q)[:20]
		results = []
		for school in schools:
			school_json = {}
			school_json['id'] = school.id
			school_json['label'] = school.school_name
			school_json['value'] = school.school_name
			results.append(school)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
	
def confirm_class_creation(request, url_code):
	link_ob = ClassConfirmLink.objects.get(url=url_code)
	if link_ob != None and link_ob.is_active:
		link_ob.is_active = False
		link_ob.save()
	else:
		return HttpResponse('This ip address and account will be frozen and banned if you continue to try this. ')
	return HttpResponseRedirect('/')


# @login_required
def view_single_class(request, class_id):
	single_class = UserDefinedClass.objects.get(pk=class_id)
	
	if request.method == 'POST':
		if 'submit_code' in request.POST:
			provided_code = request.POST.get('class_code')
			if provided_code == single_class.code:
				return HttpResponseRedirect('/join_private/' + str(class_id) + '/' + str(provided_code) + '/')
			else:
				return HttpResponseRedirect('/c/' + str(single_class.id) + '/?error_message=That class code is invalid')
		if 'submit_user' in request.POST:
			user_name = request.POST['search_user']
			single_class = UserDefinedClass.objects.get(pk=class_id)
			results = User.objects.filter(username__iexact=user_name)
			print(results)
			if results.count() != 0:
				user = User.objects.get(username=user_name)
				return HttpResponseRedirect('/send_invite/' + str(class_id) + '/' + str(user.id))
			else:
				return HttpResponseRedirect('/c/' + str(class_id) + '/?error_message=The user you submitted does not exist')
	
	classAssignments = single_class.assignments.order_by('-date_created')
	assignmentDates = []
	lastDay = ""
	for assignment in classAssignments:
		if assignment.date_created.day != lastDay:
			assignmentDates.append(assignment.date_created)
			lastDay = assignment.date_created.day
	
	
	context = {
		'single_class': single_class,
		'class_questions': single_class.questions.order_by('-date_created'),
		'class_discussions': single_class.discussions.order_by('-date_created'),
		'class_assignments': single_class.assignments.order_by('-date_created'),
		'assignment_dates': assignmentDates,
		'title': single_class.name + ' | ' + site_name
	}
	if request.user.is_authenticated():
		# try:
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		if user_profile in single_class.members.all():
			is_joined = True
		else:
			is_joined = False
		if user_profile == single_class.owner:
			is_owner = True
		else:
			is_owner = False	
		unanswered = []
		for i in single_class.questions.all():
			if i.answers.count() == 0:
				unanswered.append(i)
		most_helpful = single_class.questions.order_by('-votes')
		best_answers = single_class.questions.order_by('-answers')
		
		todays_questions = single_class.questions.order_by('-date')
		
		context = {
			'single_class': single_class,
			'class_questions': single_class.questions.order_by('-date_created'),
			'class_discussions': single_class.discussions.order_by('-date_created'),
			'class_assignments': single_class.assignments.order_by('-date_created'),
			'assignment_dates': assignmentDates,
			'is_joined': is_joined,
			'user_profile': user_profile,
			'all_questions': single_class.questions.all(),
			'unanswered': unanswered,
			'most_helpful': most_helpful,
			'best_answers': best_answers,
			'todays_questions': todays_questions,
			'is_owner': is_owner,
			'error_message': request.GET.get('error_message', False),
			'message': request.GET.get('message', False),
			'title': single_class.name + ' | ' + site_name
		}
		return render(request, 'view_single_class.html', context)
		# except:
		# 	return HttpResponse("error")
	else:
		return render(request, 'view_single_class.html', context)

	
@login_required
def join_public_class(request, class_id):
	user_ob = User.objects.get(id=request.user.id)
	user_profile = UserProfile.objects.get(user=user_ob)
	single_class = UserDefinedClass.objects.get(pk=class_id)
	if user_profile == single_class.owner:
		return HttpResponseRedirect('/c/' + str(single_class.id))
	if single_class.is_private and not user_profile in single_class.members.all():
		return HttpResponseRedirect('/c/' + str(single_class.id))
	# if single_class in user_profile.classes.all():
	# 	return HttpResponseRedirect('/c/' + str(single_class.id) + '/?error_message=You are already in this class!')
	# 	#and request.session['valid_to_join'] 
	# if single_class.is_private == False:
	# 	return HttpResponseRedirect('/c/' + str(single_class.id))
	# del request.session['valid_to_join']
	
	# print(request.session['valid_to_join'])
	
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	if user_profile.is_confirmed:
		if user_profile in single_class.members.all():
			user_profile.classes.remove(single_class)
			single_class.members.remove(user_profile)
			single_class.member_count = single_class.members.count()
			user_profile.save()
			single_class.save()
		else:
			single_class.members.add(user_profile)
			user_profile.classes.add(single_class)
			single_class.member_count = single_class.members.count()
			user_profile.save()
			single_class.save()
	return HttpResponseRedirect('/c/' + str(single_class.id))
	
@login_required
def join_private_class(request, class_id, class_code):
	user_ob = User.objects.get(id=request.user.id)
	user_profile = UserProfile.objects.get(user=user_ob)
	single_class = UserDefinedClass.objects.get(pk=class_id)
	if user_profile == single_class.owner:
		return HttpResponseRedirect('/c/' + str(single_class.id))
	# if single_class in user_profile.classes.all():
	# 	return HttpResponseRedirect('/c/' + str(single_class.id) + '/?error_message=You are already in this class!')
	# 	#and request.session['valid_to_join'] 
	# if single_class.is_private == False:
	# 	return HttpResponseRedirect('/c/' + str(single_class.id))
	# del request.session['valid_to_join']
	
	# print(request.session['valid_to_join'])
	if user_profile.is_confirmed and single_class.code == class_code:
		message =  user_profile.user.username + ' joined ' + single_class.name
		url = '/c/' + str(single_class.id)
		Notifications.objects.create(message=message, url=url, user=single_class.owner)
		single_class.members.add(user_profile)
		user_profile.classes.add(single_class)
		single_class.member_count = single_class.members.count()
		user_profile.save()
		single_class.save()
	else:
		return HttpResponseRedirect('/c/' + str(single_class.id) + '/?error_message=That class code is invalid')
	return HttpResponseRedirect('/c/' + str(single_class.id))

	
@login_required
def add_question(request, class_id):
	if filter_profanity({ request.POST.get('question_text', None), request.POST.get('question_title', None), }):
		return HttpResponseRedirect('/c/' + str(class_id) + '/ask_question/?error_message=Don\'t use that kind of language on our site.')
	if request.user.is_authenticated():
		single_class = UserDefinedClass.objects.get(pk=class_id)
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		if not user_profile in single_class.members.all():
			return HttpResponseRedirect('/c/' + class_id)
		else:
			if request.method == 'POST':
				question_text = request.POST['question_text']
				question_title = request.POST['question_title']
				
				if question_text.strip() == '' or question_title.strip() == '':
					return HttpResponseRedirect('/c/' + class_id + '/ask_question/?error_message=You have a blank title or description')
				is_anon = request.POST.get('is_anon', False)
				question = Question.objects.create(question_text=question_text, question_title=question_title,
				is_anon=is_anon, asker=user_profile, parent_class=single_class)
				single_class.questions.add(question)
				single_class.save()
				return HttpResponseRedirect('/c/' + class_id + '/q/' + str(question.id))
	return render(request, 'ask_question.html', {'error_message': request.GET.get('error_message', False), 'title': 'Ask a question ' + '| ' + site_name})
	
	
def view_single_question(request, class_id, question_id):
	try:
		single_class = UserDefinedClass.objects.get(pk=class_id)
		question = single_class.questions.get(pk=question_id)
	except:
		raise Http404
	if request.method == 'POST':
		if request.user.is_authenticated():
			user_id = request.user.id
			user_ob = User.objects.get(id=user_id)
			user_profile = UserProfile.objects.get(user=user_ob)
			if 'submit_answer' in request.POST:
				if not user_profile in single_class.members.all():
					return HttpResponseRedirect('/c/' + str(class_id) + '/q/' + str(question_id) + '?error_messages=You need to join the class to answer')
				else:
					answer_text = request.POST['answer_text']
					is_anon = request.POST.get('is_anon', False)
					if not user_profile == question.asker:
						if not is_anon:
							message = str(user_ob.username) + ' submitted an answer to your question'
						else:
							message = 'Anonymous submitted an answer to your question'
						url = '/c/' + str(class_id) + '/q/' + str(question_id)
						Notifications.objects.create(message=message, url=url, user=question.asker)
					question.answers.add(Answer.objects.create(text=answer_text, answerer=user_profile, is_anon=is_anon, question=question))
					return HttpResponseRedirect('/c/%s/q/%s' % (str(class_id), str(question_id)))
			elif 'submit_comment' in request.POST:
				if not user_profile in single_class.members.all():
					return HttpResponseRedirect('/c/' + str(class_id) + '/q/' + str(question_id) + '?error_messages=You need to join the class to comment')
				else:
					comment_text = request.POST['comment_text']
					answer_id = request.POST['answer_id']
					answer = Answer.objects.get(pk=answer_id)
					is_anon = request.POST.get('is_anon_comment', False)
					if not user_profile == answer.answerer:
						if not is_anon:
							message = str(user_ob.username) + ' submitted a comment to your answer'
						else:
							message = 'Anonymous submitted a comment to your answer'
						url = '/c/' + str(class_id) + '/q/' + str(question_id)
						Notifications.objects.create(message=message, url=url, user=answer.answerer)
					answer.comments.add(Comments.objects.create(text=comment_text, commenter=user_profile, is_anon=is_anon, answer=answer))
					return HttpResponseRedirect('/c/%s/q/%s' % (str(class_id), str(question_id)))
	context = {}
	# try:
	ip = get_client_ip(request)
	print(ip)
	answers = question.answers.order_by('-points')
	# session = request.session.session_key
	if not Viewer.objects.filter(ip=ip):
		Viewer.objects.create(ip=ip, question=question)
		question.views = Viewer.objects.filter(question=question).count()
		question.save()
	if request.user.is_authenticated():
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		if user_profile in single_class.members.all():
			is_member = True
		else:
			is_member = False
		if question.votes.filter(user=user_profile).count() == 1:
			vote_question = True
		else:
			vote_question = False
	else:
		vote_question = False
		is_member = False
	context = {
		'single_class': single_class,
		'question': question,
		'question_id': question_id,
		'answers': answers,
		'error_messages': request.GET.get('error_messages', False),
		'is_member': is_member,
		'vote_question': vote_question,
		'title': question.question_title + ' | ' + site_name
		# 'votes': answers.votes.filter(user = user_profile),
	}
	# except:
	# 	raise Http404
	return render(request, 'view_single_question.html', context)
	
	
# @login_required
# def add_answer(request, class_id, question_id):
# 	if request.user.is_authenticated:
	
# 		single_class = UserDefinedClass.objects.get(pk=class_id)
# 		user_id = request.user.id
# 		user_ob = User.objects.get(id=user_id)
# 		user_profile = UserProfile.objects.get(user=user_ob)
	
# 		# FIX THIS
# 		if not user_profile in single_class.members.all():
# 			return HttpResponseRedirect('/c/' + str(class_id) + '/q/?error_message=You need you join the class to answer')
# 		else:
# 			if request.method == 'POST':
# 				answer_text = request.POST['answer_text']
# 				user_id = request.user.id
# 				user_ob = User.objects.get(id=user_id)
# 				user_profile = UserProfile.objects.get(user=user_ob)
# 				is_anon = request.POST.get('is_anon', False)
# 				question = single_class.questions.get(pk=question_id)
# 				message = str(user_profile.username) + ' submitted an answer to your question'
# 				url = '/c/' + str(class_id) + '/q/' + str(question_id)
# 				Notifications.objects.create(message=message, url=url, user=question.asker)
# 				question.answers.add(Answer.objects.create(text=answer_text, answerer=user_profile, is_anon=is_anon))
# 				return HttpResponseRedirect('/c/%s/q/%s' % (str(class_id), str(question_id)))
# 		return render(request, 'add_answer.html', {})
# 	return render(request, 'ask_question.html', {'error_message': request.GET.get('error_message', False)})
	

@login_required
def vote_question(request, class_id, question_id):
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	question = Question.objects.get(pk=question_id)
	single_class = UserDefinedClass.objects.get(pk=class_id)
	
	if QVote.objects.filter(user=user_profile, question=question).exists():
		pass
	elif question.asker.id == user_id:
		return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id) + '/?error_messages=You can\'t vote on your own question')
	else:
		vote = QVote.objects.create(user=user_profile, question=question)
		question.points += 1
		question.asker.points +=1
		question.votes.add(vote)
		question.asker.save()
		question.save()
		return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id))
	return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id))


@login_required
def vote_answer(request, answer_id, question_id, positive):
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	answer = Answer.objects.get(pk=answer_id)
	question = Question.objects.get(pk=question_id)
	single_class = question.parent_class
	if positive == unicode('1'):
		is_negative = False
	else:
		is_negative = True
	print(answer.answerer.id)
	print(user_profile.id)
	if answer.votes.filter(user=user_profile).exists():
		previous_vote = answer.votes.get(user=user_profile)
		if previous_vote.is_negative != is_negative:
			if is_negative:
				answer.points -= 2
				answer.answerer.points -=2
			else:
				answer.points += 2
				answer.answerer.points +=2
			
			answer.answerer.save()
			answer.save()
			previous_vote.is_negative = is_negative
			previous_vote.save()
		else:
			pass
	elif answer.answerer.id == user_profile.id:
		return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id) + '/?error_messages=You can\'t vote on your own answer')
	else:
		if not is_negative:
			answer.points += 1
			answer.answerer.points +=1
		else:
			answer.points -= 1
			answer.answerer.points -=1
		answer.answerer.save()
		answer.save()
		
		answer.votes.add(Vote.objects.create(user=user_profile, is_negative=is_negative))
		# return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id))
	return HttpResponseRedirect('/c/' + str(single_class.id) + '/q/' + str(question.id))
	
def redirect_notifications(request, notification_id):
	notification = Notifications.objects.get(pk=notification_id)
	notification.is_viewed = True
	notification.save()
	return HttpResponseRedirect(notification.url)

@login_required
def create_discussion(request, class_id):
	if request.user.is_authenticated():
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		single_class = UserDefinedClass.objects.get(pk=class_id)
		if not user_profile in single_class.members.all():
			return HttpResponseRedirect('/c/' + class_id)
		else:
			if request.method == 'POST':
				discussion_text = request.POST['discussion_text']
				discussion_title = request.POST['discussion_title']
				
				if discussion_text.strip() == '' or discussion_title.strip() == '':
					return HttpResponseRedirect('/c/' + class_id + '/create_discussion/?error_message=You have a blank title or description')
				is_anon = request.POST.get('is_anon', False)
				discussion = Discussion.objects.create(text=discussion_text, title=discussion_title,
				is_anon=is_anon, creator=user_profile, parent_class=single_class)
				single_class.discussions.add(discussion)
				single_class.save()
				return HttpResponseRedirect('/c/' + str(class_id) + '/d/' + str(discussion.id))
			
	return render(request, 'create_discussion.html', {'error_message': request.GET.get('error_message', False), 'title' :'Create discussion ' + '| ' + site_name})
	
def view_single_discussion(request, class_id, discussion_id):
	user_id = request.user.id
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	if request.method == 'POST':
		reply_text = request.POST['reply_text']
		is_anon = request.POST.get('is_anon', False)
		discussion = Discussion.objects.get(pk=discussion_id)
		if not user_profile == discussion.creator:
			if not is_anon:
				message = str(user_ob.username) + ' submitted a reply to your discussion'
			else:
				message = 'Anonymous submitted a reply to your discussion'
			url = '/c/' + str(class_id) + '/d/' + str(discussion_id)
			Notifications.objects.create(message=message, url=url, user=discussion.creator)
		discussion.replies.add(Replies.objects.create(text=reply_text, replier=user_profile, is_anon=is_anon, discussion=discussion))
		return HttpResponseRedirect('/c/%s/d/%s' % (str(class_id), str(discussion_id)))
	context = {}
	try:
		single_class = UserDefinedClass.objects.get(pk=class_id)
		discussion = single_class.discussions.get(pk=discussion_id)
		ip=request.META['REMOTE_ADDR']
		# session = request.session.session_key
		if request.user.is_authenticated():
			user_id = request.user.id
			user_ob = User.objects.get(id=user_id)
			user_profile = UserProfile.objects.get(user=user_ob)
			single_class = UserDefinedClass.objects.get(pk=class_id)
			if user_profile in single_class.members.all():
				is_member = True
			else:
				is_member = False
		if not Viewer.objects.filter(ip=ip):
			Viewer.objects.create(ip=ip, discussion=discussion)
			discussion.views = Viewer.objects.filter(discussion=discussion).count()
			discussion.save()
		context = {
			'single_class': single_class,
			'discussion': discussion,
			'discussion_id': discussion_id,
			'replies': discussion.replies.order_by('date_created'),
			'is_member': is_member,
			'title': discussion.title + ' | ' + site_name
		}
	except:
		raise Http404
	return render(request, 'view_single_discussion.html', context)
	
	
# @login_required
# def invite(request, class_id):
# 	context = {}
# 	if request.method == 'POST':
# 		search_username = request.POST['search_user']
# 		single_class = UserDefinedClass.objects.get(pk=class_id)
# 		results = User.objects.filter(username__iexact=search_username.lower())
# 		context = { 'results': results, 'single_class': single_class }
# 	return render(request, 'invite_user.html', context)

@login_required
def send_user_invite(request, class_id, user_id):
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	single_class = UserDefinedClass.objects.get(pk=class_id)
	
	message = 'You have been invited to ' + single_class.name
	url = '/accept_invite/' + str(class_id) + '/' + str(user_id)
	Notifications.objects.create(message='You have been invited to a class!', user=user_profile, url=url)
	return HttpResponseRedirect('/c/' + str(class_id) + '/?message=You sent an invite to ' + user_profile.user.username)

@login_required
def accept_invite(request, class_id, user_id):
	correct_username = UserProfile.objects.get(pk=user_id).user.username # still the error message
	user_ob = User.objects.get(id=user_id)
	user_profile = UserProfile.objects.get(user=user_ob)
	single_class = UserDefinedClass.objects.get(pk=class_id)
	print('Correct Username: ' + correct_username + ', Request Username: ' + request.user.username + ', Passed in ID: '  + str(user_id) + ', Request id: ' + str(request.user.id))
	if user_profile.id == request.user.id and request.user.username == user_ob.username:
		if request.method == 'POST':
			if request.POST.get('confirm', False):
				request.session['valid_to_join'] = True
				return HttpResponseRedirect('/join_private/' + str(class_id) + '/' + str(UserDefinedClass.objects.get(pk=class_id).code))
	else:
		return HttpResponse('Doesn\'t Work!!')
	return render(request, 'accept_invite.html', {'title': 'Accept invite to ' + single_class.name + ' | ' + site_name, 'class_name': single_class.name })
	
def post_assignment(request, class_id):
	if filter_profanity({ request.POST.get('details'), request.POST.get('assignment_text') }):
		return HttpResponseRedirect('/%2Fc/' + str(class_id) + '/post_assignment/?error_message=Don\'t use that kind of language on our site.')
	if request.user.is_authenticated():
		user_id = request.user.id
		user_ob = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(user=user_ob)
		single_class = UserDefinedClass.objects.get(pk=class_id)
		if not user_profile in single_class.members.all():
			return HttpResponseRedirect('/c/' + str(class_id))
		else:
			if request.method == 'POST':
				assignment_text = request.POST.get('assignment_text')
				is_anon = request.POST.get('is_anon', False)
				details = request.POST.get('details')
				if assignment_text.strip() == '':
					return HttpResponseRedirect('/c/' + str(class_id) + '/post_assignment/?error_message=You have a blank assignment')
				if details.strip() == '':
					return HttpResponseRedirect('/c/' + str(class_id) + '/post_assignment/?error_message=You left details blank')
				user_id = request.user.id
				user_ob = User.objects.get(id=user_id)
				user_profile = UserProfile.objects.get(user=user_ob)
				single_class = UserDefinedClass.objects.get(pk=class_id)
				assignment = Assignments.objects.create(assignment = assignment_text, details=details, poster = user_profile, is_anon=is_anon, parent_class=single_class)
				single_class.assignments.add(assignment)
				return HttpResponseRedirect('/c/' + str(class_id))
			
	return render(request, 'post_assignment.html', {'error_message': request.GET.get('error_message', False), 'title': 'Post assignment' + ' | ' + site_name})
	
def view_single_school(request, school_id):
	school = School.objects.get(pk=school_id)
	context = {
		'school': school,
		'title': school.school_name + ' | ' + site_name
	}
	return render(request, 'view_single_school.html', context)

def ajax_page(request):
	return render(request, 'Ajax_Page.html', {})

def ajax_post_page(request):
	return HttpResponse(request.POST.get('text_input', False))