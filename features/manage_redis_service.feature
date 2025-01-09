Feature: Mange Redis service
    Validates if Redis service can be run

    Scenario: Run Redis service
        Given a Redis service is not running
        When start a Redis service
        Then the Redis should be running
    
