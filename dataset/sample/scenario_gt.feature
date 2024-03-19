Feature: Login Suite

  @Login
  Scenario: Login successfully with correct account @login_user_success
    Given I go to login page
    When I type data with key "user.email" to input with locator "input[name='email']"
    And I type data with key "user.password" to input with locator "input[name='password']"
    And I click button with locator "form > button"
    Then I should be in home page

  Scenario: Login unsuccessfully with empty email and password @login_empty_fields_unsuccessfully
    Given I go to login page
    When I type "" to input with locator "input[name='email']"
    And I type "" to input with locator "input[name='password']"
    And I click button with locator "form > button"
    Then I expect that the text "Email is required" is visible
    Then I expect that the text "Password is required" is visible

  Scenario: Login unsuccessfully with non-existing email in system @login_non_exisiting_email_unsuccessfully
    Given I go to login page
    When I type "<user_email>" to input with locator "input[name='email']"
    And I type "<user_password>" to input with locator "input[name='password']"
    And I click button with locator "form > button"
    Then I expect that the text "The email or password is incorrect!" is invisible

    Examples:
      | user_email              | user_password |
      | volta_e2e_non@gmail.com |        123456 |

  Scenario: Login unsuccessfully with incorrect password @login_wrong_password_unsuccessfully
    Given I go to login page
    When I type "<user_email>" to input with locator "input[name='email']"
    And I type "<user_password>" to input with locator "input[name='password']"
    And I click button with locator "form > button"
    Then I expect that the text "The email or password is incorrect!" is invisible

    Examples:
      | user_email          | user_password |
      | volta_e2e@gmail.com |  123456123123 |

  Scenario: Login unsuccessfully with invalid email format @login_invalid_email_unsuccessfully
    Given I go to login page
    When I type "<user_email>" to input with locator "input[name='email']"
    And I type "<user_password>" to input with locator "input[name='password']"
    And I click button with locator "form > button"
    Then I expect that the text "Invalid email" is visible

    Examples:
      | user_email      | user_password |
      | volta_e2e@gmail |        123456 |

  Scenario: Login successfully with account user @given_login_user_success
    Given I login as user