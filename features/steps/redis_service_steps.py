from service_under_test.redis_docker import RedisDocker
from behave import given, when, then

@given("a Redis service is not running")
def step_redis_not_running(context):
    context.redis_service = RedisDocker()
    context.redis_service.stop()

@when("start a Redis service")
def step_start_redis(context):
    context.redis_service.start()

@then('the Redis should be running')
def step_redis_status(context):
    status = context.redis_service.status()
    assert status, f"Service is not running"