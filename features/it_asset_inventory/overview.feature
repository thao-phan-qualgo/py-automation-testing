# Created by thaophan@qualgo.net at 11/11/25
Feature: IT Asset Inventory Overview
  As a security administrator
  I want to view the IT Asset Inventory Overview page
  So that I can monitor security posture and compliance metrics

  Background:
	Given I am logged in as an admin user
	And I am on the Security Operations Dashboard Page

  @OV_01 @navigation @smoke
  Scenario Outline: Navigate to Overview page via menu
	When I click on the "<menu_item>" menu item
	And I click on "<submenu_item>" submenu item
	Then I should see the Overview page

	Examples:
	  | menu_item          | submenu_item |
	  | IT Asset Inventory | Overview     |

  @OV_02 @SecurityPosture @High @metrics
  Scenario Outline: Verify Security Posture Overview metrics display correctly
	Given I am on the Overview page
	When I locate the "Security Posture Overview" section
	Then I should see the section title "Security Posture Overview"
	And I should see 4 metric cards displayed
	And I should see the "<metric_card>" metric card with value displayed

	Examples:
	  | metric_card          |
	  | Critical Assets      |
	  | Non-Compliant Assets |
	  | Inactive Devices     |
	  | Compliance Coverage  |

  @OV_03 @SecurityPosture @validation
  Scenario: Verify all metric values are properly formatted
	Given I am on the Overview page
	When I locate the "Security Posture Overview" section
	Then all metric values should be numeric and properly formatted


  @OV_04 @EndpointDevices @High @chart
  Scenario: Verify Endpoint Devices section displays device distribution
	Given I am on the Overview page
	When I scroll to the "Endpoint Devices" section
	Then I should see the "Endpoint Devices" section title
	And I should see the pie chart displayed
	And I should see the "Devices by Criticality" breakdown
	And I should see devices grouped by criticality levels
	  | criticality_level |
	  | Critical          |
	  | High              |
	  | Medium            |
	  | Low               |
	And I should see the total devices count displayed
	And I should see the "View More" link available



