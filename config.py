from run_ansible import *
from audit import *


def set_pass_max_days():
    task = [
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/login.defs",
                regexp="^PASS_MAX_DAYS.*",
                replace="PASS_MAX_DAYS 90",
            ),
        )
    ]
    ip, status, output, error, time = run_ansible(task, "config")
    name_task = "Set PASS_MAX_DAYS"
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def set_pass_min_days():
    task = [
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/login.defs",
                regexp="^PASS_MIN_DAYS.*",
                replace="PASS_MIN_DAYS 6",
            ),
        )
    ]
    ip, status, output, error, time = run_ansible(task, "config")
    name_task = "Set PASS_MAX_DAYS"
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def set_pass_min_len(inventory):
    temp, temp, temp, result, temp, temp = audit_pass_min_len(inventory)

    name_task = "Set PASS_MIN_LEN"
    if result != "":
        task = [
            dict(
                action=dict(module="replace"),
                args=dict(
                    path="/etc/login.defs",
                    regexp="^PASS_MIN_LEN.*",
                    replace="PASS_MIN_LEN 6",
                ),
            )
        ]
        ip, status, output, error, time = run_ansible(task, "config")
    else:
        task = [
            dict(
                action=dict(module="lineinfile"),
                args=dict(
                    path="/etc/login.defs",
                    line="PASS_MIN_LEN 6",
                    insertafter="^PASS_MIN_DAYS",
                ),
            )
        ]
        ip, status, output, error, time = run_ansible(task, "config")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def set_pass_warm_age():
    task = [
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/login.defs",
                regexp="^PASS_WARM_AGE.*",
                replace="PASS_WARM_AGE 7",
            ),
        )
    ]
    ip, status, output, error, time = run_ansible(task, "config")
    name_task = "Set PASS_WARM_AGE"
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def config_permitroot():
    task = [
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/ssh/sshd_config",
                regexp="^PermitRootLogin.*",
                replace="PermitRootLogin no",
            ),
        )
    ]
    name_task = "Config PermitRootLogin"
    ip, status, output, error, time = run_ansible(task, "config")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def config_password_authentication():
    task = [
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/ssh/sshd_config",
                regexp="^PasswordAuthentication.*",
                replace="PasswordAuthentication no",
            ),
        )
    ]
    name_task = "Set Password Authentication"
    ip, status, output, error, time = run_ansible(task, "config")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def config_apache(inventory):
    name_task = "Config Apache"
    task = [
        dict(action=dict(module="shell", args="a2dissite 000-default.conf")),
        dict(action=dict(module="shell"), args="a2enmod headers"),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line='Header set X-XSS-Protection "1; mode=block"',
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line='Header set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"',
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line='Header always append X-Frame-Options DENY"',
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line="Header set X-Content-Type-Options nosniff",
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line="Header set Content-Security-Policy \"default-src 'self'",
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/apache2/conf-available/security.conf",
                regexp="ServerSignature.*",
                replace="ServerSignature Off",
            ),
        ),
        dict(
            action=dict(module="replace"),
            args=dict(
                path="/etc/apache2/conf-available/security.conf",
                regexp="ServerTokens.*",
                replace="ServerTokens Prod",
            ),
        ),
        dict(
            action=dict(module="service", args=dict(name="apache2", state="restarted"))
        ),
    ]
    ip, status, output, error, time = run_ansible(task, "config")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def config_nginx(inventory):
    name_task = "Config Nginx"
    task = [
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/nginx/sites-available/default",
                line='add_header X-XSS-Protection "1; mode=block";',
                insertafter="try_file*",
            ),
        ),
        dict(action=dict(module="service", args=dict(name="nginx", state="restarted"))),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/nginx/sites-available/default",
                line='add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";',
                insertafter="try_file*",
            ),
        ),
        dict(action=dict(module="service", args=dict(name="nginx", state="restarted"))),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line='add_header X-Frame-Options "DENY";',
                insertafter="try_file*",
            ),
        ),
        dict(action=dict(module="service", args=dict(name="nginx", state="restarted"))),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line="add_header X-Content-Type-Options nosniff;",
                insertafter="try_file*",
            ),
        ),
        dict(action=dict(module="service", args=dict(name="nginx", state="restarted"))),
        dict(
            action=dict(module="lineinfile"),
            args=dict(
                path="/etc/apache2/apache2.conf",
                line="add_header Content-Security-Policy \"default-src 'self'\";",
                insertafter="try_file*",
            ),
        ),
        dict(action=dict(module="service", args=dict(name="nginx", state="restarted"))),
    ]
    ip, status, output, error, time = run_ansible(task, "config")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }
