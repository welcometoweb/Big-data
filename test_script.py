from datetime import datetime

with open("test_output.txt", "a") as f:
    f.write(f"Script ran at: {datetime.now()}\n")

print("Script executed successfully")
