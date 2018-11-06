--sqlite command to replace a string
update bm_section set link=replace(link,'section','s') where link like 'section%';

--sqlite command to find the last inserted value to the table
SELECT last_insert_rowid();
