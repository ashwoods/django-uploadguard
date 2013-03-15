import os
import json

from resumable.views import ResumableUploadView
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from resumable.files import ResumableFile
from django.http import HttpResponse
import unidecode as u

from submitz.apps.unchained.projects.models import Project
from submitz.apps.unchained.entries.models import Entry
from submitz.apps.unchained.simpleasset.models import SimpleAsset
from submitz.apps.unchained.simpleasset import helpers as h
import  submitz.apps.unchained.projects.tasks as tasks
from submitz.apps.submitto.mitto.models import EntryAsset

from django.views.decorators.csrf import csrf_exempt, csrf_protect

class UserResumableUploadView(ResumableUploadView):

    def get(self, *args, **kwargs):
        """Checks if chunk has allready been sended.
        """
        r = ResumableFile(self.storage, self.request.GET)
        if not (r.chunk_exists or r.is_complete):
            return HttpResponse('chunk not found', status=404)
        if r.is_complete:
            message=self.process_file(r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(message)
        return HttpResponse('chunk already exists')

    @property
    def chunks_dir(self):
        chunks_dir = getattr(settings, 'FILE_UPLOAD_TEMP_DIR', None)
        if not chunks_dir:
            raise ImproperlyConfigured(
                'You must set settings.FILE_UPLOAD_TEMP_DIR')

        user_chunks_dir = os.path.join(chunks_dir, self.request.user.username)

        if not os.path.exists(user_chunks_dir):
            os.makedirs(user_chunks_dir)
        return user_chunks_dir


    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserResumableUploadView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Saves chunks then checks if the file is complete."""

        message=""


        uploader = self.request.POST.get('uploader',None)
        if uploader == 'plupload':
            message = self.handle_plupload_post(*args, **kwargs)
        else:
            chunk = self.request.FILES.get('file')
            r = ResumableFile(self.storage, self.request.POST)
            if r.chunk_exists:
                if r.is_complete:
                    message = self.process_file(r.filename, r.file)
                    r.delete_chunks()
                    return HttpResponse(message)
                else:
                    return HttpResponse('chunk already exists new')
            r.process_chunk(chunk)


            if r.is_complete:
                message = self.process_file(r.filename, r.file)
                r.delete_chunks()
        return HttpResponse(message)

    def handle_plupload_post(self, *args, **kwargs):
    	"""Handles plupload post request"""
        request = self.request
        uploaded_file = request.FILES['file']
        chunk = request.REQUEST.get('chunk', '0')
        chunks = request.REQUEST.get('chunks', '0')
        name = u.unidecode(request.REQUEST.get('name', ''))

        if not name:
            name = uploaded_file.name

        temp_file = os.path.join(self.storage.location, name)
        with open(temp_file, ('wb' if chunk == '0' else 'ab')) as f:
            for content in uploaded_file.chunks():
                f.write(content)

        if int(chunk) + 1 >= int(chunks):
               return self.process_file(name)


    def process_file(self, filename, file=None):
            """Process the complete file.
            """
            if file:
                self.storage.save(filename, file)