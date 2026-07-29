import urllib.request
import urllib.parse
url = "http://127.0.0.1:8000/research?" + urllib.parse.urlencode({"q":"Type 2 diabetes treatment"})
with urllib.request.urlopen(url) as r:
    print(r.status)
    print(r.read().decode())
