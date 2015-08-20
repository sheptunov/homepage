# -*- coding: utf-8 -*-
from django.db import models
from PIL import Image, ImageOps
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import os

class Project(models.Model):
    title = models.CharField(max_length=100, help_text="Title", blank=False)
    slug = models.SlugField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length=5000, blank=False)
    date_created = models.DateTimeField(auto_now=True, help_text="Creation Date")
    order = models.IntegerField(blank=True, default=1)

    class Meta():
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __unicode__(self):
            return "%s" % self.title

    def get_images(self):
        try:
            return get_list_or_404(Entity, gallery=self.id)
        except IndexError:
            pass

    def get_cover(self):
        try:
            return get_list_or_404(Entity, gallery=self.id)[0]
        except IndexError:
            pass

    def get_month(self):
        try:
            return self.date_created.strftime("%B")
        except:
            raise(BaseException, ("Can't get PROJECT.get_month"))

    def get_previous(self):
        '''
        Return the previous published portfolio.
        '''
        try:
            print(self.get_previous_by_date_created(pk__lt=self.id))
            return self.get_previous_by_date_created(pk__lt=self.id)
        except ObjectDoesNotExist:
            print("abnormal")
            return Project.objects.last()

    def get_next(self):
        '''
        Return the next published portfolio.
        '''
        try:
            return self.get_next_by_date_created(pk__gt=self.id)
        except ObjectDoesNotExist:
            return Project.objects.first()

    def get_ids(self):
        '''
        Return object.id in queryset
        '''
        projects = get_list_or_404(Project)




class Entity(models.Model):
    gallery = models.ForeignKey(Project, verbose_name="+")
    title = models.CharField(max_length=500, blank=True)
    image = models.ImageField(verbose_name='Image', blank=False)
    thumbnail = models.ImageField(verbose_name='Thumbnail', blank=True, null=True)
    order = models.IntegerField(blank=True, default=1)


    class Meta():
        verbose_name_plural = "Images"
        verbose_name = "Image"
        def __unicode__(self):
            return self.title

    def create_thumbnail(self):
        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (460,460)
        print self.image
        MIME_TYPE = "image/%s" % os.path.splitext(self.image.name)[1].replace(".", '')
        if MIME_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif MIME_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))
        image = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read())
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self):
        # create a thumbnail
        self.create_thumbnail()
        super(Entity, self).save()


class Message(models.Model):
    author = models.CharField(max_length=255, help_text="Author")
    email = models.EmailField(blank=True, null=True, help_text="Email")
    message = models.CharField(max_length=255, help_text="Message")
    date_created = models.DateTimeField(auto_now=True, help_text="Creation Date")
    class Meta():
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        def __unicode__(self):
            return self.author