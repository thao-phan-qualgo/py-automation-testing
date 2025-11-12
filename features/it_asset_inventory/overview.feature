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
  Scenario: Verify Security Posture Overview metrics display correctly
	Given I am on the Overview page
	When I locate the "Security Posture Overview" section
	Then I should see the section title "Security Posture Overview"
	And I should see 4 metric cards displayed
	And I should see the "Critical Assets" metric card
	And I should see the "Non-Compliant Assets" metric card
	And I should see the "Inactive Devices" metric card
	And I should see the "Compliance Coverage" metric card
	And all metric values should be numeric and properly formatted
