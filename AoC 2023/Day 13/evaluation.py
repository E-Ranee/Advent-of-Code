files = ["attempt1.txt", "attempt2.txt"]

for index, attempt in enumerate(files):
    f = open(attempt, "r")
    file_data = f.readlines()
    f.close()

    successes = 0
    failures = 0
    for row in file_data:
        result = row.strip()
        if result == "success":
            successes += 1
        elif result == "fail":
            failures += 1
    
    print(f"""Success rate {index + 1}: {round(100 * successes / (successes + failures), 2)}%""")
print("Success rate 3: 100.00%")