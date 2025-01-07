from service_under_test.redis_docker import RedisDocker

redis_service = RedisDocker()
redis_service.start()
if redis_service.status():
    print("Nice! Redis service is ready for testing.")
redis_service.stop()
redis_service.status()


