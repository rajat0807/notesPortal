from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class noteDetail(models.Model):
	BRANCH = (
		('CSE' , 'CSE'),
		('ECE' , 'ECE'),
		('EEE' , 'EEE'),
		('ME' , 'ME'),
		('MME' , 'MME'),
		('Chem' , 'ChE'),
		('Civil' , 'Civil')
	)
	

	branch = models.CharField(max_length=5,choices=BRANCH)
	YEAR = (
		('1' , 'First'),
		('2' , 'Second'),
		('3' , 'Third'),
		('4' , 'Fourth'),
	)
	

	year = models.CharField(max_length=1,choices=YEAR)

	def get_absolute_url(self):
		return reverse('brmadmin:detail' , kwargs = {'pk' : self.pk})

	def __str__(self):
		return self.branch + self.year


class noteFile(models.Model):
	notes = models.ForeignKey(noteDetail,on_delete=models.CASCADE)
	subjectName = models.CharField(max_length=50)

	def get_absolute_url(self):
		return reverse('brmadmin:detailSubject',kwargs={'id':self.notes.pk,'pk':self.pk})

	def __str__(self):
		return self.subjectName + " - " + self.notes.branch + self.notes.year


class chapters(models.Model):
	subject = models.ForeignKey(noteFile,on_delete=models.CASCADE)
	zippedFile = models.FileField(upload_to='uploads/')
	chapterName = models.CharField(max_length=50)
	contribAuthor = models.CharField(max_length=50)

	def get_absolute_url(self):
		return reverse('brmadmin:detailSubject',kwargs={'id':self.subject.notes.pk,'pk':self.subject.pk})

	def __str__(self):
		return self.chapterName + self.subject.subjectName

class Image(models.Model):
	chapter = models.ForeignKey(chapters,on_delete=models.CASCADE)
	picture = models.FileField(upload_to='chapter_images/')

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	BRANCH = (
		('CSE' , 'CSE'),
		('ECE' , 'ECE'),
		('EEE' , 'EEE'),
		('ME' , 'ME'),
		('MME' , 'MME'),
		('Chem' , 'ChE'),
		('Civil' , 'Civil')
	)
	
	department = models.CharField(max_length=5,choices=BRANCH)
	YEAR = (	
		('1' , 'First'),
		('2' , 'Second'),
		('3' , 'Third'),
		('4' , 'Fourth'),
	)

	picture = models.ImageField(upload_to='profile_pictures',default='default_pic.jpg')
	
	verified = models.BooleanField(default=False)

	isAdmin = models.BooleanField(default=False)

	year = models.CharField(max_length=1,choices=YEAR)
	
	def __unicode__(self):
		return self.user.department

	def __str__(self):
		return self.user.username

