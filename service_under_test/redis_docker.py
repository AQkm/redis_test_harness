import docker
import time
import argparse

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