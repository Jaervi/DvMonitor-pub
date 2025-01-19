import asyncio
import aioping

# Pings a single host with aioping method. Returns -1 if an error occurs, otherwise the delay in milliseconds
async def ping_device(host):
    try:
        delay = await aioping.ping(host) * 1000  # in seconds, convert to ms
        return delay
    except TimeoutError:
        return -1.0
    except Exception as e:
        return -1.0
    
# Runs the ping_device method for each address in the list and returns a tuple of the address and its delay.
async def ping_all(host_list):
    tasks = [ping_device(host) for host in host_list]
    return list(zip(host_list, await asyncio.gather(*tasks)))

# A synchronous interface method to call the ping_all method from a synchronous program
def ping_list(host_list):
    return asyncio.run(ping_all(host_list))


# Prints the list of tuples. Translates a delay of -1 to 'NO RESPONSE'
def ping_prettyPrint(data):
    for entry in sorted(data):
        address = entry[0]
        delay = entry[1]
        if(delay == -1):
            print(f'{address}: NO RESPONSE')
        else:
            print(f'{address}: {delay} ms')

# Prints an informative description from the list of tuples
def informative_print(data):
    successes = list(filter(lambda d: d[1] != -1,data))
    successtimes = list(map(lambda x: x[1],successes))
    failures =  list(filter(lambda d: d[1] == -1,data))
    average = 0
    if len(successtimes) > 0:
        average = sum(successtimes) / len(successtimes)
    print(f'\nSUCCESSFUL PINGS ({len(successes)}/{len(data)}, average: {average} ms):')
    ping_prettyPrint(successes)
    print(f'\nFAILED PINGS ({len(failures)}/{len(data)})')
    ping_prettyPrint(failures)
    print('\n')