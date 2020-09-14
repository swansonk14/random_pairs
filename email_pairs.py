"""Emails each pair of people in a pairing."""
import os

from fire import Fire
import pandas as pd

from gmail import build_service, create_message, send_message


def email_pairs(pairings_dir: str,
                pairing_num: int,
                sender_name: str,
                my_email: str = None,
                subject_prefix: str = 'Pairing',
                token_path: str = 'token.pickle',
                credentials_path: str = 'credentials.json') -> None:
    """
    Emails each pair of people in a pairing.

    :param pairings_dir: Path to a directory where the random pairings are saved.
    :param pairing_num: The number of the pairing to send.
    :param sender_name: The name of the sender, which is the name signed at the bottom of the email.
    :param my_email: The email of the sender if the sender is a participant in the pairing.
    :param subject_prefix: The prefix used in the subject header, followed by pairing_num.
    :param token_path: Path to user token .pickle file. If it doesn't already exist,
                       it will be saved here.
    :param credentials_path: Path to credentials .json file.
    """
    # Load pairing
    pairing = pd.read_csv(os.path.join(pairings_dir, f'pairing_{pairing_num}.csv'))

    # Convert NaN to None
    pairing = pairing.where(pairing.notna(), None)

    # Create subject
    subject = f'{subject_prefix.strip()} {pairing_num}'

    # Build email messages
    messages = []
    for name_1, email_1, name_2, email_2 in pairing.itertuples(index=False):
        # Check names and emails are None at the same time
        if (name_1 is None) != (email_1 is None) or (name_2 is None) != (email_2 is None):
            raise ValueError('Names and emails are not None at the same time.')

        # If both are None, continue
        if name_1 is None and name_2 is None:
            continue

        # If one is None, create unpaired message
        elif name_1 is None or name_2 is None:
            name = name_1 if name_1 is not None else name_2
            to = email_1 if email_1 is not None else email_2
            message_text = (f'Hi {name},\n'
                            f'\n'
                            f'Unfortunately you don\'t have a partner this week. '
                            f'But don\'t worry, you\'ll have a partner again next week!\n'
                            f'\n'
                            f'Best,\n'
                            f'{sender_name}')

        # If neither is none and one is me, send special paired message
        elif email_1 == my_email or email_2 == my_email:
            name, to = (name_1, email_1) if email_1 != my_email else (name_2, email_2)
            message_text = (f'Hi {name},\n'
                            f'\n'
                            f'You\'re paired with me this week! '
                            f'When would be a good time to chat?\n'
                            f'\n'
                            f'Best,\n'
                            f'{sender_name}')

        # If neither is none and neither is me, send paired message
        else:
            to = f'{email_1},{email_2}'
            message_text = (f'Hi {name_1} and {name_2},\n'
                            f'\n'
                            f'You two are paired this week! '
                            f'Please try to find a time by the end of the week to chat.\n'
                            f'\n'
                            f'Best,\n'
                            f'{sender_name}')

        print(f'Email {len(messages) + 1}\n'
              f'To: {to}\n'
              f'Subject: {subject}\n\n'
              f'{message_text}\n')

        messages.append(create_message(
            to=to,
            subject=subject,
            message_text=message_text
        ))

    # Check whether to send the emails
    if input(f'Would you like to send these {len(messages):,} emails? Y/n: ').lower() != 'y':
        print('Not sending emails')
        return

    # Load Gmail service
    print('Building Gmail service')
    service = build_service(token_path=token_path, credentials_path=credentials_path)

    # Send emails
    print('Sending emails')
    for i, message in enumerate(messages):
        message = send_message(service=service, message=message)
        print(f'Message {i} Id: {message["id"]}')


if __name__ == '__main__':
    Fire(email_pairs)
