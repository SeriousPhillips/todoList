from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from math import ceil
from .models import Task
# Create your views here.
"""
def preauth(request):
	return render(request,'todoLst/auth_template.html')

def auth(request):
	print(request.POST)
	return HttpResponseRedirect(reverse( 'todoLst:tt') )
	
def tt(request):
	print(request.POST)
	return HttpResponse('testing')

"""		

fields=['priority','status']
allFields=['task_text']+fields


fieldInfo={ 'status':['waiting','in_progress','done'],
		 'priority': ['low','medium','high']}





pgSize_dflt=10


def index(request):
	if 'signed' in request.session:
		return HttpResponseRedirect( reverse('todoLst:tasks'))
	else:
		return HttpResponseRedirect( reverse('todoLst:sign_in'))
def sign_in(request):
	TasksState.clearSession(request.session)


	return render(request, 'todoLst/sign_in_template.html')

def log_out(request):
	AuthState.clearSession(request.session)
	return HttpResponseRedirect( reverse('todoLst:sign_in'))

def sign_up(request):
	TasksState.clearSession(request.session)

	return render(request, 'todoLst/sign_up_template.html')

def sign_in_process(request):



	#print('running here',request.POST['auth_action'])
	request.session['lgn']=request.POST['lgn']
	request.session['pwd']=request.POST['pwd']
	if 'signed' in request.session:
		del(request.session['signed'])	
	

	if request.POST['auth_action']=='sign up':
		return HttpResponseRedirect( reverse('todoLst:sign_up'))
	else:
		
		return HttpResponseRedirect( reverse('todoLst:tasks'))
def sign_up_process(request):
	request.session['lgn']=request.POST['lgn']
	request.session['pwd']=request.POST['pwd']	
	request.session['pwd2']=request.POST['pwd2']
	if 'signed' in request.session:
		del(request.session['signed'])



	if len(request.POST['lgn'])==0 or len(request.POST['pwd'])==0 or len(request.POST['pwd2'])==0:
		return HttpResponse('all fields nust be filled')
	if request.POST['pwd2']!=request.POST['pwd']:
		return HttpResponse('passwords are different!')

	login=request.POST['lgn']
	try:					
		User.objects.get(username=login)
		return HttpResponse('user with such login already exists')
	
	except 	ObjectDoesNotExist:
		pass
	
	User.objects.create_user(request.session['lgn'], '', request.session['pwd'])

	request.session['signed']=True
	return HttpResponseRedirect( reverse('todoLst:tasks'))






def tasks_old(request):
	user = authenticate(username=request.session['lgn'], password=request.session['pwd'])
	#print( request.POST)
	if user is None:
		if 'signed' in request.session:
			del(request.session['signed'])

		return HttpResponse('authentification problem!!!')
	else:
		request.session['signed']=True
		return HttpResponse('now you can view your tasks, {}'.format(user.username) )
def onAuthProblem():
	return HttpResponseRedirect( reverse('todoLst:sign_in'))



def removeTasks(pks,user):
	if user.is_superuser:
		Task.objects.filter( pk__in=pks ).delete()
	else:
		Task.objects.filter( pk__in=pks, user__username=user.username ).delete()	
def updateTasks(taskDict,user):
	def updateTask(task):
		for field in allFields:
			if field in taskDict[str(task.pk)]:
			
				task.__dict__[field]=taskDict[str(task.pk)][field]
			task.save()
	if user.is_superuser:
		for task in Task.objects.filter( pk__in=list(taskDict) ):
			updateTask(task)

	else:
		for task in user.task_set.filter( pk__in=list(taskDict) ):
			updateTask(task)


def addTask(taskSpecsDict,user):
	if taskSpecsDict:
		user.task_set.create(**taskSpecsDict )

class AuthState:
	def __init__(self,session):
		self.lgn=( session['lgn'] if 'lgn' in session else None  )
		self.pwd=( session['pwd'] if 'pwd' in session else None  )
	def looksAuthd(self):
		return None not in (self.lgn,self.pwd)

	@staticmethod	
	def clearSession(session):
		for field in ['lgn','pwd']:
			if field in session:
				del(session[field])



def getOrAlt(obj,key,alt=None):

	return (obj[key] if key in obj else alt)
	if key in obj:
		return obj[key]
	else:
		return None

