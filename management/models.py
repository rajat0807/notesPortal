from django.db import models
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from PIL import Image as Img
import io

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
	picThumbnail = models.ImageField(upload_to='thumbnails/')
	picture = models.ImageField(upload_to='chapter_images/')
	def save(self, *args, **kwargs):
		if self.picture:
			img = Img.open(self.picture)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			new_width = 300
			img.thumbnail((new_width, new_width * self.picture.height / self.picture.width), Img.ANTIALIAS)
			output = io.BytesIO()
			img.save(output, format='JPEG', quality=70)
			output.seek(0)
			self.picThumbnail= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.picture.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
		super(Image, self).save(*args, **kwargs)


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

