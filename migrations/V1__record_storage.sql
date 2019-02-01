CREATE TABLE fetched_records(
    fetched_record_id bigserial PRIMARY KEY,
    created_at timestamp WITHOUT TIME ZONE DEFAULT now(),
    query_string text,
    record_meta json,
    file_data json,
    record_id UUID NOT NULL,
    record_id_updated_at timestamp WITHOUT TIME ZONE,
    s3_bucket text NOT NULL,
    s3_location text NOT NULL,
    file_name text
);

CREATE INDEX record_id_idx ON fetched_records (record_id);