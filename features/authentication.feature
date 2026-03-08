@web

Feature: Login Logout Functionality

  @login 
  Scenario: Successful login with valid credentials
    Given the user is on the home page 
    And User clicks on the login link
    When user logins to the application with valid credentials "Testuserdemo94" and "Welcome@1234"
    Then the username "Testuserdemo94" should be displayed on dashboard page


  
  @invalidlogin
  Scenario: Login with invalid credentials
    Given the user is on the home page [HomePage]
    And User clicks on the login link
    When user logins to the application with invalid credentials "Testuserdemo94" and "Welcom"
    Then the error message should be displayed on login page


  @logout
  Scenario: Successful logout
    Given the user is on the home page [HomePage]
    And User clicks on the login link [HomePage]
    When user logins to the application with valid credentials "Testuserdemo94" and "Welcome@1234" [LoginPage]
    When user clicks on the logout link [DashboardPage]
    Then verify user is logged out successfully [LogoutPage]
    When user clicks on continue button on logout page [LogoutPage]
    Then the user should be redirected to the home page [HomePage]