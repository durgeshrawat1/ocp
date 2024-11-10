json_output='{ "request": "abc", "lease": "1", "ten": "r", "due": 5, "data": {"access_key": "key"} }'

# Extract access_key
echo "$json_output" | grep -o '"access_key"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"access_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/'
