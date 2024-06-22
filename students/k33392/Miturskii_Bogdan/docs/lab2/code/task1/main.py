import subprocess
import pandas as pd
import sys

def run_program(command, num_threads, total):
    result = subprocess.run(command + [str(num_threads), str(total)], capture_output=True, text=True)
    output = result.stdout.strip().split(", ")
    if len(output) < 2:
        print(f"Error in output: {result.stdout}")
        return None, None
    result_value = int(output[0].split(": ")[1])
    time_taken = float(output[1].split(": ")[1].split(" ")[0])
    return result_value, time_taken

def main(num_threads, total):
    methods = {
        "Threading": ["python3", "threadingCode.py"],
        "Multiprocessing": ["python3", "multiprocessingCode.py"],
        "Async/await": ["python3", "asyncCode.py"]
    }
    
    results = []
    
    for method, command in methods.items():
        result_value, time_taken = run_program(command, num_threads, total)
        if result_value is not None and time_taken is not None:
            results.append([method, result_value, time_taken])
    
    df = pd.DataFrame(results, columns=["Method", "Result", "Time Taken (s)"])
    print(df)

if __name__ == "__main__":
    num_threads = int(sys.argv[1])
    total = int(sys.argv[2])
    main(num_threads, total)
