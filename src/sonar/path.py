import os

print(f"__file__ is: {__file__}")
print(f"dirname is: {os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}")
