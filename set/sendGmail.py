import smtplib

gmail_user = "jaded.it@gmail.com"
gmail_password = "is43m\@ilth"

sent_from = gmail_user
to = ['jaded.iwork@gmail.com']
subject = 'OMG Super Important Message'
body = "Hey, what's up?\n\n- You"

email_text = """\
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    #server = smtplib.SMTP('smtp.gmail.com:587')
    server = smtplib.SMTP_SSL("smtp.gmail.com:465")
    server.ehlo()
    #server.starttls()
    server.ehlo()
    #server.login(gmail_user, gmail_password)
    #server.sendmail(sent_from, to, email_text)
    #server.close()

    print("Email sent!")

except:
    print("Something went wrong...")