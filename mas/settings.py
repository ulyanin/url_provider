# server
DEFAULT_PORT = 3030
DEFAULT_HOST = 'localhost'
DEFAULT_SCHEMA = 'http'
DEFAULT_GET_ADDR = '/get/'

# settings
DEFAULT_RANDOM_KEY_LENGTH = 6

# cassandra
CASSANDRA_HOSTS = (
    'cassandra-seed',  # in docker-compose
)

CASSANDRA_CONNECTION_CONF = {
    'contact_points': CASSANDRA_HOSTS,
    'executor_threads': 8,
}

STATSD_CONF = {
    'host': 'graphite-statsd',
    # 'host': '127.0.0.1',
    'prefix': 'mipt.highload',
}

REDIS_HOST = 'redis'
