CREATE TABLE IF NOT EXISTS job_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    downloadurl TEXT NOT NULL,
    job_type_num INTEGER,
    job_id TEXT ,
    created_at TIMESTAMP ,
    finish_at TIMESTAMP
);
DROP TABLE IF EXISTS job_type;
CREATE TABLE IF NOT EXISTS job_type (
    job_type TEXT NOT NULL,
    job_num INTEGER NOT NULL
);
INSERT INTO job_type (job_type, job_num)
VALUES
    ('提交', 0),
    ('运行中', 1),
    ('完成', 2),
    ('错误', 3);