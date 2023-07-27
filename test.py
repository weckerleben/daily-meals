import logging

import messagebird


def send_message():
    client = messagebird.Client('xkwIEg4lEpGxBZCeXfwSy8w9o')

    try:
        client.message_create(
            'William Eckerleben',
            '+595982844853',
            'This is a test message3',
            {'reference': 'Foobar'}
        )
        logging.info("WhatsApp message sent successfully!")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


if __name__ == "__main__":
    send_message()
