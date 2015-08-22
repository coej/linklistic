CREATE TABLE Link
(
    link_id     serial,
    href        text,
    title       text,
    note        text,
    thumbnail   bytea,
    CONSTRAINT link_pk PRIMARY KEY(link_id)
);


# INSERT INTO Link (href, title, note) 
#    VALUES ('http://www.ysib.com', 'YSIB Homepage', 'ysib rox');
#
# INSERT INTO Link (href, title, note) 
#    VALUES ('http://www.amazon.com', 'Amazon', 'get back to work');

#INSERT INTO Link (href, title, note) 
#SELECT LOWER('http://www.AVClub.com'), 'The A.V. Club', 'w00t'
#WHERE NOT EXISTS (
#    select * from Link where LOWER(href) = LOWER('http://www.avclub.com')
#);
#
#select * from link;