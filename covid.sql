CREATE TABLE public."case" (
    notification_date date NOT NULL,
    postcode character varying,
    lhd_2010_code character varying(4),
    lhd_2010_name character varying(21),
    lga_code19 integer,
    lga_name19 character varying(33),
    likely_source_of_infection character varying(52)
);