class TasksState:
	"""
	extracts task representation/update cofiguration from request.session and request.post
	+
	save representation configurarion into requset.session
	####################
	representation configuraion:

	pgN - page number to show
	pgSize - tasks per page
	filterState - current task filter setting
	
	update configuration:

        update_type - specifies what kind of change if any should be applied to stored task		
	newTaskInfo - dictionary with all fields to create new task
	selected_ids - list of seleted ids
	taskUpdateDict - information how to update selected tasks
	warning - list of warnings that contains description of problems encountered
	(not all update configuration elements presented in every instance)		
	
	

	"""
				
	repFields=['pgN','pgSize','filterState']
	def __init__(self,session, post):
		dfltFieldVals_rep={'pgN':1,'pgSize':pgSize_dflt,'filterState':{}}
		self.warnings=[]	
	
		for field in dfltFieldVals_rep:
			self.__dict__[field]=getOrAlt(session,field,dfltFieldVals_rep[field])

		self.update_type=getOrAlt(post,'update_type','just show' )

		self.selected_ids=(post.getlist('selected_ids') if  'selected_ids' in post else [] )

		


		if self.update_type=='add task':
			newTaskInfo={}
			for field in allFields:
				if field+'__new' not in post:
					self.update_type=='just show'			
					self.warnings.append(" new task can't be created: {} must be specified".format(field))
					newTaskInfo=None
					break
				else:
					newTaskInfo[field]=post[field+'__new']
			self.newTaskInfo=newTaskInfo
			
			self.pgN=1
			
		
		elif self.update_type=='update selected':
			self.taskUpdateDict={}
			for id in self.selected_ids:
				self.taskUpdateDict[id]={}
				for field in allFields:
					if field+'__'+id in post:
						self.taskUpdateDict[id][field]=post[field+'__'+id]

			self.pgN=1

		elif self.update_type=='apply filters':
			self.filterState={}
			for field in fields:
				if field+'__filter' in post:
					self.filterState[field]=post.getlist(field+'__filter')

			self.pgN=1

		elif self.update_type=='go to':
			try:
				self.pgN=int(post['pgN'])
			except Exception:
				self.pgN=1
		elif self.update_type=='Set page size to':
			try:
				self.pgSize=int(post['pgSize'])
				self.pgN=1
			except Exception:
				self.pgSize=pgSize_dflt		
		



		for field in dfltFieldVals_rep:
			session[field]=self.__dict__[field]

		 
		
		
				
	def getFilter(self):
		return {field+'__in':self.filterState[field] for field in self.filterState  }					
			
				
	@staticmethod	
	def clearSession(session):
		for field in TasksState.repFields:
			if field in session:
				del(session[field])
		
						
		


	
def tasks(request):
	authState=AuthState(request.session)
	tasksState=TasksState(request.session,request.POST)

	print(tasksState.__dict__)
	print(request.POST)

	if not authState.looksAuthd():	
		return onAuthProblem()

	
	user = authenticate(username=request.session['lgn'], password=request.session['pwd'])

	if user is None:	
		return onAuthProblem()
	else:
		
		
		if tasksState.update_type=='delete selected':
			removeTasks( tasksState.selected_ids ,user )

		elif tasksState.update_type=='update selected':
			updateTasks( tasksState.taskUpdateDict,user  )

		elif tasksState.update_type=='add task':
			addTask( tasksState.newTaskInfo,user )

			
			
		"""
		if 'priority_filter' in request.POST:
			fltrs['priority__in']=request.POST.getlist('priority_filter')
		
		if 'status_filter' in request.POST:
			fltrs['status__in']=request.POST.getlist('status_filter') 


		fltrs2={field: (fltrs[field+str('__in')] if field+str('__in') in fltrs else []) for field in fields}
		"""
		if user.is_superuser:
			tasks=Task.objects.filter(**tasksState.getFilter()).order_by('-pk')
		else:
			tasks=user.task_set.filter(**tasksState.getFilter()).order_by('-pk')
		
		#taskN=len(tasks)
		pgSize=max(1,tasksState.pgSize)
		maxPgN= max(int(ceil(len(tasks)/ pgSize )),1)
		pgN=min(max( 1, tasksState.pgN  ),maxPgN)
			
		return render(request,'todoLst/tasks_template.html', 
			dict( user=user,isAdmin=user.is_superuser,tasks=tasks[(pgN-1)*pgSize:pgN*pgSize],
				fields=fields,fieldInfo=fieldInfo, filterConf=tasksState.filterState,  pages=list(range(1,maxPgN+1)), pgN=pgN, warnings=tasksState.warnings  )   )				
		
	





def chngTasks(request):
	#print('HERE')
	print('here', request.POST)
	user = authenticate(username=request.session['lgn'], password=request.session['pwd'])

	if user is None:
		if 'signed' in request.session:
			del(request.session['signed'])

		return HttpResponse('authentification problem!!!')
	else:
		request.session['signed']=True
		#print(request.POST,user.is_superuser)
		#print( request.POST['to_del'])
		
		#ress=Task.objects.filter( pk__in=request.POST['to_del'])
		#print ('n ress',len(request.POST.getlist('to_del')))
		if request.POST['update_type']=='delete selected':
			if user.is_superuser:
				Task.objects.filter( pk__in=request.POST.getlist('to_del') ).delete()
			else:
				Task.objects.filter( pk__in=request.POST.getlist('to_del'), user__username=user.username ).delete()
		elif request.POST['update_type']=='update selected':
			print(request.POST.getlist('to_del'))
			for task in Task.objects.filter( pk__in=request.POST.getlist('to_del') ):
				print('updating task', task)
				if  user.is_superuser or user.username==task.user.username:
					print('updating task', task)
					task.priority=int(request.POST[str(task.pk)+'priority'])
					task.status=int(request.POST[str(task.pk)+'status']	)											
					task.save()	
		

			
		#print(request.POST)	
		
		return HttpResponseRedirect( reverse('todoLst:tasks'))



	







