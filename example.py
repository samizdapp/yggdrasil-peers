from peer_sources import PublicPeers, CrawledPeers
from yggdrasil_iface import YggdrasilConnection, yqq

public = PublicPeers()
public.perform()

with open("peers", 'w') as f:
    public.write(f)

ygg = YggdrasilConnection.fromServer("192.168.1.127")
ygg.query(yqq.SELF)

crawler = CrawledPeers(ygg)
# crawler.perform()
with open("hosts", 'a') as f:
    crawler.write(f)
