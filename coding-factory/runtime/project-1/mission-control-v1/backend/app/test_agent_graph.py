import unittest
from agent_graph import graph, AgentState

class TestAgentGraph(unittest.TestCase):
    def test_routing_logic(self):
        # Test Low Tier
        state_low = {"task": "Format this list of status updates", "plan": [], "current_step": 0, "worker_output": None, "validation_passed": False, "confidence_score": 0.0, "retry_count": 0, "routing_tier": "medium"}
        output_low = graph.invoke(state_low)
        self.assertEqual(output_low["routing_tier"], "low")

        # Test High Tier
        state_high = {"task": "Design a security architecture for a multi-tenant DB", "plan": [], "current_step": 0, "worker_output": None, "validation_passed": False, "confidence_score": 0.0, "retry_count": 0, "routing_tier": "medium"}
        output_high = graph.invoke(state_high)
        self.assertEqual(output_high["routing_tier"], "high")

    def test_full_execution_flow(self):
        state = {
            "task": "Test full pipeline",
            "plan": [],
            "current_step": 0,
            "worker_output": None,
            "validation_passed": False,
            "confidence_score": 0.0,
            "retry_count": 0,
            "routing_tier": "medium"
        }
        final_state = graph.invoke(state)
        self.assertTrue(len(final_state["plan"]) > 0)
        self.assertTrue(final_state["validation_passed"])
        self.assertIsNotNone(final_state["worker_output"])

if __name__ == "__main__":
    unittest.main()
