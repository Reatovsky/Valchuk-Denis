ATTACH TABLE _ UUID '7b83862b-cceb-45e9-8ab9-cc0189ed0327'
(
    `grade_id` String,
    `student_id` String,
    `course_code` String,
    `grade` UInt8,
    `grade_type` String,
    `grade_date` Date,
    `semester` UInt8,
    `academic_year` String,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(grade_date)
ORDER BY (student_id, grade_date)
SETTINGS index_granularity = 8192
