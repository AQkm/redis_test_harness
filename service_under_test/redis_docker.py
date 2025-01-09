import docker
import time
import redis
import docker.errors

class RedisDocker:
    def __init__(self, container_name="redisToTest", image="redis:latest", port=7874):
        self.container_name = container_name
        self.image = image
        self.port = port
        self.client = docker.from_env()

    def start(self):
        try:
            print(f"Starting")
            container = self.client.containers.run(
                self.image,
                detach=True,
                name=self.container_name,
                ports={"7874/tcp": self.port},
            )
            for _ in range(5):
                print(f"Witing for {self.container_name} container")
                if self.status(): break
                print(".")
                time.sleep(1)
            if self.status():
                print(f"{self.container_name} container is running.")
                return container
            else:
                print(f"{self.container_name} container have been not started.")
        except docker.errors.APIError as e:
            print(f"Error starting Redis container: {e}")
            return None

    def status(self):
        try:
            container = self.client.containers.get(self.container_name)
            return container.status == 'running'
        except docker.errors.NotFound:
            print(f"{self.container_name} not found")

    def stop(self):
        try:
            print(f"Stopping {self.container_name} container.")
            container = self.client.containers.get(self.container_name)
            container.stop()
            print(f"{self.container_name} stopped")
            container.remove()
            print(f"{self.container_name} removed")
        except docker.errors.NotFound:
            print(f"{self.container_name} container not found.")
        except docker.errors.APIError as e:
            print(f"Error stopping and removing container {e}")

    def get_cluster_status(self):
        try:
            info = self.redis_client.info("replication")
            primary = info["role"] == "master"
            replicas = info.get("connected_slaves", 0)
            return {
                "primary": primary,
                "replicas": replicas
            }
        except redis.ConnectionError:
            print("Unable to connect to Redis instance for cluster status.")
            return None

    def fail_primary_node(self):
        try:
            print(f"Simulating failure of the primary node: {self.container_name}")
            self.stop()
        except Exception as e:
            print(f"Error failing primary node: {e}")

    def restart_failed_node(self):
        try:
            print(f"Restarting failed node: {self.container_name}")
            self.start()
        except Exception as e:
            print(f"Error restarting failed node: {e}")

    def set_key(self, key, value, expiration=None):
        try:
            if expiration:
                self.redis_client.setex(key, expiration, value)
            else:
                self.redis_client.set(key, value)
        except redis.ConnectionError as e:
            print(f"Error setting key in Redis: {e}")

    def get_key(self, key):
        try:
            return self.redis_client.get(key)
        except redis.ConnectionError as e:
            print(f"Error getting key from Redis: {e}")
            return None

    def is_replica_promoted_to_primary(self):
        try:
            cluster_status = self.get_cluster_status()
            return cluster_status["primary"]
        except Exception as e:
            print(f"Error checking replica promotion: {e}")
            return False

    def is_node_rejoined_as_replica(self):
        try:
            cluster_status = self.get_cluster_status()
            return cluster_status["replicas"] > 0
        except Exception as e:
            print(f"Error checking node rejoin status: {e}")
            return False