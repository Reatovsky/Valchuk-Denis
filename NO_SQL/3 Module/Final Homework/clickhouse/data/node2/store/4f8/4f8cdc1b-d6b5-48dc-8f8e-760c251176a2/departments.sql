ATTACH TABLE _ UUID '8b772cdf-f06e-44ad-92cf-94d4ed7f7742'
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
ENGINE = Distributed('cluster_3shards', 'test', 'departments_local', rand())
