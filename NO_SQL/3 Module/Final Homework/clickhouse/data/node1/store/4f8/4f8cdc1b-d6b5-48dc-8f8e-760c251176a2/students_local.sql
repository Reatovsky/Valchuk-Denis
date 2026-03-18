ATTACH TABLE _ UUID 'adcc615b-4a80-499d-a267-5ed2e1cff73a'
(
    `student_id` String,
    `full_name` String,
    `birth_date` Date,
    `email` String,
    `faculty_code` String,
    `group_code` String,
    `enrollment_year` UInt16,
    `status` String,
    `gpa` Float32,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY enrollment_year
ORDER BY (student_id, enrollment_year)
SETTINGS index_granularity = 8192
