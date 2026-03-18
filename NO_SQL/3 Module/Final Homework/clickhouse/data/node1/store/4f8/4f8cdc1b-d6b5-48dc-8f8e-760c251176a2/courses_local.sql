ATTACH TABLE _ UUID '459349ad-92fc-4b00-822f-1454403d3a61'
(
    `course_code` String,
    `course_name` String,
    `credits` UInt8,
    `department_id` String,
    `semester` UInt8,
    `is_elective` UInt8,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (course_code, semester)
SETTINGS index_granularity = 8192
