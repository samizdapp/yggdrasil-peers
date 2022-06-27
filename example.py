from peer_sources import PublicPeers, CrawledPeers
from yggdrasil_iface import YggdrasilConnection, yqq

# public = PublicPeers()
# public.perform()

# with open("peers", 'w') as f:
#     public.write(f)

print('connect server', True)
ygg = YggdrasilConnection.fromServer()
print("query self", True)
ygg.query(yqq.SELF)

try:
    with open("hosts_crawled", 'r') as file:
        lines = file.readlines()
        keys = [line.rstrip().split(' ').pop().split('.')[1] + line.rstrip().split(' ').pop().split('.')[2] for line in lines]
        file.close()
        if len(keys) == 0:
            raise 0
        print('bootstrap from previously crawled')
except:
    print('get neighbors')
    keys = [data["key"] for data in ygg.neighbours.values()]

print('make crawler', keys)
crawler = CrawledPeers(ygg, keys)
print('do perform')
crawler.perform()
print('do open', True) 
with open("hosts_crawled", 'w') as f:
    crawler.write(f)
