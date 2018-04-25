from django.shortcuts import render

# Create your views here.
def deneme(request):
	return render(request, 'index.html')
