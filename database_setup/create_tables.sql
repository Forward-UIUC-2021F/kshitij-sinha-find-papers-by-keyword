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

CREATE TABLE FoS_npmi_Springer (
    id1 int NOT NULL,
    id2 int NOT NULL,
    len1 int DEFAULT NULL,
    len2 int DEFAULT NULL,
    intersection_len int DEFAULT NULL,
    npmi double DEFAULT NULL,
    PRIMARY KEY (id1,id2),
    FOREIGN KEY (id1) REFERENCES FoS (id),
    FOREIGN KEY (id2) REFERENCES FoS (id)
);