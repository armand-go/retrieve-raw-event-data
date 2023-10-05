SET ROLE postgres;
CREATE SCHEMA data;
CREATE TABLE data.events (
    event_id INT PRIMARY KEY,
    title VARCHAR NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    location_name VARCHAR,
    address VARCHAR NOT NULL,
    total_tickets_count INT NOT NULL,
    max_ticket_per_user INT NOT NULL,
    sale_start_date TIMESTAMP NOT NULL,
    line_up VARCHAR[],
    asset_url VARCHAR
);