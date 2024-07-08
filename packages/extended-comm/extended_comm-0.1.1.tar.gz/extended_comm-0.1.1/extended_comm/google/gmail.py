import logging
from extended_comm.google.service import CreateService
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import dotenv
import mimetypes
from pathlib import Path
from email import encoders

dotenv.load_dotenv()

logging.getLogger('googleapiclient.discovery_cache').setLevel('ERROR')

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

def _create_gmail_api():
    mail = CreateService(api_name='gmail', api_version='v1', scopes=['https://mail.google.com/'])
    return mail


def add_embedded_image(id, file_path: Path):
    with open(file_path, 'rb') as f:
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_main, mime_sub = mime_type.split('/')

        print(mime_main, mime_sub)

        img_base = MIMEImage(f.read(), _subtype=mime_sub)
        img_base.add_header('Content-ID', f'<image{id}>')
        img_base.add_header('Content-Disposition', 'inline', filename=f'{file_path.stem + file_path.suffix}')
        return img_base


def add_attachment(file_path: Path):
    with open(file_path, 'rb') as f:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(f.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename={file_path.stem + file_path.suffix}')
        return mime_base


def send_email(to: list[str], subject: str, body: str = '', attachments: [Path] = [], embedded_images: [Path] = [], **kwargs):
    # TODO: I think I want the api to be explict as possible
    #  add defintion and insist that to, cc, bcc, attachments need to be a list

    msg = MIMEMultipart('related')
    cc = kwargs.get('cc', [])
    bcc = kwargs.get('bcc', [])
    msg['subject'] = subject

    part = MIMEText(body, 'html')
    msg.attach(part)

    recipients = dict(to=to, cc=cc, bcc=bcc)
    for k, v in recipients.items():
        if v:
            emails = [v] if isinstance(v, str) else v
            emails = ', '.join(emails)
            msg[k] = emails

    if isinstance(attachments, Path):
        attachments = [attachments]

    for file in set(attachments):
        msg.attach(add_attachment(file_path=file))

    for idx, file in enumerate(embedded_images):
        msg.attach(add_embedded_image(id=idx, file_path=file))
        print(idx, file)

    raw_body = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    gmail_api = _create_gmail_api()
    gmail_api.users().messages().send(userId='me', body={'raw': raw_body}).execute()
    logging.info(f'Sent "{subject}" to {recipients.get('to')}')
