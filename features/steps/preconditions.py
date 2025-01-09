from service_under_test.redis_docker import RedisDocker
from behave import given

@given("the Redis container is running")
def step_redis_running(context):
    context.redis_service = RedisDocker()
    context.redis_service.start()
    assert context.redis_service.status() == True, "Redis container is not running"

@given("the Redis container is not running")
def step_redis_not_running(context):
    context.redis_service = RedisDocker()
    context.redis_service.stop()
    assert context.redis_service.status() == False, "Redis container is still running"

@given("a Redis cluster with one primary and one replica")
def step_redis_cluster_setup(context):
    context.redis_service = RedisDocker()
    context.redis_service.setup_cluster()
    assert context.redis_service.is_cluster_healthy(), "Redis cluster is not healthy"
