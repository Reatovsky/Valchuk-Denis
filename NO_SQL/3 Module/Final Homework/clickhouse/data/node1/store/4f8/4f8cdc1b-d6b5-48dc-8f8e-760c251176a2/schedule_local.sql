ATTACH TABLE _ UUID 'c5a236a4-b19d-49e9-bdcd-89504d35b521'
(
    `schedule_id` String,
    `group_code` String,
    `course_code` String,
    `teacher_id` String,
    `day_of_week` UInt8,
    `pair_number` UInt8,
    `week_type` String,
    `classroom` String,
    `semester` UInt8,
    `academic_year` String,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY semester
ORDER BY (group_code, day_of_week, pair_number)
SETTINGS index_granularity = 8192
