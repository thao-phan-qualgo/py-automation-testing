"""
SQL queries for database testing.

This module contains reusable SQL queries for test automation,
organized by table and purpose.
"""

# ============================================================================
# USERS TABLE QUERIES
# ============================================================================
# Schema: id, deleted_at, organization_id, hr_system_id, name, email, phone,
#         title, department, manager_id, status, risk_score, privileged_user,
#         metadata, created_at, updated_at

# Basic SELECT queries
GET_ALL_USERS = """
                SELECT *
                FROM users
                WHERE deleted_at IS NULL
                ORDER BY created_at DESC; \
                """

GET_USER_BY_ID = """
                 SELECT *
                 FROM users
                 WHERE id = %s
                   AND deleted_at IS NULL; \
                 """

GET_USER_BY_EMAIL = """
                    SELECT *
                    FROM users
                    WHERE email = %s
                      AND deleted_at IS NULL; \
                    """

GET_USER_BY_NAME = """
                   SELECT *
                   FROM users
                   WHERE name = %s
                     AND deleted_at IS NULL; \
                   """

# Filter queries
GET_ACTIVE_USERS = """
                   SELECT *
                   FROM users
                   WHERE status = 'active'
                     AND deleted_at IS NULL
                   ORDER BY created_at DESC; \
                   """

GET_DELETED_USERS = """
                    SELECT *
                    FROM users
                    WHERE deleted_at IS NOT NULL
                    ORDER BY deleted_at DESC; \
                    """

GET_USERS_BY_TITLE = """
                     SELECT *
                     FROM users
                     WHERE title = %s
                       AND deleted_at IS NULL
                     ORDER BY created_at DESC; \
                     """

GET_USERS_BY_STATUS = """
                      SELECT *
                      FROM users
                      WHERE status = %s
                        AND deleted_at IS NULL
                      ORDER BY created_at DESC; \
                      """

# Filter by department and organization
GET_USERS_BY_DEPARTMENT = """
                          SELECT *
                          FROM users
                          WHERE department = %s
                            AND deleted_at IS NULL
                          ORDER BY name; \
                          """

GET_USERS_BY_ORGANIZATION = """
                            SELECT *
                            FROM users
                            WHERE organization_id = %s
                              AND deleted_at IS NULL
                            ORDER BY created_at DESC; \
                            """

GET_PRIVILEGED_USERS = """
                       SELECT *
                       FROM users
                       WHERE privileged_user = true
                         AND deleted_at IS NULL
                       ORDER BY risk_score DESC; \
                       """

GET_HIGH_RISK_USERS = """
                      SELECT *
                      FROM users
                      WHERE risk_score >= %s
                        AND deleted_at IS NULL
                      ORDER BY risk_score DESC; \
                      """

# Search queries
SEARCH_USERS_BY_NAME = """
                       SELECT *
                       FROM users
                       WHERE name ILIKE %s
                         AND deleted_at IS NULL
                       ORDER BY name; \
                       """

SEARCH_USERS_BY_EMAIL = """
                        SELECT *
                        FROM users
                        WHERE email ILIKE %s
                          AND deleted_at IS NULL
                        ORDER BY email; \
                        """

SEARCH_USERS_BY_DEPARTMENT = """
                             SELECT *
                             FROM users
                             WHERE department ILIKE %s
                               AND deleted_at IS NULL
                             ORDER BY department, name; \
                             """

# Count queries
COUNT_ALL_USERS = """
                  SELECT COUNT(*)
                  FROM users
                  WHERE deleted_at IS NULL; \
                  """

COUNT_ACTIVE_USERS = """
                     SELECT COUNT(*)
                     FROM users
                     WHERE status = 'active'
                       AND deleted_at IS NULL; \
                     """

COUNT_USERS_BY_STATUS = """
                        SELECT status, COUNT(*) as count
                        FROM users
                        WHERE deleted_at IS NULL
                        GROUP BY status
                        ORDER BY count DESC; \
                        """

COUNT_USERS_BY_DEPARTMENT = """
                            SELECT department, COUNT(*) as count
                            FROM users
                            WHERE deleted_at IS NULL
                              AND department IS NOT NULL
                            GROUP BY department
                            ORDER BY count DESC; \
                            """

# Validation queries
CHECK_USER_EXISTS_BY_EMAIL = """
                             SELECT EXISTS(SELECT 1
                                           FROM users
                                           WHERE email = %s
                                             AND deleted_at IS NULL); \
                             """

CHECK_USER_EXISTS_BY_ID = """
                          SELECT EXISTS(SELECT 1
                                        FROM users
                                        WHERE id = %s
                                          AND deleted_at IS NULL); \
                          """

# Recent users
GET_RECENT_USERS = """
                   SELECT *
                   FROM users
                   WHERE deleted_at IS NULL
                   ORDER BY created_at DESC
                       LIMIT %s; \
                   """

GET_USERS_CREATED_TODAY = """
                          SELECT *
                          FROM users
                          WHERE DATE (created_at) = CURRENT_DATE
                            AND deleted_at IS NULL
                          ORDER BY created_at DESC; \
                          """

GET_USERS_CREATED_LAST_N_DAYS = """
                                SELECT *
                                FROM users
                                WHERE created_at >= CURRENT_DATE - INTERVAL '%s days'
                                  AND deleted_at IS NULL
                                ORDER BY created_at DESC; \
                                """

GET_RECENTLY_UPDATED_USERS = """
                             SELECT *
                             FROM users
                             WHERE deleted_at IS NULL
                             ORDER BY updated_at DESC
                                 LIMIT %s; \
                             """

