CREATE TABLE Link
(
    link_id     serial,
    href        text,
    title       text,
    note        text,
    thumbnail   bytea,
    CONSTRAINT link_pk PRIMARY KEY(link_id)
);


INSERT INTO Link VALUES 
    (1,

        )


INSERT INTO Link (linkproduct_no, name, price) VALUES (1, 'Cheese', 9.99);