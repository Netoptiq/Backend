import time
import dns.resolver

def measure_response_time(dns_server, domain='example.com'):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    
    start_time = time.time()
    
    try:
        response = resolver.query(domain)
    except dns.exception.Timeout:
        return None
    
    end_time = time.time()
    
    return end_time - start_time

def rank_dns_servers(dns_servers):
    results = []

    for server in dns_servers:
        response_time = measure_response_time(server)
        if response_time is not None:
            results.append({'server': server, 'response_time': response_time})

    # Sort the results based on response time
    results.sort(key=lambda x: x['response_time'])

    return results

if __name__ == "__main__":
    # Example list of DNS servers to test
    dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']

    ranked_results = rank_dns_servers(dns_servers)

    for result in ranked_results:
        print(f"Server: {result['server']} | Response Time: {result['response_time']:.4f} seconds")