# User details
GET_USER_WITH_DETAILS = """
                        SELECT u.*
                        FROM users u
                        WHERE u.id = %s
                          AND u.deleted_at IS NULL; \
                        """

# Specific field queries
GET_USER_EMAILS = """
                  SELECT id, email
                  FROM users
                  WHERE deleted_at IS NULL
                  ORDER BY email; \
                  """

GET_ALL_DEPARTMENTS = """
                      SELECT DISTINCT department
                      FROM users
                      WHERE department IS NOT NULL
                        AND deleted_at IS NULL
                      ORDER BY department; \
                      """

GET_ALL_TITLES = """
                 SELECT DISTINCT title
                 FROM users
                 WHERE title IS NOT NULL
                   AND deleted_at IS NULL
                 ORDER BY title; \
                 """

GET_ALL_STATUSES = """
                   SELECT DISTINCT status
                   FROM users
                   WHERE status IS NOT NULL
                     AND deleted_at IS NULL
                   ORDER BY status; \
                   """

# ============================================================================
# TEST DATA QUERIES
# ============================================================================

GET_TEST_USERS = """
                 SELECT *
                 FROM users
                 WHERE email LIKE '%@test.com'
                   AND deleted_at IS NULL
                 ORDER BY created_at DESC; \
                 """

COUNT_TEST_USERS = """
                   SELECT COUNT(*)
                   FROM users
                   WHERE email LIKE '%@test.com'
                     AND deleted_at IS NULL; \
                   """

# ============================================================================
# VALIDATION QUERIES
# ============================================================================

VALIDATE_USER_DATA = """
                     SELECT id,
                            name,
                            email,
                            phone,
                            title,
                            department,
                            status,
                            risk_score,
                            privileged_user,
                            created_at IS NOT NULL as has_created_at,
                            updated_at IS NOT NULL as has_updated_at,
                            email ~ '^[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$' as valid_email
                     FROM users
                     WHERE id = %s
                       AND deleted_at IS NULL; \
                     """

GET_USERS_WITH_INVALID_EMAIL = """
                               SELECT *
                               FROM users
                               WHERE email !~ '^[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$'
    AND deleted_at IS NULL; \
                               """

GET_DUPLICATE_EMAILS = """
                       SELECT email, COUNT(*) as count
                       FROM users
                       WHERE deleted_at IS NULL
                       GROUP BY email
                       HAVING COUNT (*) > 1; \
                       """

GET_USERS_WITHOUT_EMAIL = """
                          SELECT *
                          FROM users
                          WHERE (email IS NULL OR email = '')
                            AND deleted_at IS NULL; \
                          """

# ============================================================================
# MANAGER & TEAM QUERIES
# ============================================================================

GET_USERS_BY_MANAGER = """
                       SELECT *
                       FROM users
                       WHERE manager_id = %s
                         AND deleted_at IS NULL
                       ORDER BY name; \
                       """

GET_USER_WITH_MANAGER_INFO = """
                             SELECT u.*,
                                    m.name  as manager_name,
                                    m.email as manager_email
                             FROM users u
                                      LEFT JOIN users m ON u.manager_id = m.id
                             WHERE u.id = %s
                               AND u.deleted_at IS NULL; \
                             """

COUNT_DIRECT_REPORTS = """
                       SELECT COUNT(*)
                       FROM users
                       WHERE manager_id = %s
                         AND deleted_at IS NULL; \
                       """

# ============================================================================
# PAGINATION QUERIES
# ============================================================================

GET_USERS_PAGINATED = """
                      SELECT *
                      FROM users
                      WHERE deleted_at IS NULL
                      ORDER BY created_at DESC
                          LIMIT %s
                      OFFSET %s; \
                      """

GET_USERS_WITH_TOTAL_COUNT = """
                             SELECT *,
                                    COUNT(*) OVER() as total_count
                             FROM users
                             WHERE deleted_at IS NULL
                             ORDER BY created_at DESC
                                 LIMIT %s
                             OFFSET %s; \
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
                        SELECT EXISTS (SELECT
                                       FROM information_schema.tables
                                       WHERE table_schema = 'public'
                                         AND table_name = '{table_name}'); \
                        """

GET_TABLE_COLUMNS_TEMPLATE = """
                             SELECT column_name, data_type, is_nullable
                             FROM information_schema.columns
                             WHERE table_schema = 'public'
                               AND table_name = '{table_name}'
                             ORDER BY ordinal_position; \
                             """

GET_TABLE_COUNT_TEMPLATE = """
                           SELECT COUNT(*)
                           FROM {table_name}; \
                           """

# ============================================================================
# DEVICES TABLE QUERIES
# ============================================================================

# Total devices count
COUNT_TOTAL_DEVICES = """
                      SELECT COUNT(*)
                      FROM endpoint_devices
                      WHERE deleted_at IS NULL
                      GROUP BY device_type WHERE deleted_at IS NULL; \
                      """

# Total active devices
COUNT_ACTIVE_DEVICES = """
                       SELECT COUNT(*)
                       FROM devices
                       WHERE status = 'active'
                         AND deleted_at IS NULL; \
                       """

# Devices by type
COUNT_DEVICES_BY_TYPE = """
                        SELECT device_type, COUNT(*) as count
                        FROM endpoint_devices
                        WHERE deleted_at IS NULL
                        GROUP BY device_type
                        ORDER BY count DESC; \
                        """
