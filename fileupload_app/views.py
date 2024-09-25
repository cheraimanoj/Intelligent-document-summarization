from django.shortcuts import render, get_object_or_404, redirect
from .forms import DocumentForm
from .models import Document
import os, PyPDF2
from django.conf import settings
from transformers import pipeline


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = DocumentForm()
    return render(request, 'fileupload_app/upload_file.html', {'form': form})

def file_list(request):
    documents = Document.objects.all()
    return render(request, 'fileupload_app/file_list.html', {'documents': documents})

def document_detail(request, slug):
    document = get_object_or_404(Document, slug=slug)
    
    extension = (str(document.uploaded_file)).split('.')[1]

    if extension == 'pdf':
        full_text = extract_text_from_pdf(str(document.uploaded_file))
    else:
        #Convert to pdf
        # LibreOffice command for conversion
        command = [
            libreoffice_path,
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            output_dir,
            file_path
        ]
        try:
            subprocess.run(command, check=True)
            print(f"{file_path} has been converted to PDF.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {file_path}. Error: {e}")
    res = summarise_extract_modal(full_text)

    #print(type(res))
    #print(res)

    context = {
        'title': 'Summarised Content of the uploaded document',
        'summary': res,
        'document': document,
    }

    return render(request, 'fileupload_app/document_detail.html', context)

def extract_text_from_pdf(pdf_path):
    pdf_path = '/app/'+str(settings.MEDIA_URL)+pdf_path
    print(pdf_path)
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    #print(text)
    return text

def summarise_extract_modal(textcontent):
    #from gensim.summarization import summarize
    #from summarizer.sbert import SBertSummarizer
    import torch
    from summarizer.bert import Summarizer
    body = textcontent
    model = Summarizer()
    result = model(body, ratio=0.2)  # Specified with ratio
    result = model(body, num_sentences=3)  # Will return 3 sentences 

    return result

    #summary_ratio = summarize(textcontent, ratio=0.1)
    #summary_ratio = summarizer(textcontent, max_length=500, min_length=25, do_sample=False) 
    #print('Summary====')
    #print(summary_ratio)
    #print('summary end')
