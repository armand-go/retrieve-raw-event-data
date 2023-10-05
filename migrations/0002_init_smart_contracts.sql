SET ROLE postgres;

CREATE TABLE data.smart_contract (
    event_id INT REFERENCES data.events(event_id) ON DELETE CASCADE,
    collection_name VARCHAR NOT NULL,
    crowdsale VARCHAR NOT NULL,
    collection_address VARCHAR NOT NULL,
    multisig VARCHAR NOT NULL,
    is_presale BOOLEAN NOT NULL,
    metadata_list VARCHAR[] NOT NULL,
    price_per_token INT NOT NULL,
    max_mint_per_user INT NOT NULL,
    sale_size INT NOT NULL,
    sale_currency JSON NOT NULL,
    start_time BIGINT NOT NULL,
    end_time BIGINT NOT NULL
);