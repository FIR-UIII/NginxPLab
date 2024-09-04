### Regex
|regex|explanaitions|
|----:|:------------|
|`~`  |case-sensitive|
|`~*` |case-insensitive|
|`=`  |   exactly match|
|`.(png\|ico\|gif\|jpg\|jpeg\|css\|js)$`|match all file types|
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

# HTTP security headers
CORS
```
location / {
    add_header 'Access-Control-Allow-Origin' 
        '*.example.com';
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self';" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    }
```

# Session managment

# Secret managment / Cache

# TLS
Client-Side Encryption for whole application
```
http { # All directives used below are also valid in stream
        server {
            listen 433 ssl;
            server_name example.com;
            ssl_certificate /etc/nginx/ssl/nginx.crt;
            ssl_certificate_key /etc/nginx/ssl/nginx.key;
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
            ssl_prefer_server_ciphers on;
            ssl_session_cache shared:SSL:10m;
            ssl_session_timeout 10m;
            location / <...>}
        server {
            listen 80; # Redirect HTTP to HTTPS
            server_name example.com;
            return 301 https://$host$request_uri;}
}
```

### Upstream Encryption for URL path
```
location / {
        proxy_pass https://upstream.example.com;
        proxy_ssl_verify on;
        proxy_ssl_verify_depth 2;
        proxy_ssl_protocols TLSv1.2;
    }
```

# Rate Limiting
```
# Limits requests to 10 per second, with a burst of 5 requests allowed
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
    server {
        location /login {
            limit_req zone=one burst=5 nodelay;
            proxy_pass http://127.0.0.1:8080;
            client_body_buffer_size 16K;
            client_max_body_size 10M;
            client_header_buffer_size 1k;
            large_client_header_buffers 4 16k;
        }
    }
}
```

# Logs

# Security assessment and misconfigurations
* <br>
    Why needed: <br>
    Vulnerable: ` #` <br>
    Exploit: ` #` <br>
    Secure: ` #` <br>

* SSRF <br>
    Why needed: уязвимость позволяющая выполнять различного рода запросы от Nginx<br>
    Vulnerable: 
    ```
    # отсутствие директивы internal
    location ~ /proxy/(.*)/(.*)/(.*)$ {
        proxy_pass $1://$2/$3;}
   
    # небезопасное внутреннее перенаправление proxy_pass.
    location ~* ^/internal-proxy/(?<proxy_proto>https?)/(?<proxy_host>.*?)/(?<proxy_path>.*)$ {
        internal;
        proxy_pass $proxy_proto://$proxy_host/$proxy_path ;
        proxy_set_header Host $proxy_host;}
    ``` <br>
    Exploit: ` #` <br>
    Secure: ` #` <br>

* host_spoofing Подделка заголовка запроса Host <br>
    Why needed: проброс заголовка host приложению за прокси <br>
    Vulnerable: 
    ```
    location @app {
        proxy_set_header Host $http_host;
        proxy_pass http://...;} 
    ``` <br>
    Exploit: ` #` <br>
    Secure: ` #` перечислить корректные имена сервера в директиве server_name; всегда использовать переменную $host, вместо $http_host. <br>

* LFI \ Path travers in alias location <br>
    Why needed: Директива alias используется для замены пути указанного локейшена <br>
    Vulnerable: `location /imgs {alias /path/images/;}` запрос /img/1.gif будет отдан файл /path/images/1.gif <br>
    Exploit: `curl /imgs../../../etc/passwd` <br>
    Secure: `location /imgs {alias /path/images/;}` необходимо найти все директивы alias и убедится что префиксный локейшен оканчивается на `/` <br>

* No limits against DDoS <br>
    Why needed: Ограничение лимитов траффика<br>
    Vulnerable: `if none` <br>
    Exploit: ` #` <br>
    Secure: 
    ```
    limit_req_zone $binary_remote_addr zone=one:10m rate=30r/m; # ограничение до 30запр./мин. количество запросов от одного адреса
    ...
    location /login.html {limit_req zone=one;} # применение ограничения к конкретному пути

    client_body_timeout 5s; # таймауты которые не позволят соединениям висеть слишком долго
    client_header_timeout 5s; # таймауты которые не позволят соединениям висеть слишком долго
    client_body_buffer_size <= 1M
    client_max_body_size <= 1M
    large_client_header_buffers_size <= 10K
    ```

