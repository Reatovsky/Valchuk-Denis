ATTACH TABLE _ UUID '625b0ee8-a9a7-4b06-820e-980cf2523c32'
(
    `course_code` String,
    `course_name` String,
    `credits` UInt8,
    `department_id` String,
    `semester` UInt8,
    `is_elective` UInt8,
    `created_at` DateTime DEFAULT now()
)
ENGINE = Distributed('cluster_3shards', 'test', 'courses_local', cityHash64(course_code))
