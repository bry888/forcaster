from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import LinkForm

from .format_category_to_dfp2 import convert_urls_for_dfp

# Create your views here.
def index(request):
    input_links = ''

    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():

            # parse links in my converter FUNCTION
            input_links = form.cleaned_data['input_links']
            query_result, error = convert_urls_for_dfp(input_links)

            return render(request, 'converter/output.html', {'form':form, 'input_links':input_links, 'query_result':query_result, 'error':error})
                                                                    # zmienna formularz, zmienna pamięć searhca, zmienna wynik konwersji


    else:
        #invalid data
        form = LinkForm(initial={'input_links': input_links})

    return render(request, 'converter/index.html', {'form':form})
