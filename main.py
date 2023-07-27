import time
from datetime import datetime
import logging

import messagebird
import numpy as np
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_menu(nombre, apellido):
    url = "https://sheets.googleapis.com/v4/spreadsheets/1A8nrBoZuTCzcpcOAl3-d3i41-ZFOE9w9i7biwTXaryQ/values/'" + nombre + "%20" + apellido + "'!A1%3AE5"
    api_key = "AIzaSyCD2PkUgZkpn8KNW0_xr_BJOjR-wr3cODM"  # Replace this with your actual Google API Key

    params = {"key": api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx errors
        data = response.json()
        return convert_to_numpy_array(data)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def convert_to_numpy_array(data):
    if not data or "values" not in data:
        return None

    # Extract the values from the data
    values = data["values"]

    # Convert the values to a 2D list and pad rows to have a consistent number of elements
    max_row_length = max(len(row) for row in values)
    data_list = [row + [""] * (max_row_length - len(row)) for row in values]

    # Convert the 2D list to a NumPy array
    np_array = np.array(data_list)
    return np_array


def send_message(msg, number):

    client = messagebird.Client('xkwIEg4lEpGxBZCeXfwSy8w9o')

    try:
        client.message_create(
            '+595982844853',
            number,
            msg,
            {'reference': 'Foobar'}
        )
        logging.info("Message sent successfully!")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


def send_menu_we_ja(we, ja, number):
    send_message(we, number)
    send_message(ja, number)


if __name__ == "__main__":
    while True:
        np_menu_we = get_menu("William", "Eckerleben")
        np_menu_ja = get_menu("Jessica", "Alvarez")
        index = datetime.now().isoweekday()
        date = str(datetime.now().day) + '/' + str(datetime.now().month) + '/' + str(datetime.now().year)

        now = datetime.now()
        logging.info(now)
        # Si son las 07:00 o 09:00 de lunes a viernes, envía el SMS
        if (now.hour == 7 or now.hour == 9) and now.minute == 0:
            if now.isoweekday() < 6:
                panambi_saludo = 'Panambi, acá te dejo mi menú para hoy y en donde lo recibiré.\n\n'
                message_we = date + '\n\n' + panambi_saludo + '+--- WILLIAM ECKERLEBEN ---+\n'
                message_ja = date + '\n\n' + panambi_saludo + '+---- JESSICA ALVAREZ -----+\n'
                for x in np_menu_we[index - 1]:
                    message_we += (x + '\n')
                for x in np_menu_ja[index - 1]:
                    message_ja += (x + '\n')
                send_menu_we_ja(message_we, message_ja, '+595982844853')
                send_menu_we_ja(message_we, message_ja, '+595982620856')
                send_menu_we_ja(message_we, message_ja, '+595971133373')
        # Si son las 19:00 de domingo a jueves, envía el SMS
        if now.hour == 19 and now.minute == 0:
            if now.isoweekday() != 5 and now.isoweekday() != 6:
                panambi_saludo = 'Panambi, acá te dejo mi menú para mañana y en donde lo recibiré.\n\n'
                message_we = date + '\n\n' + panambi_saludo + '+--- WILLIAM ECKERLEBEN ---+\n'
                message_ja = date + '\n\n' + panambi_saludo + '+---- JESSICA ALVAREZ -----+\n'
                for x in np_menu_we[index]:
                    message_we += (x + '\n')
                for x in np_menu_ja[index]:
                    message_ja += (x + '\n')
                send_menu_we_ja(message_we, message_ja, '+595982844853')
                send_menu_we_ja(message_we, message_ja, '+595982620856')
                send_menu_we_ja(message_we, message_ja, '+595971133373')

        # Espera 60 segundos antes de verificar nuevamente
        time.sleep(60)
