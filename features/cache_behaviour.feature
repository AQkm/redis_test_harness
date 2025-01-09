Feature: Cache behavior
  Validates that Redis cache behaves as expected, including key expiration and retrieval.

  Scenario: Key is stored and retrieved correctly
    Given the Redis container is running
    When a key "key_to_retrieve" is set with value "value_to_retrieved" in Redis
    And a key "key_to_retrieve" is retrieved from Redis
    Then the value of the key should be "value_to_retrieved"

  Scenario: Key expires after the specified time
    Given the Redis container is running
    When a key "key_to_expire" is set with value "value_to_expire" with expiration of 2 seconds
    And a wait of 3 seconds is performed
    And a key "key_to_expire" is retrieved from Redis
    Then the value of the key should not exist
