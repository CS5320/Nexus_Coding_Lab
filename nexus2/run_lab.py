"""Runs the lab contract with Python 3.11+, no third-party dependencies."""
from pathlib import Path
import sys, unittest
if sys.version_info < (3,11):
    raise SystemExit("Use Python 3.11 or newer.")
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/"src"))
sys.path.insert(0,str(root/"lab"))
suite=unittest.defaultTestLoader.discover(str(root/"lab"),pattern="test_contract.py")
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
