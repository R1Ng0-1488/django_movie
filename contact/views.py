from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Contact
from .forms import ContactForm
from .service import send
# from .tasks import send_spam_email
# Create your views here.

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('movie:movies')
    template_name = 'contact/tags/form.html'

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        # send_spam_email.delay(form.instance.email)
        return super().form_valid(form)
