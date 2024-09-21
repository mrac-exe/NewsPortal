from celery import shared_task
import datetime
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Category
from django.core.mail import EmailMultiAlternatives



@shared_task()
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    title = post.post_title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
    html_content = render_to_string(
        'post_created_email.html',
        {
                'text': f'{post.post_title}',
                'Link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()




@shared_task()
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filtere(created_add__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filtere(name__id=categories).values_list('subscribers_email', flat=True,))

    html_content = render_to_string(
        'daily_post.html',
        {
            'Link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статья за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()