from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ParserForm


@login_required 
def parser(request):
    if request.method == 'GET':
        return render(request, 'parser/parser.html', context={'form': ParserForm})

    if request.method == 'POST':
        input_data = request.POST.get('link')

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="output.txt"'
        response.write(input_data)
        return response
