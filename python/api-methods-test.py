import http.client
from urllib.parse import urlparse
from datetime import datetime

# Configurable parameters
BASE_URL = "https://api.example.com"  # Set your base URL here
ENDPOINTS = ["/path1", "/path2"]  # Add your endpoints here

# Bearer token you already have
ACCESS_TOKEN = "your_access_token_here"

# HTTP methods to test, including all standard ones
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "CONNECT", "TRACE", "PROPFIND"]

def check_allowed_methods(base_url, endpoint, methods, token):
    allowed_methods = []
    parsed_url = urlparse(base_url)
    conn = http.client.HTTPSConnection(parsed_url.netloc) if parsed_url.scheme == "https" else http.client.HTTPConnection(parsed_url.netloc)
    
    for method in methods:
        try:
            # Construct request headers with Authorization
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Make the request
            conn.request(method, endpoint, headers=headers)
            response = conn.getresponse()
            
            # Check if the method is allowed based on response status code
            if response.status != 405:  # HTTP 405 means 'Method Not Allowed'
                allowed_methods.append(method)
            
            # Read and close response
            response.read()
        except Exception as e:
            print(f"Error for {method} on {base_url}{endpoint}: {e}")
    
    conn.close()
    return allowed_methods

def generate_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"http_methods_report_{timestamp}.txt"
    
    with open(report_file, "w") as file:
        file.write(f"HTTP Methods Allowed Report\n")
        file.write(f"Generated on: {datetime.now()}\n")
        file.write("=" * 50 + "\n\n")
        
        for endpoint, allowed_methods in results.items():
            file.write(f"Endpoint: {endpoint}\n")
            file.write("Allowed HTTP Methods:\n")
            if allowed_methods:
                for method in allowed_methods:
                    file.write(f"  - {method}\n")
            else:
                file.write("  None\n")
            file.write("\n" + "=" * 50 + "\n\n")
    
    print(f"Report generated: {report_file}")

# Main function to perform tests and generate report
def main(base_url, endpoints, methods, token):
    results = {}
    for endpoint in endpoints:
        print(f"Testing endpoint: {endpoint}")
        allowed_methods = check_allowed_methods(base_url, endpoint, methods, token)
        results[endpoint] = allowed_methods
    
    # Generate report with the results
    generate_report(results)

# Run the script
if __name__ == "__main__":
    main(BASE_URL, ENDPOINTS, HTTP_METHODS, ACCESS_TOKEN)
