import os
import subprocess
import tempfile
from django.db import models
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
#from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify

class Document(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    uploaded_file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check the file extension
        _, extension = os.path.splitext(self.uploaded_file.name)

        if extension.lower() != '.pdf':
            # Convert to PDF using LibreOffice
            self.uploaded_file = self.convert_to_pdf(self.uploaded_file)
        
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Document.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def convert_to_pdf(self, uploaded_file):
        """
        Converts the uploaded file to PDF using LibreOffice.
        """
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings

        data = uploaded_file # or self.files['image'] in your form
        f_name = 'tmp/'+str(uploaded_file)

        path = default_storage.save(f_name, ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        out_tmp_file = os.path.join(settings.MEDIA_ROOT, 'pdf/')

        print('asdasdasddasd',out_tmp_file,tmp_file)
  
        '''
        try:
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # For in-memory files, write the content to a temporary file
                temp_input_file = tempfile.NamedTemporaryFile(delete=False)
                for chunk in uploaded_file.chunks():
                    temp_input_file.write(chunk)
                temp_input_file.close()
                input_file_path = temp_input_file.name
                print('$$$$$$$$$$$$$$')
                print(uploaded_file)
            elif isinstance(uploaded_file, TemporaryUploadedFile):
                print('#############')
                print(uploaded_file)
                # For large files, use the path directly
                input_file_path = uploaded_file.temporary_file_path()
            else:
                print('ELSE#############')
                print(uploaded_file)
                # Fallback in case of an unexpected file type
                raise ValueError("Unsupported file type for conversion.")
            '''
        # Use LibreOffice to convert the file
        print('OUTPUT++++++++++++++++')
        print(out_tmp_file)
        command = [
            'libreoffice',
            '--headless',  # Run in headless mode to avoid GUI
            '--convert-to', 'pdf',  # Convert to PDF
            '--outdir', out_tmp_file,  # Output directory
            tmp_file  # Path to the uploaded file
        ]

        subprocess.run(command, check=True)
        '''
        # Load the converted file into Django
        with open(temp_pdf.name, 'rb') as pdf_file:
            converted_pdf = File(pdf_file)
            new_pdf_name = f"{os.path.splitext(uploaded_file.name)[0]}.pdf"
            return InMemoryUploadedFile(
                file=converted_pdf,
                field_name=None,
                name=new_pdf_name,
                content_type='application/pdf',
                size=os.path.getsize(temp_pdf.name),
                charset=None,
            )
        '''
        '''
        finally:
            # Ensure the temporary files are deleted after use
            os.remove(temp_pdf.name)
            if isinstance(uploaded_file, InMemoryUploadedFile):
                os.remove(input_file_path)
        '''

    def __str__(self):
        return self.title



'''
from django.db import models
from django.utils.text import slugify

class Document(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    uploaded_file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Document.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
'''