Feature: Login Suite
  @Login
  Scenario: Login successfully with correct account
    Given I load data "USER"
    And I go to login page
    When I type test data "user.email" to input "email"
    And I type test data "user.password" to input "password"
    And I click button with locator "form > button"
    Then I should be in home page

  Scenario: Login unsuccessfully with empty email and password
    Given I load data "USER"
    And I go to login page
    When I type test data "user.emptyEmail" to input "email"
    And I type test data "user.emptyPassword" to input "password"
    And I click button with locator "form > button"
    Then The text of "Email is required" should be visible
    Then The text of "Password is required" should be visible

  Scenario: Login unsuccessfully with non-existing email in system
    Given I load data "USER"
    And I go to login page
    When I type test data "user.nonEmail" to input "email"
    And I type test data "user.password" to input "password"
    And I click button with locator "form > button"
    Then The text of "The email or password is incorrect!" should be visible

  Scenario: Login unsuccessfully with incorrect password
    Given I load data "USER"
    And I go to login page
    When I type test data "user.nonEmail" to input "email"
    And I type test data "user.incorrectPassword" to input "password"
    And I click button with locator "form > button"
    Then The text of "The email or password is incorrect!" should be visible

  Scenario: Login unsuccessfully with invalid email format
    Given I load data "USER"
    And I go to login page
    When I type test data "user.incorrectEmail" to input "email"
    And I type test data "user.password" to input "password"
    And I click button with locator "form > button"
    Then The text of "Invalid email" should be visible