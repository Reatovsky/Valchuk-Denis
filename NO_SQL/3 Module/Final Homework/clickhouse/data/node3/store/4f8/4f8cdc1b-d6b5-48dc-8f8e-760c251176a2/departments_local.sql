ATTACH TABLE _ UUID '802852eb-3467-4b52-9c99-f19fc24aa9f9'
(
    `department_id` String,
    `name` String,
    `type` String,
    `dean_name` String,
    `contact_email` String,
    `phone` String,
    `building` String,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (department_id, name)
SETTINGS index_granularity = 8192
