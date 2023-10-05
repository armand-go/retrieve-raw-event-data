SET ROLE postgres;
CREATE SCHEMA data;
CREATE TABLE data.events (
    eventId INT PRIMARY KEY,
    title VARCHAR NOT NULL,
    startDatetime TIMESTAMP NOT NULL,
    endDatetime TIMESTAMP NOT NULL,
    locationName VARCHAR,
    address VARCHAR NOT NULL,
    totalTicketsCount INT NOT NULL,
    maxTicketPerUser INT NOT NULL,
    saleStartDate TIMESTAMP NOT NULL,
    lineUp VARCHAR[],
    assetUrl VARCHAR
);