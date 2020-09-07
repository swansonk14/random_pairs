"""Emails each pair of people in a pairing."""
import os

from fire import Fire
import pandas as pd

from gmail_send import build_service, create_message, send_message


def email_pairs(pairings_dir: str,
                pairing_num: int,
                my_name: str,
                my_email: str = None,
                subject_prefix: str = 'Pairing',
                token_path: str = 'token.pickle',
                credentials_path: str = 'credentials.json'):
    """Emails each pair of people in a pairing."""
    # Load pairing
    pairing = pd.read_csv(os.path.join(pairings_dir, f'pairing_{i}.csv'))

    # Check unique emails
    unique_emails = set(pairing['email_1']) | set(pairing['email_2'])

    if len(unique_emails) != len(pairing):
        raise ValueError('Emails are not unique.')

    # Create subject
    subject = f'{subject_prefix} {pairing_num}'

    # Build email messages
    messages = []
    for name_1, email_1, name_2, email_2 in pairing.itertuples(index=False):
        # Check names and emails are None at the same time
        if (name_1 is None) != (email_1 is None) or (name_2 is None) != (email_2 is None):
            raise ValueError()

        # If both are None, continue
        if name_1 is None and name_2 is None:
            continue

        # If one is None, create unpaired message
        elif name_1 is None or name_2 is None:
            name = name_1 if name_1 is not None else name_2
            email = email_1 if email_1 is not None else email_2

            messages.append(create_message(
                to=email,
                subject=subject,
                message_text=f'Hi {name},\n'
                             f'\n'
                             f'Unfortunately you do not have a partner this week. '
                             f'But don\'t worry, you\'ll be paired with someone next week!\n'
                             f'\n'
                             f'Best,\n'
                             f'{my_name}'
            ))

        # If neither is none and one is me, send special paired message
        elif email_1 == my_email or email_2 == my_email:
            name, email = (name_1, email_1) if email_1 != my_email else (name_2, email_2)

            messages.append(create_message(
                to=email,
                subject=subject,
                message_text=f'Hi {name},\n'
                             f'\n'
                             f'You\'re paired with me this week! '
                             f'When would be a good time to chat?\n'
                             f'\n'
                             f'Best,\n'
                             f'{my_name}'
            ))

        # If neither is none and neither is me, send paired message
        else:
            messages.append(create_message(
                to=f'{email_1},{email_2}',
                subject=subject,
                message_text=f'Hi {name_1} and {name_2},\n'
                             f'\n'
                             f'You two are paired this week! '
                             f'Please try to find a time by the end of the week to meet.\n'
                             f'Best,\n'
                             f'\n'
                             f'{my_name}'
            ))

    # Load Gmail service
    service = build_service(token_path=token_path, credentials_path=credentials_path)

    # # Send emails
    # for message in messages:
    #     send_message(service=service, message=message)


if __name__ == '__main__':
    Fire(email_pairs)
