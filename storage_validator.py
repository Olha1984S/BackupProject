import config
import constants
import messages

def check_storage():
    if config.STORAGE_TYPE == constants.STORAGE_LOCAL:
        return check_local_storage()

    elif config.STORAGE_TYPE == constants.STORAGE_USB:
        return check_usb_storage()

    elif config.STORAGE_TYPE == constants.STORAGE_NETWORK:
        return check_network_storage()

    return [messages.UNKNOWN_STORAGE_TYPE]


def check_local_storage():
    return []


def check_usb_storage():
    return []


def check_network_storage():
    errors = []

    return errors


