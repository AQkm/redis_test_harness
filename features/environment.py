from service_under_test.redis_docker import RedisDocker

def before_scenario(context, scenario):
    print(f"\n- Before scenario: {scenario.name}")
    context.redis_service = RedisDocker()

def after_scenario(context, scenario):
    print(f"- After scenario: {scenario.name}")
    if hasattr(context, "redis_service"):
        context.redis_service.stop()
    context.redis_service.stop_cluster_nodes()