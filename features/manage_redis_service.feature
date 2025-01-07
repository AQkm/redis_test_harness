Feature: Mange Redis service

    As a user
    I want to start redis service
    So that I can test it

    Scenario: Run Redis service
        Given a Redis service is not running
        When start a Redis service
        Then the Redis should be running
    
