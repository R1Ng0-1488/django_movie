from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку.',
        'Мы будем присылать Вам много спама.',
        'vachpi16@bk.ru',
        [user_email],
        fail_silently=False,
    )
