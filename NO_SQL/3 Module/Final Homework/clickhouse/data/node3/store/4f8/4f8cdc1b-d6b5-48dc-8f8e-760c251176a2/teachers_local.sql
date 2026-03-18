ATTACH TABLE _ UUID 'e100a84f-1a8b-456d-baae-1ca19e5e5ecb'
(
    `teacher_id` String,
    `full_name` String,
    `email` String,
    `position` String,
    `degree` String,
    `hire_date` Date,
    `max_hours` UInt16,
    `current_hours` UInt16,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY toYear(hire_date)
ORDER BY (teacher_id, hire_date)
SETTINGS index_granularity = 8192
