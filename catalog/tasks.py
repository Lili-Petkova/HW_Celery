from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail as django_send_mail

import requests

from .models import Author, Quote


@shared_task
def send_mail(text, email):
    django_send_mail("Reminder", text, 'admin@example.com', [email])


@shared_task
def pars():
    main_page = 'http://quotes.toscrape.com/'
    page = main_page
    counter = 0
    while True:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')
        all_quotes = soup.find_all('div', {'class': 'quote'})
        for item in all_quotes:
            q_text = item.find('span', {'class': 'text'}).text
            if Quote.objects.filter(text=q_text).exists():
                continue
            else:
                about = requests.get(main_page + item.a.get('href'))
                soup_about = BeautifulSoup(about.content, 'html.parser')
                description = soup_about.find('div', {'class': 'author-description'}).text
                author = Author.objects.get_or_create(name=item.small.text, description=description)
                Quote.objects.create(text=q_text, author=author[0])
                counter += 1
            if counter == 5:
                break
        if counter == 5:
            break

        number_of_page = soup.find('li', {'class': 'next'})
        if number_of_page:
            next_url = number_of_page.a.get('href')
            page = main_page + next_url
        else:
            text = "All quotes are over. It's time to add new ones."
            django_send_mail('Notice', text, 'admin@example.com', ['writer@example.com'])
