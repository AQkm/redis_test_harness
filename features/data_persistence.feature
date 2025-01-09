Feature: Data persistence
  Verifies that data is persisted correctly in Redis after container restarts.

  Scenario: Data persists after Redis container restart
    Given the Redis container is running
    When a key "key_persistent" is set with value "value_persistent" in Redis
    And the Redis container is restarted
    And a key "key_persistent" is retrieved from Redis
    Then the value of the key should be "value_persistent"

  Scenario: Data does not persist when Redis container is not configured for persistence
    Given the Redis container is running with persistence off
    When a key "key_ephemeral" is set with value "value_ephemeral" in Redis
    And the Redis container is restarted
    And a key "key_ephemeral" is retrieved from Redis
    Then the value of the key should not exist