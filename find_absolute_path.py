import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
print("absolute path", abs_path)
