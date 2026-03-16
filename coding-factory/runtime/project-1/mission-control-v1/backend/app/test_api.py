import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestMissionControlAPI(unittest.TestCase):
    def test_health_check(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_agent_run_low_tier(self):
        # Task that should trigger 'low' tier (FinOps optimization)
        response = client.post("/agent/run", json={"task": "Format this list of status updates"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tier"], "low")
        self.assertIn("run_id", data)

    def test_agent_run_high_tier(self):
        # Task that should trigger 'high' tier (Security/Architecture)
        response = client.post("/agent/run", json={"task": "Design a security architecture for the API"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tier"], "high")

    def test_trace_retrieval(self):
        # 1. Run a task
        run_response = client.post("/agent/run", json={"task": "Standard medium task"})
        run_id = run_response.json()["run_id"]
        
        # 2. Retrieve trace
        trace_response = client.get(f"/agent/traces/{run_id}")
        self.assertEqual(trace_response.status_code, 200)
        trace_data = trace_response.json()
        self.assertEqual(trace_data["task"], "Standard medium task")
        self.assertTrue("routing_tier" in trace_data)

if __name__ == "__main__":
    unittest.main()
