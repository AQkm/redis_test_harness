from behave import when
import time

@when('a key "{key}" is set with value "{value}" in Redis')
def step_set_key(context, key, value):
    context.redis_service.set_key(key, value)

@when('a key "{key}" is set with value "{value}" with expiration of {seconds} seconds')
def step_set_key_with_expiration(context, key, value, seconds):
    context.redis_service.set_key(key, value, expiration=int(seconds))

@when('a key "{key}" is retrieved from Redis')
def step_get_key(context, key):
    context.result = context.redis_service.get_key(key)

@when("the Redis container is restarted")
def step_restart_redis(context):
    context.redis_service.restart()

@when("the primary node is failed")
def step_fail_primary_node(context):
    context.redis_service.fail_primary_node()

@when("the failed node is restarted")
def step_restart_failed_node(context):
    context.redis_service.restart_failed_node()

@when("a wait of {seconds} seconds is performed")
def step_wait_seconds(context, seconds):
    time.sleep(int(seconds))
