import argparse
import json
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main(args) -> int:
    if args.recipients_path is not None:
        # load json as a list
        with open(args.recipients_path, 'r') as f:
            recipients = json.load(f)
        email_recipients = ', '.join(recipients)
    else:
        email_recipients = args.recipient
    # Create a message
    message = MIMEMultipart()
    message['From'] = args.sender
    message['Subject'] = args.subject
    message['To'] = email_recipients
    if args.body_path is not None:
        with open(args.body_path, 'r') as f:
            body = f.read()
    else:
        body = ''
    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))
    # Connect to the SMTP server
    with smtplib.SMTP(args.smtp_host, args.smtp_port) as server:
        server.starttls()
        server.login(args.sender, args.password)
        server.send_message(msg=message)
    print('An email has been sent.')
    return 0


def setup_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--smtp_host',
        help='IP or domain name of the server.',
        type=str,
        required=True)
    parser.add_argument(
        '--smtp_port',
        help='Port number of the server.',
        type=int,
        required=True)
    parser.add_argument(
        '--sender',
        help='Address of the sender.',
        type=str,
        required=True)
    parser.add_argument(
        '--password', help='Password of the sender.', type=str, required=True)
    parser.add_argument(
        '--recipients_path',
        help='Path to a json file for address list of the recipients.',
        type=str)
    parser.add_argument(
        '--recipient',
        help='Email address of only one recipient. ' +
             'Valid when recipients_path is None.',
        type=str)
    # Subject, body
    parser.add_argument(
        '--subject', help='Subject of the email.', type=str, required=True)
    parser.add_argument(
        '--body_path',
        help='Path to a txt file, which is the body of email.',
        type=str,
        required=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = setup_parser()
    ret_val = main(args)
    sys.exit(ret_val)
