from peer_sources import PublicPeers, CrawledPeers
from yggdrasil_iface import YggdrasilConnection, yqq

# public = PublicPeers()
# public.perform()

# with open("peers", 'w') as f:
#     public.write(f)

ygg = YggdrasilConnection.fromServer()
ygg.query(yqq.SELF)

crawler = CrawledPeers(ygg)
crawler.perform()
with open("hosts_crawled", 'a') as f:
    crawler.write(f)
