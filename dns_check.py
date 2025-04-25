import time

import dns.resolver

# Website lookup list (template: "<NAME>" (put a "," on the end of the previous entry))
website_lookup = [
    "google.com",
    "github.com"
]

# DNS server list (template: {"name": "<DISPLAY_NAME>", "address": "<IP_ADDRESS>"}
# (put a "," on the end of the previous entry))
dns_servers = [
    {"name": "Main Cloudflare", "address": "1.1.1.1"},
    {"name": "Aux Cloudflare", "address": "1.0.0.1"},
    {"name": "Main Google", "address": "8.8.8.8"},
    {"name": "Aux Google", "address": "8.8.4.4"}
]

resolver = dns.resolver.Resolver()


# answers = resolver.resolve('google.com', 'A')
# answers_TXT = resolver.resolve('google.com', 'TXT')

def test_dns_speed(server_name, server_address=None):
    response_time = []

    # Create a new resolver instance to avoid global state issues
    resolver = dns.resolver.Resolver()

    if server_address:
        resolver.nameservers = [server_address]

    for website in website_lookup:
        try:
            start_time = time.time()
            resolver.resolve(website)
            end_time = time.time()
            response_time.append(end_time - start_time)
        except Exception as error:
            print(f'Error occurred while resolving {website} with {server_name}: {error}')

    if response_time:
        avg = sum(response_time) / len(response_time)
        average_time = round(avg, 4)
        print(f"Average response time for {server_name}: {average_time} seconds")
        return average_time
    else:
        print(f"No successful responses for {server_name}. Cannot compute average.")
        return None


if __name__ == '__main__':

    print('Current website_lookup table:')
    for website in website_lookup:
        print(f'\u001b[32m{website}\u001b[0m')
    print('-----' * 14, '\n')

    print('Testing Default DNS...')
    default_dns_speed = test_dns_speed('Default DNS Server')

    if default_dns_speed is not None and default_dns_speed > 2:
        print('\u001b[43mNOTE: Resolve time is longer than 2 seconds. This could mean primary DNS server is-\u001b[0m')
        print('\u001b[43m-offline and going to the secondary DNS server.\u001b[0m')
    print('-----' * 14, '\n')

    print('Testing DNS_Server_List...')
    for dns_info in dns_servers:
        print(f"Testing with {dns_info['name']} DNS server...")
        test_dns_speed(dns_info['name'], dns_info['address'])

    input('\nPress Enter to exit:')
