import sys
import pytest

sys.path.insert(0, "d:\\solarisx\\memora")
pytest.main([
    "d:\\solarisx\\tests\\unit\\test_contradiction_detector.py",
    "d:\\solarisx\\tests\\unit\\test_experience_learner.py",
    "d:\\solarisx\\tests\\integration\\test_court_to_vault.py",
    "d:\\solarisx\\tests\\integration\\test_agent_conversation.py",
    "-v",
])
