-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## Useful queries to use with System Tables
-- MAGIC
-- MAGIC 1. Get the last time each user has logged into a workspace

-- COMMAND ----------

-- DBTITLE 1,Get the last time each user has logged into a workspace
-- Get the last time each user has logged into a workspace
WITH ranked_events AS (
  SELECT
      event_date,
      user_identity.email,
      service_name,
      action_name,
      ROW_NUMBER() OVER (PARTITION BY user_identity.email ORDER BY event_date DESC) AS rank
  FROM system.access.audit
  WHERE action_name LIKE 'aad%' AND user_identity.email LIKE '%@%'
)
SELECT
    event_date,
    email
    service_name,
    action_name
FROM ranked_events
WHERE rank = 1
ORDER BY event_date DESC;
