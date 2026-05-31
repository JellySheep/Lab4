
CREATE TABLE IF NOT EXISTS os_inventory (
    id SERIAL PRIMARY KEY,
    os_id TEXT,
    os_name VARCHAR(100),
    os_version VARCHAR(50),
    software_count INTEGER,
    software_list JSONB,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vulnerabilities (
    id SERIAL PRIMARY KEY,
    os_inventory_id INTEGER REFERENCES os_inventory(id) ON DELETE CASCADE,
    vuln_id VARCHAR(100) NOT NULL,
    package_name VARCHAR(255),
    package_version VARCHAR(100),
    severity VARCHAR(20),
    summary TEXT,
    found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
