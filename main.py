# import marimo as mo
from gmail_api import init_gmail_service
from gmail_api import _extract_body, send_email, get_email_messages, get_email_message_details

GMAIL_SCOPES = ['https://mail.google.com/']
# GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']

try:
    client_secret = "client_secret.json"

    service = init_gmail_service(client_secret, "gmail", "v1", GMAIL_SCOPES)
    print("Gmail service started")
    # messages = get_email_messages(service, max_results=5)

    # for msg in messages:
    #     details = get_email_message_details(service, msg['id'])
    #     if details:
    #         print(f"Subject: {details['subject']}")
    #         print(f"From: {details['sender']}")
    #         print(f"Recipients: {details['recipients']}")
    #         print(f"Body: {details['body']}...* Print first 100 characters of the body)")
    #         print(f"Snippet: {details['snippet']}")
    #         print(f"Has Attachments: {details['has_attachments']}")
    #         print(f"Date: {details['date']}")
    #         print(f"Star: {details['star']}")
    #         print(f"Label: {details['label']}")
    #         print("*-" * 50)

    try:
        print("Trying to send email")
        to_address = 'baiyewubabawande@gmail.com'
        email_subject = 'lfg'
        email_body = 'Body test of gmail API'
        response = send_email(service, to_address, email_subject, email_body)
        print(response)
        print("Email Sent success")
    except Exception as e:
        print(f'Error sending mail {e}')
except Exception as e:
    print(e)
