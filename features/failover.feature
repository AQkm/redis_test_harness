Feature: Failover scenarios
  Validates Redis behavior under failover conditions in a clustered setup.

  Scenario: Replica is promoted to primary when primary fails
    Given a Redis cluster with one primary and one replica
    When the primary node is failed
    Then the replica should have been promoted to primary

  Scenario: Failed node rejoins as a replica after recovery
    Given a Redis cluster with one primary and one replica
    When the primary node is failed
    And the failed node is restarted
    Then the restarted node should have rejoined as a replica