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


CREATE TABLE url_provider.dasha (
    id_person text,
    id_product text,
    PRIMARY KEY (id_person, id_product));

CREATE TABLE test (
    url text,
    key timeuuid,
    data text,
    PRIMARY KEY (url, key)
)
WITH CLUSTERING ORDER BY (key DESC);


INSERT INTO test (url, key, data) VALUES ('vk1', now(), 'datavk1');


CREATE TABLE test2 (
    url text,
    key timeuuid,
    data text,
    PRIMARY KEY ((url, key))
)