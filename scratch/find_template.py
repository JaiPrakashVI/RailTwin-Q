with open('services/frontend_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '        ops_html = f"""'
end_marker = '        cls._safe_write("frontend/operations.html", ops_html)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

line_before = content[:start_idx].count('\n')
line_end = content[:end_idx].count('\n')
print(f'ops_html template spans lines {line_before+1} to {line_end+1}')

# Show 10 chars around end to see what the closing looks like
print(repr(content[end_idx-50:end_idx]))
