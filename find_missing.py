import re
text = open('test_results.txt', 'rb').read().decode('utf-16le', errors='replace')
print("MISSING FIXTURES:")
print(set(re.findall(r"fixture '(\w+)' not found", text)))
