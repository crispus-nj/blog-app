from app import mail
from flask_mail import Message

def send_mail(email):
    msg = Message('Crispus Blog Mail Subscription', sender='reactnode7@gmail.com', recipients=[email])
    msg.body = f'''You have successfully subscribed to our newsletter. We will notify when new quotes are posted.

Thank You!

To unsubscribe login the application and click unsubscribe.

'''
    mail.send(msg)