from base64 import urlsafe_b64encode
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type as guess_mime_type
from os import path
from typing import Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource

from core.config import config


class GmailHelper:
    @staticmethod
    def authenticate() -> Resource:
        scopes = ["https://mail.google.com/"]
        try:
            if not path.exists(config.GMAIL_TOKEN_PATH):
                raise Exception("Token does not exist!")
            creds = Credentials.from_authorized_user_file(config.GMAIL_TOKEN_PATH, scopes)

            if not creds.valid:
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open(config.GMAIL_TOKEN_PATH, "wt") as token:
                        token.write(creds.to_json())
                else:
                    raise Exception("Token is invalid and refresh failed!")

            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            print(e)

    @staticmethod
    def add_attachment(message: Union[MIMEText, MIMEMultipart], filename: str) -> None:
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        main_type, sub_type = content_type.split("/", 1)
        if main_type == "text":
            fp = open(filename, "rb")
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == "image":
            fp = open(filename, "rb")
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == "audio":
            fp = open(filename, "rb")
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, "rb")
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        filename = path.basename(filename)
        msg.add_header(_name="Content-Disposition", _value="attachment", filename=filename)
        message.attach(msg)

    @staticmethod
    def build_message(source: str, destination: str, subject: str, body: str, attachments=None) -> dict:
        if attachments is None:
            attachments = []
        if not attachments:
            message = MIMEText(_text=body, _subtype="HTML", _charset="UTF-8")
            message["to"] = destination
            message["from"] = source
            message["subject"] = subject
        else:
            message = MIMEMultipart()
            message["to"] = destination
            message["from"] = source
            message["subject"] = subject
            message.attach(MIMEText(_text=body, _subtype="HTML", _charset="UTF-8"))
            for filename in attachments:
                GmailHelper.add_attachment(message=message, filename=filename)
        return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}

    @staticmethod
    def send_message(destination: str, subject: str, body: str, attachments=None) -> None:
        if attachments is None:
            attachments = []
        try:
            service = GmailHelper.authenticate()
            source = config.AMDIN_GMAIL
            result = (
                service.users()
                .messages()
                .send(
                    userId="me",
                    body=GmailHelper.build_message(
                        source=source, destination=destination, subject=subject, body=body, attachments=attachments
                    ),
                )
                .execute()
            )
            if result["labelIds"][0] != "SENT":
                raise Exception("Failed to send mail.")
        except Exception as e:
            print(e)
