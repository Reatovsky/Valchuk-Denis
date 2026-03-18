ATTACH TABLE _ UUID 'd8702f36-9aae-4b6a-afce-0d5dc09db043'
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
ENGINE = Distributed('cluster_3shards', 'test', 'teachers_local', cityHash64(teacher_id))
