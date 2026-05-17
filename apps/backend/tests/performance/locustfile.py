import os
import random

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()


class CatalogUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def find_coins(self) -> None:
        authorities = ["Theodosius I", "Valentinian I", "Licinius"]
        metals = ["Gold", "Silver", "Bronze"]
        mints = ["Rome", "Nicomedia", "Ticinum", "Cyzicus"]
        authority = random.choice(authorities)
        metal = random.choice(metals)
        mint = random.choice(mints)
        prompt = f"Searching for {authority} coins made of {metal} from {mint}"
        with self.client.get(
            "/catalog",
            params={"search": prompt},
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to search coins: {prompt}")

    def on_start(self) -> None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        body = {"login": username, "password": password}
        with self.client.post(
            "/auth/sign-in",
            json=body,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.client.headers.update({"Authorization": f"Bearer {self.token}"})
            else:
                response.failure("Failed to authenticate")
