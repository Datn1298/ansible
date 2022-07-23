from run_ansible import *

def install_apache(http_host, http_conf, app_user, inventory):
    path= "/var/www/" + http_host
    path_index = path+"/index.html"
    path_dest_config = '/etc/apache2/sites-available/'+ http_conf
    path_template_config = "file/apache.conf.j2"
    path_src_config = "file/default.conf.j2"

    config=""
    with open(path_template_config, "r") as template:
        config=template.read()

    config = config.replace("{{ http_host }}", http_host)

    with open(path_src_config, "w") as _config:
        _config.write(str(config))

    name_task = "Install Apache"
        
    tasks=[
        dict(action=dict(module='apt', args=dict(name='apache2', update_cache='yes', state='present'))),
        dict(action=dict(module='shell', args='ufw allow 80')),
        dict(action=dict(module='file', args=dict(path=path, state='directory', owner=app_user , mode='0775'))),
        dict(action=dict(module='file', args=dict(path=path_index, state='touch'))),
        dict(action=dict(module='template', args=dict(src=path_src_config, dest=path_dest_config))),
        dict(action=dict(module='service', args=dict(name="apache2", state="restarted"))),
        dict(action=dict(module='shell', args='a2ensite ' + http_conf)),
        dict(action=dict(module='service', args=dict(name="apache2", state="reloaded"))),
        dict(action=dict(module='shell', args='a2dissite 000-default.conf')),
        dict(action=dict(module='service', args=dict(name="apache2", state="reloaded")))
    ]
    ip, status, output, error, time = run_ansible(tasks, "install", inventory)
    return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time} 

def install_nginx(http_host, http_conf, app_user, inventory):
    path= "/var/www/" + http_host + "/html"
    path_index = path+"/index.html"
    path_dest_config = '/etc/nginx/sites-available/'+ http_conf
    path_template_config = "nginx.conf.j2"
    path_src_config = "default.conf.j2"
    path_src_site = "/etc/nginx/sites-available/default"
    path_dest_site = "/etc/nginx/sites-enabled/default"

    config=""
    with open(path_template_config, "r") as template:
        config=template.read()

    config = config.replace("{{ http_host }}", http_host)

    with open(path_src_config, "w") as _config:
        _config.write(str(config))

    name_task = "Install Nginx"
        
    tasks=[
    dict(action=dict(module='apt', args=dict(name='nginx', update_cache='yes', state='present'))),
        dict(action=dict(module='shell', args='ufw allow 80')),
        dict(action=dict(module='file', args=dict(path=path, state='directory', owner=app_user , mode='0775'))),
        dict(action=dict(module='file', args=dict(path=path_index, state='touch'))),
        dict(action=dict(module='template', args=dict(src=path_src_config, dest=path_dest_config))),
        dict(action=dict(module='service', args=dict(name="apache2", state="restarted"))),
        dict(action=dict(module='file', args=dict(src=path_src_site, dest=path_dest_site, state='link'))),
        dict(action=dict(module='service', args=dict(name="apache2", state="restarted")))
    ]
    ip, status, output, error, time = run_ansible(tasks, "install", inventory)
    return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time} 

def install_docker(inventory):
    name_task = "Install Docker"
    tasks=[
        dict(action=dict(module='apt', args=dict(name='docker',state='absent'))),
        dict(action=dict(module='apt', args=dict(name='docker-engine',state='absent'))),
        dict(action=dict(module='apt', args=dict(name='docker.io',state='absent'))),
        dict(action=dict(module='apt', args=dict(name='containerd runc',state='absent'))),
        dict(action=dict(module='apt', args=dict(name='apt-transport-https',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='ca-certificates',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='curl',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='gnupg-agent',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='software-properties-common',state='present',update_cache='yes'))),
        dict(action=dict(module='apt_key', args=dict(url='https://download.docker.com/linux/ubuntu/gpg' ,state='present'))),
        dict(action=dict(module='apt_repository', args=dict(repo='deb https://download.docker.com/linux/ubuntu focal stable' ,state='present'))),
        dict(action=dict(module='apt', args=dict(name='docker-ce',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='docker-ce-cli',state='present',update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='containerd.io',state='present',update_cache='yes'))),
        dict(action=dict(module='shell', args='chmod 666 /var/run/docker.sock')),
        dict(action=dict(module='get_url', args=dict(url='https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Linux-x86_64',dest='/usr/local/bin/docker-compose',mode='u+x,g+x'))),
        dict(action=dict(module='service', args=dict(name="docker", state="started")))
    ]
    ip, status, output, error, time = run_ansible(tasks, "install", inventory)
    return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time} 

def install_php(inventory):
    name_task = "Install PHP"
    tasks = [
        dict(action=dict(module='apt', args=dict(name='software-properties-common'))),
        dict(action=dict(module='apt_repository', args=dict(repo="ppa:ondrej/php"))),
        dict(action=dict(module='apt', args=dict(update_cache='yes'))),
        dict(action=dict(module='apt', args=dict(name='php7.4', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-cli', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-json', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-common', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-mysql', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-zip', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-gd', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-mbstring', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-curl', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-xml', update_cache='yes', state='present'))),
        dict(action=dict(module='apt', args=dict(name='php7.4-bcmath', update_cache='yes', state='present'))),
    ]
    ip, status, output, error, time = run_ansible(tasks, "install", inventory)
    return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time}

def install_apache_php(http_host, http_conf, app_user, inventory):
    # install_apache(http_host, http_conf, app_user)
    # install_php()
    
    # path = "/var/www/html/info.php"

    # tasks = [
    # 	[dict(action=dict(module='file', args=dict(path=path, state='touch')))],
    # 	[dict(action=dict(module='lineinfile', args=dict(path=path, line='<?php phpinfo(); ?>')))],
    # 	[dict(action=dict(module='service', args=dict(name="apache2", state="restarted")))]
    # ]
    # status = True
    # for task in tasks:
        # if (status == True) :
        #     status = run_ansible(task, "install")
    return { "ip": "", "task": "", "status": "", "result": "", "error": "", "date": ""}

def install_nginx_php(http_host, http_conf, app_user, inventory):
    # install_nginx(http_host, http_conf, app_user)
    # install_php()
    
    # path = "/var/www/html/info.php"
    # config = """
    # location ~ \.php$ {
    # 	include snippets/fastcgi-php.conf;

    # 	# Nginx php-fpm sock config:
    # 	fastcgi_pass unix:/run/php/php8.1-fpm.sock;
    # 	# Nginx php-cgi config :
    # 	# Nginx PHP fastcgi_pass 127.0.0.1:9000;
    # }

    # # deny access to Apache .htaccess on Nginx with PHP, 
    # # if Apache and Nginx document roots concur
    # location ~ /\.ht {
    # 	deny all;
    # }
    # """
    # after_line="# config"

    # tasks = [
    # 	[dict(action=dict(module='file', args=dict(path=path, state='touch')))],
    # 	[dict(action=dict(module='blockinfile', args=dict(path=path, block=config, insertafter=after_line)))],
    # 	[dict(action=dict(module='service', args=dict(name="apache2", state="restarted")))],
    # 	[dict(action=dict(module='service', args=dict(name="apache2", state="reloaded")))]
    # ]
    # status = True
    # for task in tasks:
    # 	if (status == True) :
    # 		status = run_ansible(task, "install")
    return { "ip": "", "task": "", "status": "", "result": "", "error": "", "date": ""}
