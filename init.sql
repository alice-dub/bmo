-- table
CREATE table list_pdf (
        id SERIAL PRIMARY KEY,
        url text,
        content text,
        pub_date date
);

-- user for the service/script
create user bmo with password 'qsdfghjkl';
GRANT CONNECT ON DATABASE bmo TO bmo;
GRANT USAGE ON SCHEMA public TO bmo;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bmo;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bmo;

-- extension to remove accent
CREATE EXTENSION unaccent;
-- search config to add accent removal
CREATE TEXT SEARCH CONFIGURATION fr ( COPY = french );
ALTER TEXT SEARCH CONFIGURATION fr ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;

-- the view
CREATE MATERIALIZED VIEW search_index AS 
SELECT id,
       to_tsvector('fr', content) as document
FROM list_pdf;
CREATE INDEX idx_fts_search ON search_index USING gin(document);

-- re gives right after creating the view
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bmo;
