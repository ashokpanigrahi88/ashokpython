import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# put your email here
def sendmail(p_server = "smtp.gmail.com" ,
            p_port = 587,
            p_sender = "noreply.kdwholesalecashncarry@gmail.com",
            p_password = None,
            p_receiver = "ashokoffice@yahoo.co.uk" ,
            p_message = "testing from python",
            p_subject = 'Sending Attachment',
            p_body   = '''Hello,
                This is the body of the email
                sicerely yours
                G.G.
                ''' ,
             p_footer = 'Thanks',
            p_attachdir = None,
            p_attachfile = None):    
    smtp_server = p_server
    port = p_port
    sender = p_sender
    password = p_password
    receiver = p_receiver
    message = p_message
    subject = p_subject
    body = "{}\n\n\n{}".format(p_body,p_footer)
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    if p_attachfile is not None:
        DIR_FILE = p_attachdir
        pdfname = p_attachfile
        filename = "{}{}".format(DIR_FILE,pdfname)  # In same directory as script
        print(filename)
        # open the file in bynary
        binary_pdf = open(filename, 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=pdfname)
        # payload = MIMEBase('application', 'pdf', Name=pdfname)
        payload.set_payload((binary_pdf).read())
        # enconding the binary into base64
        encoders.encode_base64(payload)
        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)

    #use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    #enable security
    session.starttls()

    #login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent to {} {}'.format(receiver,p_attachfile))
