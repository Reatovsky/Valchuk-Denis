ATTACH TABLE _ UUID '9a192b21-aadf-4fc2-9907-ba539fae7e33'
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
ENGINE = Distributed('cluster_3shards', 'test', 'students_local', cityHash64(student_id))
