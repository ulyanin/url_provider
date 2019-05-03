# server
DEFAULT_PORT = 8000
DEFAULT_HOST = 'localhost'
DEFAULT_SCHEMA = 'http'
DEFAULT_GET_ADDR = '/get/'

# settings
DEFAULT_RANDOM_KEY_LENGTH = 6

# cassandra
CASSANDRA_CONNECTION_CONF = {
    'contact_points': ('localhost',),
    'executor_threads': 8,
}

STATSD_CONF = {
    'host': '127.0.0.1',
    'prefix': 'mipt.highload'
}
