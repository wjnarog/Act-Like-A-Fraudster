CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address VARCHAR(100),
    description TEXT,
    price DECIMAL(10, 2),
    location VARCHAR(100),
    type VARCHAR(100),
    lot_size VARCHAR(100),
    bedrooms INT,
    bathrooms INT,
    square_feet INT
);

CREATE TABLE owner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each owner
    first_name VARCHAR(50) NOT NULL,       -- Owner's first name
    last_name VARCHAR(50) NOT NULL,        -- Owner's last name
    age INT,
    email VARCHAR(100) UNIQUE NOT NULL,    -- Owner's email address
    phone VARCHAR(20),                     -- Owner's phone number
    
    -- Address fields
    street_address VARCHAR(100) NOT NULL,  -- Street address
    city VARCHAR(50) NOT NULL,             -- City
    state VARCHAR(50) NOT NULL,            -- State or province
    postal_code VARCHAR(20) NOT NULL,      -- Postal/ZIP code
    country VARCHAR(50) NOT NULL           -- Country
);