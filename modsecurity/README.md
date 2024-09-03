ModSecurity is an open-source, cross-platform web application firewall (WAF)

main  cat /etc/modsecurity/modsecurity.conf

```
docker network create backend --subnet 10.10.10.0/24
docker network inspect backend
```

# OWASP CRS
```
# create default.conf
# create Dockerfile
$ docker build -t nginx-modsec .

$ docker run -d -it --name juice_shop --hostname juice.shop --network backend --ip 10.10.10.100 -p 3000:3000 bkimminich/juice-shop
$ docker run -d -it --name nginx-modsec --network backend --ip 10.10.10.200 -p 80:80 nginx-modsec
$ docker network inspect backend | jq ".[0].Containers"
```

# Juice Shop
curl -D - 10.10.10.100/
# Nginx Server
curl -D - 10.10.10.200:3000/
```