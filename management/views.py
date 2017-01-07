from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate , login , logout
from .models import noteDetail,noteFile,UserProfile,chapters
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from management.forms import UserForm,UserProfileForm,UserPhotoUpdateForm,UserForm2,AddCourseForm,AddSubjectForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.db.models import Q



class branchAndYear(generic.ListView):

	template_name = 'management/test.html'

	def get_context_data(self, **kwargs):
		context = super(branchAndYear, self).get_context_data(**kwargs)
		context['usersList'] = User.objects.all()
		return context

	def get_queryset(self):
		return noteDetail.objects.all()


class detailsBranchAndYear(generic.DetailView):
	model = noteDetail
	
	def get_context_data(self, **kwargs):
		context = super(detailsBranchAndYear, self).get_context_data(**kwargs)
		context['usersList'] = User.objects.all()
		return context

	template_name = 'management/test2.html'	


def signIn(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is None:
			return render(request,'management/signIn.html',{'error':'Invalid username or password'})
		else:
			if user.userprofile.verified is False:
				return render(request,'management/signIn.html',{'error' : 'Sorry, you are blocked!'})
			else:
				login(request,user)
				course = noteDetail.objects.get(Q(branch=user.userprofile.department)&Q(year=user.userprofile.year))
				return redirect('brmadmin:detail',pk = course.id)
	else:
		return render(request,'management/signIn.html')


def signOut(request):
	logout(request)
	return redirect('brmadmin:index')

def register(request):	
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True


			activeUser = authenticate(username=user_form.cleaned_data['username'],password=user_form.cleaned_data['password'])

			if activeUser is not None:
				login(request,activeUser)
			return redirect('brmadmin:index')
		else:
			# print user_form.errors, profile_form.errors
			messages.info(request,str(user_form.errors)+str(profile_form.errors))
			return render(request,'management/regForm.html',{'user_form':user_form,'profile_form':profile_form})
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		return render(request,'management/regForm.html',{'user_form':user_form,'profile_form':profile_form}) 

@login_required(login_url='brmadmin:signIn')
def update(request):

	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		return HttpResponse("invalid user_profile!")

	if request.method == "POST":
		update_user_form = UserForm2(data=request.POST, instance=request.user)
		update_profile_form = UserPhotoUpdateForm(data=request.POST, instance=user_profile)

		if update_user_form.is_valid() and update_profile_form.is_valid():
			user = update_user_form.save()
			profile = update_profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			print("Take me to index")
			return redirect('brmadmin:index')

		else:
			print(update_user_form.errors, update_profile_form.errors)
	else:
		update_user_form = UserForm2(instance=request.user)
		update_profile_form = UserPhotoUpdateForm(instance=user_profile)

	return render(request,
			'management/update_user.html',
			{'update_user_form': update_user_form, 'update_profile_form': update_profile_form}
			)

class CourseAdd(CreateView):
	model = noteDetail
	fields = ['branch','year']

class CourseDelete(DeleteView):
	model = noteDetail
	success_url = reverse_lazy('brmadmin:index')

class SubjectAdd(CreateView):
	model = noteFile
	fields = ('notes','subjectName' )

class SubjectDelete(DeleteView):
	model = noteFile
	success_url = reverse_lazy('brmadmin:index')


def userVerification(request):
	users = UserProfile.objects.filter(Q(department=request.user.userprofile.department)&Q(year=request.user.userprofile.year)&Q(verified=False))
	context = {'users' : users}
	return render(request,'management/userVerification.html',context)

def verify(request,id):
	if request.method == "POST":
		user = User.objects.get(pk=id)
		userprof = UserProfile.objects.get(user=user)
		userprof.verified = True
		user.save()
		userprof.save()
		print(user.username)
		return redirect('brmadmin:userVerification')
	
def userBlock(request):
	# users = User.objects.all()

	users = UserProfile.objects.filter(Q(department=request.user.userprofile.department)&Q(year=request.user.userprofile.year)&Q(verified=True)).exclude(user=request.user)
	context = {'users' : users}
	return render(request,'management/userBlock.html',context)

def block(request,id):
	if request.method == "POST":
		user = User.objects.get(pk=id)
		userprof = UserProfile.objects.get(user=user)
		userprof.verified = False
		user.save()
		userprof.save()
		print(user.userprofile.verified)
		return redirect('brmadmin:userBlock')

def detailSubject(request,id,pk):
	chapter = chapters.objects.filter(Q(subject_id=id))
	context = {'chapters' : chapter , 'usersList' : User.objects.all()}
	return render(request,'management/chapters.html',context)

class chapterAdd(CreateView):
	model = chapters
	fields = ('subject','chapterName','zippedFile','contribAuthor')

class chapterDelete(DeleteView):
	model = chapters
	success_url = reverse_lazy('brmadmin:index')
