import ipaddress
import typing 
from .. import Http

#print("load " + __file__.split('/')[-1])

def GetPublicIP(HttpProxy:str=None) -> str:
    servers = [
        "http://ifconfig.me",
        "http://icanhazip.com",
        "http://ipinfo.io/ip",
        "http://api.ipify.org",
        "http://ident.me",
        "http://ipecho.net/plain",
    ]

    for s in servers:
        try:
            resp = Http.Get(s, Headers={"User-Agent": "curl/7.79.1"}, HttpProxy=HttpProxy)
            if resp.StatusCode != 200:
                continue
            else:
                return resp.Content.strip()
        except:
            pass 
    
    raise Exception("找不到公网IP, 可能是没有联网?")

#print("load " + __file__.split('/')[-1])

def IP2Int(ip:str) -> int:
    return int(ipaddress.IPv4Address(ip))

def Int2IP(intip:int) -> str:
    return str(ipaddress.IPv4Address(intip))

def GetIPRange(cidr: str) -> typing.Tuple[str, str]:
    try:
        # 判断是否为IPv4
        if ":" in cidr:
            network = ipaddress.IPv6Network(cidr, strict=False)
        else:
            network = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError as e:
        return str(e), str(e)
    
    # 获取起始IP地址
    start_ip = network.network_address
    # 获取结束IP地址
    end_ip = network.broadcast_address
    
    return str(start_ip), str(end_ip)

if __name__ == "__main__":
    print(IP2Int("192.168.0.1"))
    print(Int2IP(3232235521))

    print(GetIPRange("2404:2280:10b::/48"))
    print(GetIPRange('39.108.0.0/16'))