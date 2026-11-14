import unittest
 
from llm_client import LLMClient, LLMResult
 
 
class FakeProvider:
    provider_name = "Test"
    model = "fake-model"
 
    def generate(self, prompt):
        return LLMResult(
            text="AI stands for Artificial Intelligence.",
            input_tokens=5,
            output_tokens=8
        )
 
 
class FakeLogger:
    def __init__(self):
        self.records = []
 
    def log_call(self, record):
        self.records.append(record)
        return True
 
 
class TestLLMClient(unittest.TestCase):
 
    def test_generate_and_log_usage(self):
        logger = FakeLogger()
        client = LLMClient(FakeProvider(), logger)
 
        answer = client.generate("Explain AI")
 
        self.assertEqual(
            answer,
            "AI stands for Artificial Intelligence."
        )
        self.assertEqual(len(logger.records), 1)
        self.assertEqual(logger.records[0]["total_tokens"], 13)
        self.assertEqual(logger.records[0]["status"], "success")
 
 
if __name__ == "__main__":
    unittest.main()
