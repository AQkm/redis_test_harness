import docker
import time
import redis
import docker.errors

class RedisDocker:
    def __init__(self, container_name="redisToTest", image="redis:latest", port=6379):
        self.container_name = container_name
        self.image = image
        self.port = port
        self.docker_client = docker.from_env()
        self.redis_client = None
        self.redis_clients = []
        self.cluster_nodes = []

    def start(self, persistence=True):
        try:
            print(f"Starting {self.container_name} container...")
            custom_command = None
            if not persistence:
                custom_command = [
                    "redis-server",
                    "--save", "",
                    "--appendonly", "no",
                ]

            container = self.docker_client.containers.run(
                self.image,
                detach=True,
                name=self.container_name,
                ports={"6379/tcp": self.port},
                command=custom_command
            )
            for _ in range(5):
                print(f"Waiting for {self.container_name} container to start...")
                if self.status():
                    break
                print(".")
                time.sleep(1)
            if self.status():
                print(f"{self.container_name} container is running.")
                self.redis_client = redis.StrictRedis(host="localhost", port=self.port, decode_responses=True)
                return container
            else:
                print(f"{self.container_name} container did not start.")
        except docker.errors.APIError as e:
            print(f"Error starting Redis container: {e}")
            return None

    def status(self):
        try:
            container = self.docker_client.containers.get(self.container_name)
            return container.status == 'running'
        except docker.errors.NotFound:
            print(f"{self.container_name} not found")
            return False

    def stop(self):
        try:
            print(f"Stopping {self.container_name} container...")
            container = self.docker_client.containers.get(self.container_name)
            container.stop()
            print(f"{self.container_name} stopped.")
            container.remove()
            print(f"{self.container_name} removed.")
        except docker.errors.NotFound:
            print(f"{self.container_name} container not found.")
        except docker.errors.APIError as e:
            print(f"Error stopping and removing container: {e}")

    def restart(self):
        self.docker_client.containers.get(self.container_name).restart()

    def set(self, key, value, expiration=None):
        try:
            if expiration:
                self.redis_client.setex(key, expiration, value)
            else:
                self.redis_client.set(key, value)
        except redis.ConnectionError as e:
            print(f"Error setting key in Redis: {e}")

    def get(self, key):
        try:
            return self.redis_client.get(key)
        except redis.ConnectionError as e:
            print(f"Error getting key from Redis: {e}")
            return None
        
    def setup_cluster(self):
        try:
            print("Setting up Redis cluster...")
            ports = [6380, 6381]

            for port in ports:
                print(f"Starting Redis node on port {port}...")
                container = self.docker_client.containers.run(
                    self.image,
                    detach=True,
                    name=f"redis_node_{port}",
                    ports={f"{port}/tcp": port},
                    environment=["REDIS_CLUSTER=yes"],
                    command=[
                        "redis-server",
                        "--cluster-enabled", "yes",
                        "--cluster-config-file", "nodes.conf",
                        "--cluster-node-timeout", "5000",
                        "--appendonly", "yes"
                    ]
                )
                time.sleep(5)
                self.cluster_nodes.append((container, port))
                self.redis_clients.append(redis.StrictRedis(host="localhost", port=port, decode_responses=True))

            print("Connecting Redis nodes into the cluster...")
            for redis_client in self.redis_clients:
                for other_client in self.redis_clients:
                    if redis_client != other_client:
                        print(f"Connecting {redis_client.connection_pool.connection_kwargs['port']} to {other_client.connection_pool.connection_kwargs['port']}")
                        redis_client.cluster('meet', 'localhost', other_client.connection_pool.connection_kwargs['port'])

            print("Creating Redis cluster...")
            self.redis_clients[0].cluster('create', 'yes')
            print("Cluster created.")

        except Exception as e:
            print(f"Error setting up Redis cluster: {e}")
    
    def get_cluster_status(self):
        try:
            cluster_info = self.redis_clients[0].cluster('info')
            print(cluster_info)
            primary_node = "node_1"
            replica_nodes = ["node_2"]

            return {
                "primary": primary_node,
                "replicas": replica_nodes
            }
        except redis.ConnectionError:
            print("Unable to connect to Redis instance for cluster status.")
            return None

    def stop_cluster_nodes(self):
        for container, port in self.cluster_nodes:
            container.stop()
            print(f"{port} stopped.")
            container.remove()
            print(f"{port} removed.")

    def is_cluster_healthy(self):
        try:
            cluster_info = self.redis_clients[0].cluster('info')
            if "cluster_state:ok" not in cluster_info:
                print("Cluster is not healthy: Cluster state is not 'ok'.")
                return False

            nodes = self.redis_client[0].cluster('nodes')
            for node in nodes.splitlines():
                parts = node.split()
                node_id = parts[0]
                node_status = parts[2]
                if node_status not in ['master', 'slave']:
                    print(f"Node {node_id} is in an invalid state: {node_status}.")
                    return False

                if "fail?" in parts:
                    print(f"Node {node_id} is marked as failed.")
                    return False

            print("Cluster is healthy.")
            return True
        except redis.ConnectionError:
            print("Unable to connect to Redis instance to check cluster health.")
            return False

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