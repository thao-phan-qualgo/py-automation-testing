# Created by thaophan@qualgo.net at 11/11/25
Feature: Overview page

  Background:
    Given I am logged in as an admin user

  @OV_01
  Scenario: Verify Overview Display
    Given I am on the Overview page
    Then I should see the Overview page
