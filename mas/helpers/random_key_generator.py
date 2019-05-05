import mas.settings as settings
import string
import random


_letters = string.ascii_letters + string.digits


def random_string(string_length=settings.DEFAULT_RANDOM_KEY_LENGTH):
    """Generates a random string of fixed length """
    return ''.join(random.choices(population=_letters, k=string_length))
