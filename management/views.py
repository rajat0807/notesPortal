from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate , login , logout
from .models import noteDetail,noteFile,UserProfile,chapters,Image
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.views.generic.edit import FormView

from django.shortcuts import render
from management.forms import UserForm,UserProfileForm,UserPhotoUpdateForm,UserForm2,AddCourseForm,AddSubjectForm,FileFieldForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.db.models import Q

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class branchAndYear(generic.ListView):

	template_name = 'management/test.html'

	def get_context_data(self, **kwargs):
		context = super(branchAndYear, self).get_context_data(**kwargs)
		try:
			context['usersList'] = UserProfile.objects.filter(Q(department=self.request.user.userprofile.department)&Q(year=self.request.user.userprofile.year)&Q(verified=False))
		except:
			pass
		return context

	def get_queryset(self):
		return noteDetail.objects.all()


class detailsBranchAndYear(generic.DetailView):
	model = noteDetail
	def get_context_data(self, **kwargs):
		context = super(detailsBranchAndYear, self).get_context_data(**kwargs)
		try:
			context['usersList'] = UserProfile.objects.filter(Q(department=self.request.user.userprofile.department)&Q(year=self.request.user.userprofile.year)&Q(verified=False))
		except:
			pass
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
			print(user.username + " " + str(user.userprofile.verified))
			if user.userprofile.verified is False:
				return render(request,'management/signIn.html',{'error' : 'Sorry, you are blocked!'})
			else:
				login(request,user)
				if user.is_superuser is False:
					course = noteDetail.objects.get(Q(branch=user.userprofile.department)&Q(year=user.userprofile.year))
					return redirect('brmadmin:detail',pk = course.id)
				else:
					return redirect('brmadmin:index')
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
			if user_form.cleaned_data['password'] == user_form.cleaned_data['confirm_password']:
				user.set_password(user.password)
			else:
				return render(request,'management/regForm.html',{'user_form' : user_form,'profile_form': profile_form,'error' : 'Please use the same password'})
			
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
			temp = profile.picture
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			file_type = profile.picture.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				profile.picture = temp
				return render(request,'management/update_user.html',{'update_user_form': update_user_form, 'update_profile_form': update_profile_form,'error' : 'Not a supported image format'})

			profile.save()
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
	fields = ('subjectName',)

	def form_valid(self, form):
		form.instance.notes = noteDetail.objects.get(Q(branch=self.request.user.userprofile.department)&Q(year=self.request.user.userprofile.year))	
		return super(SubjectAdd	, self).form_valid(form)

class SubjectDelete(DeleteView):
	model = noteFile
	def get_success_url(self):
		subject = noteFile.objects.get(pk=self.kwargs['pk'])
		return reverse_lazy( 'brmadmin:detail',
		kwargs = {'pk': subject.notes.id},)


class CourseDelete(DeleteView):
	model = noteDetail
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
	subject = noteFile.objects.get(pk=pk)
	chapter = chapters.objects.filter(subject=subject)
	pk_id = pk
	context = {'chapters' : chapter , 'usersList' : User.objects.all(), 'subject_id' : pk_id}
	return render(request,'management/chapters.html',context)

class chapterAdd(CreateView):
	model = chapters
	fields = ('chapterName','contribAuthor')
	def form_valid(self, form):
		form.instance.subject = noteFile.objects.get(pk=self.kwargs['id'])
		return super(chapterAdd	, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(chapterAdd, self).get_context_data(**kwargs)
		context['subject_id'] = self.kwargs['id']
		return context



def chapterDelete(request,id,pk):
	subject = noteFile.objects.get(pk=id)
	chapter = chapters.objects.get(Q(subject=subject)&Q(pk=pk))
	chapter.delete()
	return redirect('brmadmin:detailSubject',id=subject.notes.id,pk=id)

def home(request):
	user = User.objects.get(username=request.user.username)
	userprofile = UserProfile.objects.get(user=user)
	if request.user.is_superuser:
		return redirect('brmadmin:index')
	else:
		no = noteDetail.objects.get(Q(branch=user.userprofile.department)&Q(year=user.userprofile.year)).id
		return redirect('brmadmin:detail',pk=no)

def photos(request,id,pk,pk_i):
	chapter = chapters.objects.get(pk=pk_i)
	photo = Image.objects.filter(chapter=chapter)
	id_no = chapters.objects.get(pk=pk_i)
	context = {'photos' : photo, 'usersList' : User.objects.all(),'i' : id_no}
	return render(request,'management/photos.html',context)


class FileFieldView(FormView):
	form_class = FileFieldForm
	template_name = 'management/uploadImages.html'

	def get_context_data(self, **kwargs):
		context = super(FileFieldView, self).get_context_data(**kwargs)
		context['i'] = chapters.objects.get(pk=self.kwargs['pk_i'])
		return context

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		count = 0
		form = self.get_form(form_class)
		files = request.FILES.getlist('images')
		if form.is_valid():
			for f in files:
				image = Image()
				image.chapter = chapters.objects.get(pk=self.kwargs['pk_i'])
				image.picture = f
				file_type = image.picture.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in IMAGE_FILE_TYPES:
					print("Hii")
				else:
					image.save()
			return redirect('brmadmin:photos',id=self.kwargs['id'],pk=self.kwargs['pk'],pk_i=self.kwargs['pk_i'])
		else:
			return self.form_invalid(form)

def imageDelete(request,id,pk):
	image = Image.objects.get(pk=pk)
	chapter = chapters.objects.get(pk=id)
	image.delete()
	return redirect('brmadmin:photos',id=chapter.subject.notes.id,pk=chapter.subject.id,pk_i=chapter.id)

def Search(request):
	if request.method=='GET':
		key=request.GET['q']
		if key == "":
			context = None
		else:
			context = {'keys' : UserProfile.objects.filter(Q(user__username__icontains=key)&Q(department=request.user.userprofile.department)&Q(year=request.user.userprofile.year)&Q(verified=True)).exclude(user=request.user)}
		return render(request,'management/search.html',context)

def deleteUser(request,id):
	if request.method == "POST":
		user = User.objects.get(pk=id)
		user.delete()
		try:
			if request.POST['verify']:
				return redirect('brmadmin:userVerification')
		except:
			return redirect('brmadmin:userBlock')