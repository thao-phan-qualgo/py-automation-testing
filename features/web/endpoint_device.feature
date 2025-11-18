# Created by thaophan at 17/11/25
Feature: Endpoint Device Wazuh Auto-Sync
  As a security analyst
  I want devices to automatically sync with Wazuh
  So that I have up-to-date security information

  Background:
	Given a PostgreSQL database is initialized
	And a Wazuh Manager is running
	And I am authenticated as an admin user

  Scenario: Successful device sync with active Wazuh agent
	Given I have imported a device with hostname "TEST-LAPTOP-001"
	And a Wazuh agent "001" exists with name "TEST-LAPTOP-001"
	And the Wazuh agent status is "active"
	When the sync task runs for device "TEST-LAPTOP-001"
	Then the device sync status should be "synced"
	And the device should have OS information populated
	And the device should have hardware information populated
	And the device should have a compliance score between 0 and 100
	And the sync log should show status "success"

  Scenario: Device sync with agent not found
	Given I have imported a device with hostname "MISSING-DEVICE"
	And no Wazuh agent exists with name "MISSING-DEVICE"
	When the sync task runs for device "MISSING-DEVICE"
	Then the device sync status should be "not_available"
	And the device sync error should contain "Agent not found"
	And no retry should be scheduled
	And the sync log should show status "failed"

  Scenario: Device sync with disconnected agent
	Given I have imported a device with hostname "OFFLINE-LAPTOP"
	And a Wazuh agent "002" exists with name "OFFLINE-LAPTOP"
	And the Wazuh agent status is "disconnected"
	And the agent last keep alive was "2 hours ago"
	When the sync task runs for device "OFFLINE-LAPTOP"
	Then the device sync status should be "partial"
	And the device last_seen should be updated to "2 hours ago"
	And the device monitoring_status should be "no"
	And a retry should be scheduled in "1 hour"
	And the sync log should show status "partial"

  Scenario: Scheduled hourly sync updates security status
	Given I have a device "LAPTOP-001" synced 50 minutes ago
	And the device has compliance score 85
	And the Wazuh agent now has 2 new critical vulnerabilities
	When the hourly sync task runs
	Then the device compliance score should be less than 85
	And the device security_status should show 2 critical vulnerabilities
	And an alert should be triggered for "critical_vulnerabilities"
	And the sync log should record "light sync" type

  Scenario: API rate limit handling
	Given I have 100 devices to sync
	And the Wazuh API rate limit is 60 requests per minute
	When the sync tasks run for all devices
	Then all devices should eventually sync successfully
	And the sync logs should show some "rate limit" delays
	And no device should have status "failed" due to rate limiting

  Scenario: Compliance score calculation
	Given I have a device with:
	  | Field          | Value      |
	  | SCA Score      | 90         |
	  | Critical Vulns | 0          |
	  | High Vulns     | 1          |
	  | Antivirus      | installed  |
	  | Firewall       | enabled    |
	  | Encryption     | enabled    |
	  | Patch Level    | up_to_date |
	When the compliance score is calculated
	Then the compliance score should be approximately 92
    # Formula: (90 * 0.5) + ((100 - 10) * 0.3) + (100 * 0.2) = 45 + 27 + 20 = 92

  Scenario: Excel import with mixed valid and invalid rows
	Given I have an Excel file with:
	  | Row | Hostname        | Ownership    | Business Impact | Criticality | Valid |
	  | 2   | VALID-LAPTOP-01 | organization | high            | High        | Yes   |
	  | 3   | DUPLICATE-NAME  | organization | medium          | Medium      | Yes   |
	  | 4   |                 | organization | low             | Low         | No    |
	  | 5   | DUPLICATE-NAME  | personal     | medium          | Medium      | No    |
	  | 6   | VALID-LAPTOP-02 | invalid_type | high            | High        | No    |
	When I import the Excel file
	Then 2 devices should be created
	And 3 errors should be returned
	And the errors should include details for rows 4, 5, and 6