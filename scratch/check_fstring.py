import sys

try:
    with open("services/frontend_generator.py", "r", encoding="utf-8") as f:
        content = f.read()
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Find the start and end of ops_html f-string
start_marker = 'ops_html = f"""'
end_marker = '"""'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("Could not find start of ops_html")
    sys.exit(1)

start_idx += len(start_marker)
end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("Could not find end of ops_html")
    sys.exit(1)

ops_str = content[start_idx:end_idx]

# Let's parse and count braces
print(f"Parsing ops_html string of length {len(ops_str)}...")

i = 0
n = len(ops_str)
line_no = content[:start_idx].count('\n') + 1

while i < n:
    c = ops_str[i]
    if c == '\n':
        line_no += 1
    
    if c == '{':
        if i + 1 < n and ops_str[i+1] == '{':
            # Doubled brace, skip both
            i += 2
            continue
        # Single brace is a python interpolation start. Let's scan until its closing single brace
        # We need to handle nested braces or check if they are correctly paired.
        expr_start = i
        braces_count = 1
        i += 1
        while i < n and braces_count > 0:
            if ops_str[i] == '\n':
                line_no += 1
            if ops_str[i] == '{':
                braces_count += 1
            elif ops_str[i] == '}':
                braces_count -= 1
            i += 1
        if braces_count > 0:
            print(f"Unclosed single brace starting at line {line_no}: {ops_str[expr_start:expr_start+50]}...")
        continue
        
    if c == '}':
        if i + 1 < n and ops_str[i+1] == '}':
            i += 2
            continue
        # If we see a single closing brace that wasn't matched with an opening brace, it's a syntax error!
        print(f"Error: Single closing brace '}}' at line {line_no} around: {ops_str[max(0, i-50):i+50]}")
        i += 1
        continue
    
    i += 1
