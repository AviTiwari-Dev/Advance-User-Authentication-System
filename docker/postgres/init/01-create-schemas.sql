-- Initialize application schemas inside the user_management database.
-- PostgreSQL's container entrypoint runs this file only when the data directory
-- is created for the first time.

CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS user_profile;
