import requests
import time

url = 'https://api.example.com/endpoint'
headers = {'Authorization': 'Bearer YOUR_TOKEN'}
methods = ['GET', 'POST', 'PUT', 'DELETE']  # List of HTTP methods to test

# Initialize dictionary to store results per method
results = {method: {'request_count': 0, 'successful_requests': 0, 'rate_limit_hit': False} for method in methods}

print("Starting API Rate Limiting Test for Multiple HTTP Methods...\n")

for method in methods:
    print(f"\nTesting Rate Limiting for {method} requests:")
    
    for i in range(1000):
        # Send request based on method type
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json={"data": "test"})
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json={"data": "test"})
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        # Track requests and status codes
        results[method]['request_count'] += 1
        print(f"{method} Request {i+1}: Status Code {response.status_code}")
        
        # Check for rate limiting
        if response.status_code == 429:
            print(f"Rate limit exceeded for {method} method.")
            results[method]['rate_limit_hit'] = True
            break  # Stop testing this method if rate limit is hit
        else:
            results[method]['successful_requests'] += 1
        
        # Delay to control request rate
        time.sleep(0.1)

# Print a summary report for each HTTP method
print("\n--- Rate Limiting Test Summary ---")
for method in methods:
    print(f"\nMethod: {method}")
    print(f"Total Requests Sent: {results[method]['request_count']}")
    print(f"Successful Requests (Non-429): {results[method]['successful_requests']}")
    if results[method]['rate_limit_hit']:
        print(f"Rate Limit Triggered After {results[method]['request_count']} Requests")
    else:
        print("Rate Limit Not Triggered")
print("-----------------------------------")
