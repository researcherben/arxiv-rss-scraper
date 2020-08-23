# scrape the ArXiv RSS and send email alerts

I like alerts for names and keywords


# history of the struggle

DigitalOcean blocks port 25, so this won't work: http://effbot.org/pyfaq/how-do-i-send-mail-from-a-python-script.htm

    server = smtplib.SMTP("localhost")
    server.sendmail("ben", ["ben.is.located@gmail.com"], "hello")

I set up a SendMail account, so this works:

    curl --request POST   --url https://api.sendgrid.com/v3/mail/send   --header "Authorization: Bearer $SENDGRID_API_KEY"   --header 'Content-Type: application/json'   --data '{"personalizations": [{"to": [{"email": "ben.is.located@gmail.com"}]}],"from": {"email": "ben.is.located@gmail.com"},"subject": "Sending with SendGrid is Fun","content": [{"type": "text/plain", "value": "and easy to do anywhere, even with cURL"}]}'

I translated the curl to request using the site https://curl.trillworks.com/#python