* SSL and HTTP header misconfiguration<br>
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
    ```

* proxy_set_header Upgrade & Connection <br>
    Why needed: proxy_set_header directive is often used to customize the headers that are sent to a proxied server.<br>
    Vulnerable: <br>
    ```
    location / {
        proxy_pass http://backend:9999;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade; # forwards the Upgrade header from the client to the backend server.
        proxy_set_header Connection $http_connection; # forwards the Connection header
    }
    ```
    Exploit: `curl -k -v -X GET https://localhost/ -H "Upgrade: h2c" -H "Connection: Upgrade, HTTP2-Settings"` <br>
    Secure: # remove it <br>
    ```
    location / {
        proxy_pass http://backend:9999;
        proxy_http_version 1.1;
    }
    ```

* proxy_pass and internal Directives <br>
    Why needed: The proxy_pass directive is used to forward requests to another server, while the internal directive ensures that certain locations are only accessible within Nginx<br>
    Vulnerable: `location /internal/ {internal; proxy_pass http://backend/internal/;}`<br>
    Exploit: `curl "http://example.com/internal/private-data"`<br>
    Secure: `add location /public/ {proxy_pass http://backend/public/;}`<br>

* DNS Spoofing Vulnerability<br>
    Why needed: <br>
    Vulnerable: `resolver 8.8.8.8;`<br>
    Exploit: ` #`<br>
    Secure: `resolver 127.0.0.1; #Additionally, ensure DNSSEC is used to validate DNS responses.`<br>

* map Directive Default Value<br>
    Why needed: used to map one value to another, frequently for controlling access or other logic<br>
    Vulnerable: `map $uri $mappocallow {/map-poc/private 0;}`<br>
    Exploit: `curl "http://example.com/map-poc/undefined"`<br>
    Secure: `map $uri $mappocallow {default 0;} #Always specify a default value in the map directive:`<br>

* X-Accel-Redirect: /.env<br>
    Why needed: <br>
    Vulnerable: ` #`<br>
    Exploit: `curl -I "http://example.com" -H "X-Accel-Redirect: /.env"`<br>
    Secure: ` #`<br>

* merge_slashes set to off<br>
    Why needed: By default, Nginx's merge_slashes directive is set to on<br>
    Vulnerable: ` #`<br>
    Exploit: `http://example.com//etc/passwd`<br>
    Secure: `http {merge_slashes off;}#`<br>

* Missing Root Location <br>
    Why needed: определяет директорию для выдачи контента. Если не задана - выдает из /etc/nginx/<br>
    Vulnerable: `server {root /etc/nginx/;} # no root`<br>
    Exploit: `curl http://example.com/passwd`<br>
    Secure: `server {root /var/www/html;}`<br>

* Unsafe Path Restriction <br>
    Why needed: ограничение и политика запросов<br>
    Vulnerable: `location = /admin { deny all; }` <br>
    Exploit: `curl http://example.com/%61dmin /admin%00 /admin. /ADMIN` <br>
    Secure: `location ~* ^/admin(/|$) {deny all;}` <br>

* Unsafe Use of Variables: $uri and $document_uri <br>
    Why needed: Используются для захвата данных из URL <br>
    Vulnerable: `return 302 https://example.com$uri;` <br>
    Exploit: `curl http://localhost/%0d%0aDetectify:%20clrf` <br>
    Secure: `return 302 https://example.com$request_uri; # use $request_uri` <br>

* Regex Vulnerabilities <br>
    Why needed: <br>
    Vulnerable: `location ~ /docs/([^/])? { … $1 … } # does not check for spaces` <br>
    How safe: `location ~ /docs/([^/\s])? { … $1 … }  # not vulnerable (checks for spaces)` <br>