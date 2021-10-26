USE assign_paper_kwds;

CREATE TABLE Publication_FoS (
	publication_id int,
    FoS_id int,
    score double,
    CONSTRAINT publication_keyword_pk PRIMARY KEY (publication_id, FoS_id)
);