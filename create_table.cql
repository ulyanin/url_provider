CREATE KEYSPACE IF NOT EXISTS url_provider
    WITH REPLICATION = {
        'class' : 'SimpleStrategy', 'replication_factor' : 2
    };


CREATE TABLE url_provider.url_to_random_key (
    url TEXT,
    key text,
    PRIMARY KEY (url, key))
WITH CLUSTERING ORDER BY (key DESC);

-- CREATE TABLE url_provider.url_to_key (
--     url TEXT,
--     key TEXT,
--     PRIMARY KEY (url, key))
-- WITH CLUSTERING ORDER BY (key DESC);

CREATE TABLE url_provider.key_to_url (
    key TEXT,
    url TEXT,
    PRIMARY KEY (key)
);

INSERT INTO url_provider.url_to_random_key (url, key)
VALUES ('http://vk.com', now());



