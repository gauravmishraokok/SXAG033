import sys
import traceback

sys.path.insert(0, "d:\\solarisx\\memora")

files_to_import = [
    "tests.unit.test_contradiction_detector",
    "tests.unit.test_experience_learner",
    "tests.integration.test_court_to_vault",
    "tests.integration.test_agent_conversation",
]

for f in files_to_import:
    try:
        print(f"Importing {f}...")
        __import__(f)
    except Exception as e:
        print(f"Failed to import {f}")
        traceback.print_exc()
        break
