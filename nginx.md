# NGINX security

```
nginx -t {-T} # проверить конфигурацию /etc/nginx/nginx.conf {+выводит сами конфигурации}
ps -ef | grep nginx # проверить работу процесов master и workers
nginx -s {stop, quit, reload, reopen} # отправить сигнал мастер процессу
```

### NGINX files and directories
/etc/nginx/nginx.conf > основной конфигурационный файл для всего сервера
/etc/nginx/conf.d/default.conf > определяет конфигурации HTTP сервера по умолчанию
/var/log/nginx/ > журнал логов

### Conf File
```
http {
    server { # определяет поведение сервера (правила предоставления контента)
        listen 80 default_server; # определяет порт для прослушивания
        server_name www.example.com; #
        
        location / { #
            root /usr/share/nginx/html; # определяет директорию предоставления HTTP контента
            # alias /usr/share/nginx/html; #
            index index.html index.htm; #
        } 
    }
}    
```
### Load balancer configuration
```
upstream backend { # директива опредяет балансировку между серверами
        server 10.10.12.45:80      weight=1; # weight определяет 
        server app.example.com:80  weight=2;
    }
```
### TCP UDP Load Balancing
```
stream { # для балансировки TPC UDP
        upstream mysql_read {
            server read1.example.com:3306  weight=5
            server read2.example.com:3306;
            server 10.10.12.34:3306 backup;
    }
}
```

# Security assessment
*     
    Why needed: 
    Vulnerable: ` #`
    Exploit: ` #`
    Secure: ` #`

* Missing Root Location   
    Why needed: определяет директорию для выдачи контента. Если не задана - выдает из /etc/nginx/
    Vulnerable: `server {root /etc/nginx/;} # no root`
    Exploit: `curl http://example.com/passwd`
    Secure: `server {root /var/www/html;}`

* Unsafe Path Restriction    
    Why needed: ограничение и политика запросов
    Vulnerable: `location = /admin { deny all; }`
    Exploit: `curl http://example.com/%61dmin /admin%00 /admin. /ADMIN`
    Secure: `location ~* ^/admin(/|$) {deny all;}`

* Unsafe Use of Variables: $uri and $document_uri
    Why needed: Используются для захвата данных из URL
    Vulnerable: `return 302 https://example.com$uri;`
    Exploit: `curl http://localhost/%0d%0aDetectify:%20clrf`
    Secure: `return 302 https://example.com$request_uri; # use $request_uri`

* Regex Vulnerabilities
    Why needed:
    Vulnerable: `location ~ /docs/([^/])? { … $1 … } # does not check for spaces`
    How safe: `location ~ /docs/([^/\s])? { … $1 … }  # not vulnerable (checks for spaces)`