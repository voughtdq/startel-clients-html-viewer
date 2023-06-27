from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from agent.models import ClientPage
from django.http import HttpResponse

class FakePage:
    data = ''
    client_id = ''

class ClientView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('client_id'):
            client_id = kwargs['client_id']
        else:
            client_id = self.request.GET.get('client_id')
        
        if client_id:
            try:
                page = ClientPage.objects.get(client_id=client_id)
                return render(request, 'agent/client.html', {'object': page})
            except:
                pass
        return render(request, 'agent/client.html', {'object': FakePage()})
    
class ClientListView(ListView):
    model = ClientPage
    ordering = ['client_id']