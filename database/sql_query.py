"""
SQL queries for database testing.

This module contains reusable SQL queries for test automation,
organized by table and purpose.
"""

# ============================================================================
# USERS TABLE QUERIES
# ============================================================================

# Basic SELECT queries
GET_ALL_USERS = """
    SELECT * FROM users
    ORDER BY created_at DESC;
"""

GET_USER_BY_ID = """
    SELECT * FROM users 
    WHERE id = %s;
"""

GET_USER_BY_EMAIL = """
    SELECT * FROM users 
    WHERE email = %s;
"""

GET_USER_BY_USERNAME = """
    SELECT * FROM users 
    WHERE username = %s;
"""

# Filter queries
GET_ACTIVE_USERS = """
    SELECT * FROM users 
    WHERE is_active = true
    ORDER BY created_at DESC;
"""

GET_INACTIVE_USERS = """
    SELECT * FROM users 
    WHERE is_active = false
    ORDER BY created_at DESC;
"""

GET_USERS_BY_ROLE = """
    SELECT * FROM users 
    WHERE role = %s
    ORDER BY created_at DESC;
"""

GET_USERS_BY_STATUS = """
    SELECT * FROM users 
    WHERE status = %s
    ORDER BY created_at DESC;
"""

# Search queries
SEARCH_USERS_BY_NAME = """
    SELECT * FROM users 
    WHERE name ILIKE %s
    ORDER BY name;
"""

SEARCH_USERS_BY_EMAIL = """
    SELECT * FROM users 
    WHERE email ILIKE %s
    ORDER BY email;
"""

# Count queries
COUNT_ALL_USERS = """
    SELECT COUNT(*) FROM users;
"""

COUNT_ACTIVE_USERS = """
    SELECT COUNT(*) FROM users 
    WHERE is_active = true;
"""

COUNT_USERS_BY_ROLE = """
    SELECT role, COUNT(*) as count 
    FROM users 
    GROUP BY role
    ORDER BY count DESC;
"""

# Validation queries
CHECK_USER_EXISTS = """
    SELECT EXISTS(
        SELECT 1 FROM users 
        WHERE email = %s
    );
"""

CHECK_USERNAME_EXISTS = """
    SELECT EXISTS(
        SELECT 1 FROM users 
        WHERE username = %s
    );
"""

# Recent users
GET_RECENT_USERS = """
    SELECT * FROM users 
    ORDER BY created_at DESC 
    LIMIT %s;
"""

GET_USERS_CREATED_TODAY = """
    SELECT * FROM users 
    WHERE DATE(created_at) = CURRENT_DATE
    ORDER BY created_at DESC;
"""

GET_USERS_CREATED_LAST_N_DAYS = """
    SELECT * FROM users 
    WHERE created_at >= CURRENT_DATE - INTERVAL '%s days'
    ORDER BY created_at DESC;
"""

# User details with joins (if applicable)
GET_USER_WITH_DETAILS = """
    SELECT 
        u.*,
        u.created_at,
        u.updated_at
    FROM users u
    WHERE u.id = %s;
"""

# Specific field queries
GET_USER_EMAILS = """
    SELECT email FROM users 
    ORDER BY email;
"""

GET_USER_ROLES = """
    SELECT DISTINCT role FROM users 
    WHERE role IS NOT NULL
    ORDER BY role;
"""

# ============================================================================
# INSERT QUERIES
# ============================================================================

INSERT_USER = """
    INSERT INTO users (name, email, username, role, is_active, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
"""

INSERT_USER_WITH_PASSWORD = """
    INSERT INTO users (name, email, username, password_hash, role, is_active)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
"""

# ============================================================================
# UPDATE QUERIES
# ============================================================================

UPDATE_USER_NAME = """
    UPDATE users 
    SET name = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

UPDATE_USER_EMAIL = """
    UPDATE users 
    SET email = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

UPDATE_USER_ROLE = """
    UPDATE users 
    SET role = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

UPDATE_USER_STATUS = """
    UPDATE users 
    SET is_active = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

