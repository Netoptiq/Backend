import urllib.parse, http.client

p = { 'key': 'F3A012DBDB764E07E4AD8B0D3C57A167', 'domain': 'Enter_Domain_Name', 'format': 'json' }

conn = http.client.HTTPSConnection("api.ip2whois.com")
conn.request("GET", "/v2?" + urllib.parse.urlencode(p))
res = conn.getresponse()
print res.read()