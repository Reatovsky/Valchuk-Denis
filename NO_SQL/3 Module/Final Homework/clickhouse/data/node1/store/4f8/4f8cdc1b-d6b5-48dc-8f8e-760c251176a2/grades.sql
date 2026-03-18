ATTACH TABLE _ UUID 'fe046a39-0c41-4265-99b6-6c14773a4d47'
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
ENGINE = Distributed('cluster_3shards', 'test', 'grades_local', cityHash64(student_id))
