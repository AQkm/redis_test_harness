from behave import then

@then('the value of the key should be "{expected_value}"')
def step_assert_value(context, expected_value):
    assert context.result == expected_value, f"Expected '{expected_value}', but got '{context.result}'"

@then("the value of the key should not exist")
def step_assert_value_not_exist(context):
    assert context.result is None, "Expected value to not exist, but it was found"

@then("the replica should have been promoted to primary")
def step_replica_promoted(context):
    assert context.redis_service.is_replica_promoted_to_primary(), "Replica was not promoted to primary"

@then("the restarted node should have rejoined as a replica")
def step_restarted_node_as_replica(context):
    assert context.redis_service.is_node_rejoined_as_replica(), "Restarted node did not rejoin as a replica"
