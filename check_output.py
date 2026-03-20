import os

if os.path.exists("rx.dat") and os.path.getsize("rx.dat") > 0:
    print("TEST PASS: Data received")
else:
    print("TEST FAIL: No data")
    exit(1)