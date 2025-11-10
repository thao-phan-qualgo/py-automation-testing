# Created by macbook at 10/11/25
Feature: User Login with Microsoft SSO

  As a registered user
  I want to sign in with my Microsoft account
  So that I can access the Security Operations Dashboard

  Background:
    Given I am on the sign-in page

  @web @smoke @login
  Scenario: Successful login with Microsoft SSO (manual MFA)
    When I click the "Sign in with Microsoft" button
    And I enter my email "thao.pt@qualgo.net"
    And I click the "Next" button
    And I enter my password
    And I click the "Sign in" button
    And I wait 20 seconds for manual MFA code entry
    And I choose to stay signed in
    Then I should see the Security Operations Dashboard
