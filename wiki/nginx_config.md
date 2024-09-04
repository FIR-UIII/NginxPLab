# NGINX start
```bash
sudo apt update # update package index
sudo apt install nginx # install nginx
sudo systemctl start nginx # start as service
sudo systemctl enable nginx # enable nginx with boot
echo "<h1>Welcome to NGINX!</h1>" | sudo tee /var/www/html/index.html
cat /etc/nginx/nginx.conf
nginx -t {-T} # проверить конфигурацию /etc/nginx/nginx.conf {+выводит сами конфигурации}
ps -ef | grep nginx # проверить работу процесов master и workers
nginx -s {stop, quit, reload, reopen} # отправить сигнал мастер процессу
```

### Default configuration
```
# /etc/nginx/nginx.conf
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include       mime.types; # include a file called mime.types
    default_type  application/octet-stream;
    server { # определяет поведение виртуального сервера (правила предоставления контента)
        listen 80 default_server; # определяет порт для прослушивания
        server_name localhost; # DNS имя. `_` означает любое имя
        
        location / { # определяет URL
            root /usr/share/nginx/html; # определяет директорию предоставления HTTP контента
            index index.html index.htm; # файлы для отображаения (index.html или index.htm)
        }
        location /test {
            return 200 "this is TEST";
        } 
    }
}    
```

### Configure Worker Processes
```
worker_processes auto;
events {
    worker_connections 1024; # means that each worker process can handle 1024 simultaneous connections
}

http {...}
```

### NGINX files and directories
`/etc/nginx/nginx.conf` > основной конфигурационный файл для всего сервера
`/etc/nginx/conf.d/default.conf` > определяет конфигурации HTTP сервера по умолчанию
`/var/log/nginx/` > журнал логов
    `sudo tail -f /var/log/nginx/error.log`
    
### NGINX as a Reverse Proxy (from client to server)
```
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8080; # адрес сервера для предоставления контента HTTP
        proxy_set_header Host $host; # пробрасывает заголовок Host от клиента к серверу 
        proxy_set_header X-Real-IP $remote_addr; # пробрасывает IP клиента к серверу
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # пробрасывает IP клиента к серверу
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTP Load balancer configuration (from client to 2 servers)
```
upstream backend { # директива опредяет балансировку между серверами
        server 10.10.12.45:80      weight=1; # weight определяет вес 
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

### Caching
```
http {
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m use_temp_path=off;
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_cache my_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_use_stale error timeout invalid_header updating;
    }
}
```

### Access Logs
```
# /etc/nginx/nginx.conf
http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    # Other settings...
}
```