ACTIVATE_USER = """
    UPDATE users 
    SET is_active = true, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

DEACTIVATE_USER = """
    UPDATE users 
    SET is_active = false, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s;
"""

# ============================================================================
# DELETE QUERIES
# ============================================================================

DELETE_USER_BY_ID = """
    DELETE FROM users 
    WHERE id = %s;
"""

DELETE_USER_BY_EMAIL = """
    DELETE FROM users 
    WHERE email = %s;
"""

DELETE_TEST_USERS = """
    DELETE FROM users 
    WHERE email LIKE '%@test.com'
    OR username LIKE 'test_%';
"""

DELETE_INACTIVE_USERS = """
    DELETE FROM users 
    WHERE is_active = false
    AND created_at < CURRENT_DATE - INTERVAL '90 days';
"""

# ============================================================================
# TEST DATA QUERIES
# ============================================================================

GET_TEST_USERS = """
    SELECT * FROM users 
    WHERE email LIKE '%@test.com'
    OR username LIKE 'test_%'
    ORDER BY created_at DESC;
"""

COUNT_TEST_USERS = """
    SELECT COUNT(*) FROM users 
    WHERE email LIKE '%@test.com'
    OR username LIKE 'test_%';
"""

# ============================================================================
# VALIDATION QUERIES
# ============================================================================

VALIDATE_USER_DATA = r"""
    SELECT 
        id,
        name,
        email,
        username,
        role,
        is_active,
        created_at IS NOT NULL as has_created_at,
        email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' as valid_email
    FROM users
    WHERE id = %s;
"""

GET_USERS_WITH_INVALID_EMAIL = r"""
    SELECT * FROM users 
    WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
"""

GET_DUPLICATE_EMAILS = """
    SELECT email, COUNT(*) as count 
    FROM users 
    GROUP BY email 
    HAVING COUNT(*) > 1;
"""

# ============================================================================
# ADMIN & SPECIAL ROLE QUERIES
# ============================================================================

GET_ADMIN_USERS = """
    SELECT * FROM users 
    WHERE role = 'admin'
    ORDER BY created_at;
"""

GET_USERS_BY_MULTIPLE_ROLES = """
    SELECT * FROM users 
    WHERE role IN %s
    ORDER BY role, name;
"""

# ============================================================================
# PAGINATION QUERIES
# ============================================================================

GET_USERS_PAGINATED = """
    SELECT * FROM users 
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
"""

GET_USERS_WITH_TOTAL_COUNT = """
    SELECT 
        *,
        COUNT(*) OVER() as total_count
    FROM users 
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
"""

# ============================================================================
# HELPER FUNCTIONS FOR QUERY USAGE
# ============================================================================

def build_search_pattern(search_term: str) -> str:
    """
    Build a search pattern for ILIKE queries.
    
    Args:
        search_term: The term to search for
        
    Returns:
        Search pattern with wildcards
        
    Example:
        >>> build_search_pattern("john")
        '%john%'
    """
    return f"%{search_term}%"


def get_users_by_filter(filter_dict: dict) -> tuple:
    """
    Build dynamic WHERE clause from filter dictionary.
    
    Args:
        filter_dict: Dictionary of field: value filters
        
    Returns:
        Tuple of (query, params)
        
    Example:
        >>> filters = {'role': 'admin', 'is_active': True}
        >>> query, params = get_users_by_filter(filters)
    """
    base_query = "SELECT * FROM users WHERE "
    conditions = []
    params = []
    
    for field, value in filter_dict.items():
        conditions.append(f"{field} = %s")
        params.append(value)
    
    query = base_query + " AND ".join(conditions) + " ORDER BY created_at DESC;"
    return query, tuple(params)


# ============================================================================
# QUERY TEMPLATES (Use with .format() for dynamic table names)
# ============================================================================

TABLE_EXISTS_TEMPLATE = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = '{table_name}'
    );
"""

GET_TABLE_COLUMNS_TEMPLATE = """
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_schema = 'public' 
    AND table_name = '{table_name}'
    ORDER BY ordinal_position;
"""

GET_TABLE_COUNT_TEMPLATE = """
    SELECT COUNT(*) FROM {table_name};
"""

