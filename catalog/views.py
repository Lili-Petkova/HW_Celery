import datetime

from django.shortcuts import render
from django.utils import timezone

from .forms import EmailForm
from .tasks import send_mail


def send_reminder(request):
    if request.method == 'POST':
        reminder = EmailForm(data=request.POST)
        if reminder.is_valid():
            email = reminder.cleaned_data['email']
            text = reminder.cleaned_data['text']
            data = reminder.cleaned_data['datetime']
            today_now = timezone.now()
            if today_now < data < today_now + datetime.timedelta(days=2):
                message = "Reminder has sent successfully!"
                send_mail.apply_async((text, email), eta=data)
                return render(
                    request,
                    'catalog/reminder.html',
                    {
                        'reminder_form': reminder,
                        'message': message,

                    }
                )
    else:
        reminder = EmailForm()
    return render(
        request,
        'catalog/reminder.html',
        {
            'reminder': reminder,
        }
    )
