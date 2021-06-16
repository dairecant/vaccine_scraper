import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sched, time
from datetime import datetime, timedelta
import re


def web_scraper(age=0,name='',email=''):
    url = 'https://vaccine.hse.ie/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    results=soup.find_all('div',class_='hse-grid-column-two-thirds')



    for result in results:
        p_text=result.find_all('p')

    #scrape html to find age range

    for p in p_text:
        words = str(p.string).split(' ')
        search='age'

        #sarching for sentence with age range
        res = [i for i in words if i.startswith(search)] #contains word aged
        age_range = [int(i.replace(',','')) for i in words if i.replace(',','').isnumeric()] #age demographic

        if(res and age_range):
            if((age >= min(age_range)) and (age <= max(age_range))):
                sender_email="dazzlersdevelopments@gmail.com"
                message = MIMEMultipart("alternative")
                message["Subject"] = "COVID-19 Vaccine Eligibility"
                message["From"] = sender_email
                message["To"] = email

                # Create the plain-text and HTML version of your message
                text = """\
                Hi {name}, you are elligible to be vaccinated against COVID-19.""".format(name=name)
                html = """\
                <html>
                <body>
                    <h2>Hi {name}, you are elligible to be vaccinated against COVID-19.</h2>
                    <p>Visit
                    <a href="{url}">HSE website</a> 
                    to register for your vaccine.
                    </p>
                </body>
                </html>
                """.format(url=url,name=name)
                text_part=MIMEText(text,"plain")
                html_part=MIMEText(html,"html")


                message.attach(text_part)
                message.attach(html_part)
                send_mail(message,email)
            else:
                print('You are not elligble to be vaccinated against COVID-19. You will be notified.')


def send_mail(message,receiver_email):
    #test sending email
    sender_email     = "dazzlersdevelopments@gmail.com" # Enter your address



    port = 465  # For SSL
    password = "CodePortfolio2021!"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        # TODO: Send email here
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            exit()
        except Exception as e:
            print(type(e),e)
            print('login failed')


def check_email(email):
    regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
    if(re.search(regex, email)):
        return True
    else:
        return False

def main():
    name=input("Enter Name: ")

    while True:
        try:
            age=int(input('Enter age:'))
            break
        except Exception as e:
            print(type(e),e)
            print('Type valid numerical age.')

   # while True:
    email=input('Enter Email: ')
     #   if(check_email(email)):
     #       break
     #   else:
       #     print(email+' is an invalid email address. Please Try Again.')


                # Create the plain-text and HTML version of your message
    text = """\
    Hi {name}, testing Google Cloud"""
    text_part=MIMEText(text,"plain")
    message = MIMEMultipart("alternative")
    message.attach(text_part)
    send_mail(message,email)
    while True:
        web_scraper(age,name,email)
        time.sleep(60)

if __name__ == "__main__":
    main()