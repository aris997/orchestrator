DROP TABLE IF EXISTS Tenant;
DROP TABLE IF EXISTS Backup;


-- Starting point
CREATE TABLE IF NOT EXISTS Tenant
(
    id   INTEGER
        CONSTRAINT pk_id_tenant PRIMARY KEY ASC AUTOINCREMENT,
    name TEXT
        CONSTRAINT uq_name_tenants UNIQUE
        CONSTRAINT len_name_tenant CHECK ( length(name) > 3 )
)
;

-- Backup infos
ALTER TABLE Tenant ADD COLUMN
    backup_frequency TEXT
        CONSTRAINT ck_backup_frequency_tenant
            CHECK ( backup_frequency in ('daily', 'weekly', 'montly'));
ALTER TABLE Tenant ADD COLUMN
    backup_offset INTEGER CONSTRAINT ck_backup_offset_tenant CHECK (
        CASE backup_frequency
            WHEN 'daily'
                THEN backup_offset BETWEEN -24 AND 24
            WHEN 'weekly'
                THEN backup_offset BETWEEN -168 AND 168
            WHEN 'montly'
                THEN backup_offset BETWEEN -672 AND 672
            -- ELSE NULL
            END
        )
;
CREATE TABLE IF NOT EXISTS Backup
(
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    id_tenant INTEGER
        CONSTRAINT fk_id_tenant_backup REFERENCES Tenant (id),
    path TEXT,
    hash TEXT,
    type TEXT,
    ts_create TEXT DEFAULT CURRENT_TIMESTAMP
)
;
