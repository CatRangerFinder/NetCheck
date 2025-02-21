import dns.resolver
import time

#TODO 1. make it resolve to DNS servers local/internet
#TODO 2. make it do network quality checks
#TODO 3. make it do internet speed tests


#Website lookup list (template: "<NAME>" (put a "," on the end of the previous entry))
website_lookup = [
    "google.com",
    "github.com"
]



#DNS server list (template: {"name": "<DISPLAY_NAME>", "address": "<IP_ADDRESS>"} (put a "," on the end of the previous entry))
dns_servers = [
    {"name": "Main Clourdflare", "address": "1.1.1.1"},
    {"name": "Aux Clourdflare", "address": "1.0.0.1"},
    {"name": "Main Google", "address": "8.8.8.8"},
    {"name": "Aux Google", "address": "8.8.4.4"}
]


#Prints list of websites
print('Current website_lookup table:')
for website in website_lookup:
    print(website)
print('-----' * 14, '\n')

resolver = dns.resolver.Resolver()
#answers = resolver.resolve('google.com', 'A')
#answers_TXT = resolver.resolve('google.com', 'TXT')

def test_dns_speed(server_name, server_address=None):
    response_time = []
    if server_address:
        resolver.nameservers = [server_address]

    #Checks DNS response times
    for website in website_lookup:
        try:
            start_time = time.time()
            resolver.resolve(website)
            end_time = time.time()
            response_time.append(end_time - start_time)
        except Exception as error:
            print(f'Error occurred while resolving {website} with {server_name}: {error}')

    #Makes an average response time
    avg = sum(response_time) / len(response_time)
    average_time = round(avg, 4)
    print(f"Average response time for {server_name}: {average_time:} seconds") #Prints out the average time for each website
    return average_time

#Test default DNS server
print('Testing Default DNS...')
default_dns_speed = test_dns_speed('Default DNS Server')
if default_dns_speed > 2:   #In case DNS response is longer than 2 seconds
    print('NOTE: Resolve time is longer than 2 seconds. This could mean primary DNS server is-\n-offline and going to the secondary DNS server.')
print('-----' * 14, '\n')
print('Testing DNS_Server_List...')

#Test all DNS servers from list
for dns_info in dns_servers:
    print(f"Testing with {dns_info['name']} DNS server...")
    list_dns_speed = test_dns_speed(dns_info['name'], dns_info['address'])

input('\nPress Enter to exit:')