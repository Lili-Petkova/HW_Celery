from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail as django_send_mail

import requests

from .models import Author, Quote


@shared_task
def send_mail(text, email):
    django_send_mail("Reminder", text, 'admin@example.com', [email])


def pars():
    page = 'http://quotes.toscrape.com/'
    list_page = [page]
    for p in list_page:
        r = requests.get(p)
        soup = BeautifulSoup(r.content, 'html.parser')
        string = soup.find_all('div', {'class': 'quote'})
        counter_for_new = 0
        get_counter = 0
        for item in string:
            about = requests.get('http://quotes.toscrape.com/' + item.a.get('href'))
            soup_about = BeautifulSoup(about.content, 'html.parser')
            description = soup_about.find('div', {'class': 'author-description'}).text
            author = Author.objects.get_or_create(name=item.small.text, description=description)
            quote = item.find('span', {'class': 'text'}).text
            try:
                Quote.objects.get(text=quote)
                get_counter += 1
            except:
                """author[0] is name of author"""
                Quote.objects.create(text=quote, author=author[0])
                counter_for_new += 1
                if counter_for_new == 5:
                    break
        if get_counter == 10:
            try:
                """create url for next page"""
                nex = soup.find('li', {'class': 'next'}).a.get('href')
                list_page.append(page + nex)
            except:
                text = "All quotes are over. It's time to add new ones."
                django_send_mail('Notice', text, 'admin@example.com', ['writer@example.com'])


def non():
    django_send_mail("Reminder", 'всё нормально', 'admin@example.com', ['email@example.com'])
