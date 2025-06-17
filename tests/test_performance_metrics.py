# tests/test_performance_metrics.py
import time
from assistant.main import process_user_input

def test_openai_latency():
    input_text = "What is the capital of France?"
    start = time.time()
    process_user_input(input_text)
    end = time.time()
    latency = end - start
    assert latency < 4, f"Response took too long: {latency:.2f}s"
