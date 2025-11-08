CREATE OR REPLACE MODEL `dataset.table_name`
OPTIONS(
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['__label__'],   -- this will be replaced below
  auto_class_weights = TRUE,
  data_split_method = 'AUTO_SPLIT'
) AS

WITH prepared AS (
  SELECT *
  FROM `dataset.table_name`
)

SELECT
  * EXCEPT(last_col),
  last_col AS __label__
FROM (
  SELECT
    *,

    is_duplicate AS last_col
  FROM `dataset.table_name`
);
