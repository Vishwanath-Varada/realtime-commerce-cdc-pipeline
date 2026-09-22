from locust import HttpUser, task, between
import random


class CommerceUser(HttpUser):

    # Each simulated user waits 0.05–0.20 seconds
    # before sending the next transaction
    wait_time = between(0.05, 0.20)

    @task
    def create_transaction(self):

        transaction = {
            "customer_id": random.randint(1, 100000),
            "product_id": random.randint(1, 1000),
            "quantity": random.randint(1, 5),
            "amount": round(random.uniform(20.00, 2000.00), 2)
        }

        with self.client.post(
            "/transactions",
            json=transaction,
            name="/transactions",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()

            else:
                response.failure(
                    f"Transaction failed: {response.status_code}"
                )