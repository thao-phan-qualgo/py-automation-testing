#!/usr/bin/env python3
"""
Test script for users table queries.

This script demonstrates how to use the SQL queries defined in sql_query.py
with the database helper to query and validate user data.
"""

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
    print("1. Counting all users...")
    result = db.fetch_one(sql_query.COUNT_ALL_USERS)
    total_users = result[0] if result else 0
    print(f"   Total users: {total_users}\n")
    
    # 2. Get recent users (limit 5)
    print("2. Getting recent users (top 5)...")
    recent_users = db.execute_query_dict(sql_query.GET_RECENT_USERS, (5,))
    if recent_users:
        for user in recent_users:
            print(f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')}) - Role: {user.get('role', 'N/A')}")
    else:
        print("   No users found")
    print()
    
    # 3. Count active vs inactive users
    print("3. Counting active users...")
    result = db.fetch_one(sql_query.COUNT_ACTIVE_USERS)
    active_count = result[0] if result else 0
    print(f"   Active users: {active_count}")
    print(f"   Inactive users: {total_users - active_count}\n")
    
    # 4. Get all unique roles
    print("4. Getting all user roles...")
    roles = db.execute_query(sql_query.GET_USER_ROLES)
    if roles:
        print(f"   Roles: {', '.join([r[0] for r in roles if r[0]])}")
    else:
        print("   No roles found")
    print()
    
    # 5. Count users by role
    print("5. Counting users by role...")
    role_counts = db.execute_query_dict(sql_query.COUNT_USERS_BY_ROLE)
    if role_counts:
        for rc in role_counts:
            print(f"   {rc.get('role', 'NULL')}: {rc.get('count', 0)} users")
    print()
    
    return True


def test_search_queries():
    """Test search and filter queries."""
    print("\n" + "=" * 60)
    print("Testing Search Queries")
    print("=" * 60)
    
    db = get_db_helper()
    
    # 1. Search by email pattern
    print("\n1. Searching users with 'test' in email...")
    search_pattern = sql_query.build_search_pattern("test")
    test_users = db.execute_query_dict(sql_query.SEARCH_USERS_BY_EMAIL, (search_pattern,))
    print(f"   Found {len(test_users)} test users")
    for user in test_users[:5]:  # Show first 5
        print(f"   - {user.get('email', 'N/A')}")
    print()
    
    # 2. Get users by specific role
    print("2. Getting admin users...")
    admin_users = db.execute_query_dict(sql_query.GET_ADMIN_USERS)
    print(f"   Found {len(admin_users)} admin users")
    for user in admin_users[:3]:  # Show first 3
        print(f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
    print()
    
    return True


def test_specific_user(user_id=None, email=None):
    """Test queries for a specific user."""
    print("\n" + "=" * 60)
    print("Testing Specific User Queries")
    print("=" * 60)
    
    db = get_db_helper()
    
    if email:
        print(f"\nSearching for user by email: {email}")
        user = db.fetch_one_dict(sql_query.GET_USER_BY_EMAIL, (email,))
        
        if user:
            print("✅ User found:")
            print(f"   ID: {user.get('id')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Username: {user.get('username')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Active: {user.get('is_active')}")
            print(f"   Created: {user.get('created_at')}")
            
            # Check if user exists
            exists = db.fetch_one(sql_query.CHECK_USER_EXISTS, (email,))
            print(f"\n   Email exists check: {exists[0] if exists else False}")
        else:
            print(f"❌ User not found with email: {email}")
    
    elif user_id:
        print(f"\nSearching for user by ID: {user_id}")
        user = db.fetch_one_dict(sql_query.GET_USER_BY_ID, (user_id,))
        
        if user:
            print("✅ User found:")
            print(f"   ID: {user.get('id')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Role: {user.get('role')}")
        else:
            print(f"❌ User not found with ID: {user_id}")
    
    print()
    return True


def test_validation_queries():
    """Test data validation queries."""
    print("\n" + "=" * 60)
    print("Testing Validation Queries")
    print("=" * 60)
    
    db = get_db_helper()
    
    # 1. Check for duplicate emails
    print("\n1. Checking for duplicate emails...")
    duplicates = db.execute_query_dict(sql_query.GET_DUPLICATE_EMAILS)
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} duplicate emails:")
        for dup in duplicates[:5]:
            print(f"   - {dup.get('email')}: {dup.get('count')} occurrences")
    else:
        print("   ✅ No duplicate emails found")
    print()
    
    # 2. Check for invalid emails
    print("2. Checking for invalid email formats...")
    invalid_emails = db.execute_query_dict(sql_query.GET_USERS_WITH_INVALID_EMAIL)
    if invalid_emails:
        print(f"   ⚠️  Found {len(invalid_emails)} invalid emails:")
        for user in invalid_emails[:5]:
            print(f"   - {user.get('email')}")
    else:
        print("   ✅ All emails have valid format")
    print()
    
    return True


def test_test_data_queries():
    """Test queries related to test data."""
    print("\n" + "=" * 60)
    print("Testing Test Data Queries")
    print("=" * 60)
    
    db = get_db_helper()
    
    # Count test users
    result = db.fetch_one(sql_query.COUNT_TEST_USERS)
    test_user_count = result[0] if result else 0
    print(f"\nTest users in database: {test_user_count}")
    
    if test_user_count > 0:
        print("\nTest user details:")
        test_users = db.execute_query_dict(sql_query.GET_TEST_USERS)
        for user in test_users[:10]:  # Show first 10
            print(f"  - {user.get('email')} (ID: {user.get('id')}, Role: {user.get('role')})")
    
    print()
    return True


def main():
    """Run all test queries."""
    print("\n" + "=" * 70)
    print("USER TABLE QUERY TESTS")
    print("=" * 70)
    
    try:
        # Run tests
        test_basic_queries()
        test_search_queries()
        test_validation_queries()
        test_test_data_queries()
        
        # Optional: Test specific user
        # Uncomment and modify with actual email/ID
        # test_specific_user(email="user@example.com")
        # test_specific_user(user_id=1)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

