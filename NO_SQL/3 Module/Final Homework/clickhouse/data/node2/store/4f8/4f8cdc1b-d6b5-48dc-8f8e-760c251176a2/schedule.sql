ATTACH TABLE _ UUID 'ee333041-0f03-4848-94c5-3f511ee055d3'
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
ENGINE = Distributed('cluster_3shards', 'test', 'schedule_local', cityHash64(group_code))
