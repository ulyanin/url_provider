CREATE KEYSPACE IF NOT EXISTS url_provider
    WITH REPLICATION = {
        'class' : 'SimpleStrategy', 'replication_factor' : 2
    };


CREATE TABLE url_provider.url_to_random_key (
    url TEXT,
    key text,
    PRIMARY KEY (url, key))
WITH CLUSTERING ORDER BY (key DESC);


CREATE TABLE url_provider.key_to_url (
    key TEXT,
    url TEXT,
    operation_id UUID,
    PRIMARY KEY (key)
);


INSERT INTO url_provider.url_to_random_key (url, key)
VALUES ('http://vk.com', 'aaaaa');


INSERT INTO url_provider.key_to_url (url, key, operation_id)
VALUES ('http://vk.com', 'aaaaa', now())


UPDATE url_provider.key_to_url
SET url = 'http://vk.com', operation_id=dac995c9-4cc6-469d-bdcd-ee879a41a0e5 where key='abaca' and operation_id!=dac995c9-4cc6-469d-bdcd-ee879a41a0e5;