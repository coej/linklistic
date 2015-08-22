CREATE TABLE Link
(
    link_id     serial,
    href        text,
    title       text,
    note        text,
    thumbnail   bytea,
    CONSTRAINT link_pk PRIMARY KEY(link_id)
);


INSERT INTO Link (href, title, note) 
    VALUES ('http://www.ysib.com', 'YSIB Homepage', 'ysib rox');

INSERT INTO Link (href, title, note) 
    VALUES ('http://www.amazon.com', 'Amazon', 'get back to work');
