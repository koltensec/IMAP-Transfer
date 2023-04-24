import imaplib
import email
from email.message import EmailMessage

def transfer_emails(yandex_email, yandex_password, cpanel_email, cpanel_password, folder_name):

    yandex_imap = imaplib.IMAP4_SSL("imap.yandex.com")
    yandex_imap.login(yandex_email, yandex_password)


    cpanel_imap = imaplib.IMAP4_SSL("IP OR DOMAIN")
    cpanel_imap.login(cpanel_email, cpanel_password)


    yandex_imap.select(folder_name)
    typ, data = yandex_imap.search(None, "ALL")
    mail_ids = data[0].split()


    for mail_id in mail_ids:
        typ, message_data = yandex_imap.fetch(mail_id, "(RFC822 FLAGS)")
        raw_email = message_data[0][1]
        msg = email.message_from_bytes(raw_email)


        flags = message_data[0][0].decode("utf-8").split()
        keywords = [flag for flag in flags if flag.startswith("\\")]
        if keywords:
            msg["X-Keywords"] = ",".join(keywords)

        cpanel_imap.append(folder_name, "", imaplib.Time2Internaldate(email.utils.parsedate(msg["date"])), msg.as_bytes())


    yandex_imap.logout()
    cpanel_imap.logout()


with open("credentials.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    email_address, password = line.strip().split(":")


    try:
        transfer_emails(email_address, password, email_address, password, "inbox")
        transfer_emails(email_address, password, email_address, password, "Sent")
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{email_address}: Successful\n")
    except Exception as e:
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{email_address}: Unsuccessful ({e})\n")
