import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    # 1. Register User 1
    print("Registering User 1...")
    response = requests.post(f"{BASE_URL}/register", json={"username": "user1", "email": "user1@example.com", "password": "password123"})
    if response.status_code not in [200, 400]: # 400 if already exists
        print(f"Failed to register user1: {response.text}")
        return False
    print("User 1 registered or already exists.")

    # 2. Login User 1
    print("Logging in User 1...")
    response = requests.post(f"{BASE_URL}/token", data={"username": "user1", "password": "password123"})
    if response.status_code != 200:
        print(f"Failed to login user1: {response.text}")
        return False
    token1 = response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    print("User 1 logged in.")

    # 3. Create Task for User 1
    print("Creating Task 1 for User 1...")
    response = requests.post(f"{BASE_URL}/tasks/", json={"title": "Task 1", "description": "Do something"}, headers=headers1)
    if response.status_code != 200:
        print(f"Failed to create task: {response.text}")
        return False
    task1_id = response.json()["id"]
    print(f"Task 1 created with ID {task1_id}")

    # 4. Get Tasks for User 1
    print("Getting tasks for User 1...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers1)
    if response.status_code != 200:
        print(f"Failed to get tasks: {response.text}")
        return False
    tasks = response.json()
    if len(tasks) < 1:
        print("Expected at least 1 task for User 1")
        return False
    print(f"User 1 has {len(tasks)} tasks.")

    # 5. Register User 2
    print("Registering User 2...")
    requests.post(f"{BASE_URL}/register", json={"username": "user2", "email": "user2@example.com", "password": "password123"})
    
    # 6. Login User 2
    print("Logging in User 2...")
    response = requests.post(f"{BASE_URL}/token", data={"username": "user2", "password": "password123"})
    token2 = response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # 7. Verify User 2 sees no tasks (or at least not User 1's)
    print("Getting tasks for User 2...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers2)
    tasks2 = response.json()
    # Note: user2 might have tasks from previous runs if not cleaned up, but shouldn't have task1_id
    user2_task_ids = [t["id"] for t in tasks2]
    if task1_id in user2_task_ids:
        print("Security Flaw: User 2 can see User 1's task!")
        return False
    print("User 2 cannot see User 1's task. Auth Check Passed.")

    # 8. User 2 tries to delete User 1's task
    print("User 2 trying to delete User 1's task...")
    response = requests.delete(f"{BASE_URL}/tasks/{task1_id}", headers=headers2)
    if response.status_code != 403:
        print(f"Expected 403, got {response.status_code}. Security Flaw!")
        return False
    print("User 2 blocked from deleting User 1's task.")

    # 9. User 1 deletes their task
    print("User 1 deleting Task 1...")
    response = requests.delete(f"{BASE_URL}/tasks/{task1_id}", headers=headers1)
    if response.status_code != 200:
        print(f"Failed to delete task: {response.text}")
        return False
    print("User 1 deleted task successfully.")

    print("\nALL TESTS PASSED!")
    return True

if __name__ == "__main__":
    if test_api():
        sys.exit(0)
    else:
        sys.exit(1)
