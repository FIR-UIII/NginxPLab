# NGINX basics

```
nginx -t {-T} # проверить конфигурацию /etc/nginx/nginx.conf {+выводит сами конфигурации}
ps -ef | grep nginx # проверить работу процесов master и workers
nginx -s {stop, quit, reload, reopen} # отправить сигнал мастер процессу
```

### NGINX files and directories
/etc/nginx/nginx.conf > основной конфигурационный файл для всего сервера
/etc/nginx/conf.d/default.conf > определяет конфигурации HTTP сервера по умолчанию
/var/log/nginx/ > журнал логов

### Default configuration
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

### Regex
|regex|explanaitions|
|----:|:------------|
|`~`  |case-sensitive|
|`~*` |case-insensitive|
|`=`  |   exactly match|
|`.(png|ico|gif|jpg|jpeg|css|js)$`|match all file types|
|`^~` |  |
|     |  |

# Authentication
HTTP Basic Authentication
```
location / {
        auth_basic          "Private site";
        auth_basic_user_file conf.d/passwd;
    }
```
JWT
```
location /api/ {
        auth_jwt          "api";
        auth_jwt_key_file conf/keys.json;
    }
```
# Authorization / ACL
Запрет по location URL. Правила пишутся по логиге iptables
```
    location /admin {
            deny  10.0.0.1;
            allow 10.0.0.0/20;
            deny all;
    }
```

# HTTP heades
CORS
```
location / {
    add_header 'Access-Control-Allow-Origin' 
        '*.example.com';
    add_header Strict-Transport-Security max-age=31536000;
    }
```

# Session managment

# Secret managment / Cache

# TLS
Client-Side Encryption for whole application
```
http { # All directives used below are also valid in stream
        server {
            listen 8433 ssl;
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_ciphers HIGH:!aNULL:!MD5;
            ssl_certificate /etc/nginx/ssl/example.pem;
            ssl_certificate_key /etc/nginx/ssl/example.key;
            ssl_certificate /etc/nginx/ssl/example.ecdsa.crt;
            ssl_certificate_key /etc/nginx/ssl/example.ecdsa.key;
            ssl_session_cache shared:SSL:10m;
            ssl_session_timeout 10m;
} }
```

Upstream Encryption for URL path
```
location / {
        proxy_pass https://upstream.example.com;
        proxy_ssl_verify on;
        proxy_ssl_verify_depth 2;
        proxy_ssl_protocols TLSv1.2;
    }
```

# Logs

# Security assessment and misconfigurations
* <br>
    Why needed: <br>
    Vulnerable: ` #` <br>
    Exploit: ` #` <br>
    Secure: ` #` <br>

* No limits<br>
    Why needed: Ограничение лимитов траффика<br>
    Vulnerable: `if none` <br>
    Exploit: ` #` <br>
    Secure: 
    ```
    client_body_buffer_size <= 1M
    client_max_body_size <= 1M
    large_client_header_buffers_size <= 10K
    ```<br>

* Security misconfiguration<br>
    Why needed: исключает стандартные ошибки<br>
    Vulnerable: `if none` <br>
    Exploit: ` #` <br>
    Secure: 
    ```
    ssl on;
    listen <port> ssl;
    ssl_protocols ssl_ciphers ...;
    ssl_stampling on;
    server_tokens off;
    $request_method
    add_header X-Frame-Options sameorigin; X-XSS-Protection 1;
    access_log on;
    ```<br>

* proxy_set_header Upgrade & Connection <br>
    Why needed: proxy_set_header directive is often used to customize the headers that are sent to a proxied server.<br>
    Vulnerable: 
    ```
    location / {
        proxy_pass http://backend:9999;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade; # forwards the Upgrade header from the client to the backend server.
        proxy_set_header Connection $http_connection; # forwards the Connection header
    }
    ```
    Exploit: `curl -k -v -X GET https://localhost/ -H "Upgrade: h2c" -H "Connection: Upgrade, HTTP2-Settings"`
    Secure: # remove it 
    ```
    location / {
        proxy_pass http://backend:9999;
        proxy_http_version 1.1;
    }
    ```

* proxy_pass and internal Directives
    Why needed: The proxy_pass directive is used to forward requests to another server, while the internal directive ensures that certain locations are only accessible within Nginx
    Vulnerable: `location /internal/ {internal; proxy_pass http://backend/internal/;}`
    Exploit: `curl "http://example.com/internal/private-data"`
    Secure: `add location /public/ {proxy_pass http://backend/public/;}`

* DNS Spoofing Vulnerability
    Why needed: 
    Vulnerable: `resolver 8.8.8.8;`
    Exploit: ` #`
    Secure: `resolver 127.0.0.1; #Additionally, ensure DNSSEC is used to validate DNS responses.`

* map Directive Default Value
    Why needed: used to map one value to another, frequently for controlling access or other logic
    Vulnerable: `map $uri $mappocallow {/map-poc/private 0;}`
    Exploit: `curl "http://example.com/map-poc/undefined"`
    Secure: `map $uri $mappocallow {default 0;} #Always specify a default value in the map directive:`

* X-Accel-Redirect: /.env
    Why needed: 
    Vulnerable: ` #`
    Exploit: `curl -I "http://example.com" -H "X-Accel-Redirect: /.env"`
    Secure: ` #`

* merge_slashes set to off
    Why needed: By default, Nginx's merge_slashes directive is set to on
    Vulnerable: ` #`
    Exploit: `http://example.com//etc/passwd`
    Secure: `http {merge_slashes off;}#`

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