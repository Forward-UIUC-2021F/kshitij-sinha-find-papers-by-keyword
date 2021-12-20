USE assign_paper_kwds;

CREATE TABLE FoS(
	id INT PRIMARY KEY,
    keyword TEXT,
    frequency INT
);

CREATE TABLE Publication(
    id VARCHAR(300) PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    citations INT
);

CREATE TABLE Publication_FoS (
    Publication_id VARCHAR(300),
    FoS_id INT,
    score DOUBLE,
    FOREIGN KEY (publication_id) REFERENCES Publication(id) ON DELETE CASCADE,
    FOREIGN KEY (FoS_id) REFERENCES FoS(id) ON DELETE CASCADE,
    CONSTRAINT publication_keyword_pk PRIMARY KEY (publication_id, FoS_id)
);