#!/usr/bin/env python3
"""
Test script for users table queries.

This script demonstrates how to use the SQL queries defined in sql_query.py
with the database helper to query and validate user data.

Actual Schema:
- id, deleted_at, organization_id, hr_system_id, name, email, phone,
- title, department, manager_id, status, risk_score, privileged_user,
- metadata, created_at, updated_at
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.db_helper import get_db_helper
from database import sql_query


def test_basic_queries():
    """Test basic user queries."""
    print("\n" + "=" * 60)
    print("Testing Basic User Queries")
    print("=" * 60)

    db = get_db_helper()

    # Test connection
    if not db.test_connection():
        print("❌ Database connection failed!")
        return False

    print("✅ Database connected successfully\n")

    # 1. Count all users
    print("1. Counting all users (excluding deleted)...")
    result = db.fetch_one(sql_query.COUNT_ALL_USERS)
    total_users = result[0] if result else 0
    print(f"   Total users: {total_users}\n")

    # 2. Get recent users (limit 5)
    print("2. Getting recent users (top 5)...")
    recent_users = db.execute_query_dict(sql_query.GET_RECENT_USERS, (5,))
    if recent_users:
        for user in recent_users:
            print(
                f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')}) - Title: {user.get('title', 'N/A')}"
            )
    else:
        print("   No users found")
    print()

    # 3. Count active users
    print("3. Counting users by status...")
    result = db.fetch_one(sql_query.COUNT_ACTIVE_USERS)
    active_count = result[0] if result else 0
    print(f"   Active users: {active_count}")

    # Get status breakdown
    status_counts = db.execute_query_dict(sql_query.COUNT_USERS_BY_STATUS)
    if status_counts:
        print("   Status breakdown:")
        for sc in status_counts:
            print(f"   - {sc.get('status', 'NULL')}: {sc.get('count', 0)} users")
    print()

    # 4. Get all departments
    print("4. Getting all departments...")
    departments = db.execute_query(sql_query.GET_ALL_DEPARTMENTS)
    if departments:
        dept_list = [d[0] for d in departments if d[0]][:10]  # Show first 10
        print(f"   Found {len(departments)} departments (showing first 10):")
        for dept in dept_list:
            print(f"   - {dept}")
    else:
        print("   No departments found")
    print()

    # 5. Count users by department
    print("5. Counting users by department (top 5)...")
    dept_counts = db.execute_query_dict(sql_query.COUNT_USERS_BY_DEPARTMENT)
    if dept_counts:
        for dc in dept_counts[:5]:
            print(f"   {dc.get('department', 'NULL')}: {dc.get('count', 0)} users")
    print()

    return True


def test_search_queries():
    """Test search and filter queries."""
    print("\n" + "=" * 60)
    print("Testing Search Queries")
    print("=" * 60)

    db = get_db_helper()

    # 1. Search by email pattern
    print("\n1. Searching users with '@test.com' in email...")
    search_pattern = sql_query.build_search_pattern("@test.com")
    test_users = db.execute_query_dict(
        sql_query.SEARCH_USERS_BY_EMAIL, (search_pattern,)
    )
    print(f"   Found {len(test_users)} test users")
    for user in test_users[:5]:  # Show first 5
        print(f"   - {user.get('email', 'N/A')}")
    print()

    # 2. Get privileged users
    print("2. Getting privileged users (top 5)...")
    privileged = db.execute_query_dict(sql_query.GET_PRIVILEGED_USERS)
    if privileged:
        print(f"   Found {len(privileged)} privileged users (showing first 5):")
        for user in privileged[:5]:
            print(
                f"   - {user.get('name', 'N/A')} - Risk Score: {user.get('risk_score', 'N/A')}"
            )
    else:
        print("   No privileged users found")
    print()

    # 3. Search by department
    print("3. Searching departments with 'IT' in name...")
    dept_pattern = sql_query.build_search_pattern("IT")
    it_users = db.execute_query_dict(
        sql_query.SEARCH_USERS_BY_DEPARTMENT, (dept_pattern,)
    )
    if it_users:
        print(
            f"   Found {len(it_users)} users in IT-related departments (showing first 5):"
        )
        for user in it_users[:5]:
            print(f"   - {user.get('name', 'N/A')} ({user.get('department', 'N/A')})")
    else:
        print("   No IT users found")
    print()

    # 4. Get high risk users (risk score >= 50)
    print("4. Getting high-risk users (risk_score >= 50)...")
    high_risk = db.execute_query_dict(sql_query.GET_HIGH_RISK_USERS, (50,))
    if high_risk:
        print(f"   Found {len(high_risk)} high-risk users (showing first 5):")
        for user in high_risk[:5]:
            print(
                f"   - {user.get('name', 'N/A')} - Risk: {user.get('risk_score', 'N/A')}"
            )
    else:
        print("   No high-risk users found")
    print()

    return True


def test_specific_user_queries():
    """Test queries for specific users."""
    print("\n" + "=" * 60)
    print("Testing Specific User Queries")
    print("=" * 60)

    db = get_db_helper()

    # Get a user to test with
    recent_users = db.execute_query_dict(sql_query.GET_RECENT_USERS, (1,))
    if not recent_users:
        print("\n❌ No users found for testing")
        return False

    test_user = recent_users[0]
    user_id = test_user.get("id")
    user_email = test_user.get("email")

    print(f"\nUsing test user: {test_user.get('name')} (ID: {user_id})")

    # 1. Get user by ID
    print("\n1. Getting user by ID...")
    user = db.fetch_one_dict(sql_query.GET_USER_BY_ID, (user_id,))
    if user:
        print(f"   ✅ Found: {user.get('name')} ({user.get('email')})")
    else:
        print("   ❌ User not found")

    # 2. Get user by email
    print("\n2. Getting user by email...")
    user = db.fetch_one_dict(sql_query.GET_USER_BY_EMAIL, (user_email,))
    if user:
        print(f"   ✅ Found: {user.get('name')} (ID: {user.get('id')})")
    else:
        print("   ❌ User not found")

    # 3. Check if user exists
    print("\n3. Checking if user exists...")
    exists = db.fetch_one(sql_query.CHECK_USER_EXISTS_BY_EMAIL, (user_email,))
    if exists and exists[0]:
        print("   ✅ User exists")
    else:
        print("   ❌ User does not exist")

    # 4. Get user with details
    print("\n4. Getting user with full details...")
    user_details = db.fetch_one_dict(sql_query.GET_USER_WITH_DETAILS, (user_id,))
    if user_details:
        print("   User details:")
        print(f"   - Name: {user_details.get('name')}")
        print(f"   - Email: {user_details.get('email')}")
        print(f"   - Phone: {user_details.get('phone', 'N/A')}")
        print(f"   - Title: {user_details.get('title', 'N/A')}")
        print(f"   - Department: {user_details.get('department', 'N/A')}")
        print(f"   - Status: {user_details.get('status', 'N/A')}")
        print(f"   - Risk Score: {user_details.get('risk_score', 'N/A')}")
        print(f"   - Privileged: {user_details.get('privileged_user', False)}")
        print(f"   - Created: {user_details.get('created_at')}")

    # 5. Check for manager/direct reports
    if test_user.get("manager_id"):
        print("\n5. Getting user with manager info...")
        user_with_mgr = db.fetch_one_dict(
            sql_query.GET_USER_WITH_MANAGER_INFO, (user_id,)
        )
        if user_with_mgr:
            print(f"   Manager: {user_with_mgr.get('manager_name', 'N/A')}")
    else:
        print("\n5. Checking direct reports...")
        reports_count = db.fetch_one(sql_query.COUNT_DIRECT_REPORTS, (user_id,))
        if reports_count:
            print(f"   Direct reports: {reports_count[0]}")

    print()
    return True


def test_validation_queries():
    """Test data validation queries."""
    print("\n" + "=" * 60)
    print("Testing Validation Queries")
    print("=" * 60)

    db = get_db_helper()

    # 1. Check for invalid emails
    print("\n1. Checking for users with invalid emails...")
    invalid = db.execute_query_dict(sql_query.GET_USERS_WITH_INVALID_EMAIL)
    if invalid:
        print(
            f"   ⚠️  Found {len(invalid)} users with invalid emails (showing first 3):"
        )
        for user in invalid[:3]:
            print(f"   - {user.get('email', 'N/A')}")
    else:
        print("   ✅ All emails are valid")
    print()

    # 2. Check for duplicate emails
    print("2. Checking for duplicate emails...")
    duplicates = db.execute_query_dict(sql_query.GET_DUPLICATE_EMAILS)
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} duplicate emails:")
        for dup in duplicates:
            print(f"   - {dup.get('email')}: {dup.get('count')} occurrences")
    else:
        print("   ✅ No duplicate emails found")
    print()

    # 3. Check for users without email
    print("3. Checking for users without email...")
    no_email = db.execute_query_dict(sql_query.GET_USERS_WITHOUT_EMAIL)
    if no_email:
        print(f"   ⚠️  Found {len(no_email)} users without email (showing first 3):")
        for user in no_email[:3]:
            print(f"   - {user.get('name', 'N/A')} (ID: {user.get('id')})")
    else:
        print("   ✅ All users have email addresses")
    print()

    # 4. Validate specific user data
    print("4. Validating a specific user's data...")
    recent_users = db.execute_query_dict(sql_query.GET_RECENT_USERS, (1,))
    if recent_users:
        user_id = recent_users[0].get("id")
        validation = db.fetch_one_dict(sql_query.VALIDATE_USER_DATA, (user_id,))
        if validation:
            print("   Validation results:")
            print(f"   - Has created_at: {validation.get('has_created_at')}")
            print(f"   - Has updated_at: {validation.get('has_updated_at')}")
            print(f"   - Valid email: {validation.get('valid_email')}")
    print()

    return True


def test_pagination_queries():
    """Test pagination queries."""
    print("\n" + "=" * 60)
    print("Testing Pagination Queries")
    print("=" * 60)

    db = get_db_helper()

    # 1. Get first page
    print("\n1. Getting first page (10 users, offset 0)...")
    page1 = db.execute_query_dict(sql_query.GET_USERS_PAGINATED, (10, 0))
    print(f"   Retrieved {len(page1)} users")
    if page1:
        print("   First 3 users:")
        for user in page1[:3]:
            print(f"   - {user.get('name', 'N/A')}")
    print()

    # 2. Get with total count
    print("2. Getting users with total count (10 users, offset 0)...")
    users_with_count = db.execute_query_dict(
        sql_query.GET_USERS_WITH_TOTAL_COUNT, (10, 0)
    )
    if users_with_count:
        total_count = users_with_count[0].get("total_count")
        print(f"   Total users in database: {total_count}")
        print(f"   Retrieved {len(users_with_count)} users on this page")
    print()

    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("USER TABLE QUERY TESTS")
    print("=" * 70)

    try:
        # Run all test suites
        success = True
        success = test_basic_queries() and success
        success = test_search_queries() and success
        success = test_specific_user_queries() and success
        success = test_validation_queries() and success
        success = test_pagination_queries() and success

        # Summary
        print("\n" + "=" * 70)
        if success:
            print("✅ All tests completed successfully!")
        else:
            print("⚠️  Some tests encountered issues")
        print("=" * 70)

        return 0 if success else 1

    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
