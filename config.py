# config.py — Temas, fontes e whitelist de termos técnicos

TEMAS = {
    "dark": {
        "appearance":   "dark",
        "vinho":        "#6e0202",
        "azul_hover":   "#4a0101",
        "bg_card":      "#1e1e1e",
        "bg_app":       "#161616",
        "text_muted":   "#888880",
        "text_main":    "white",
        "border_result":"#333",
        "border_total": "#444",
        "icon":         "☀",
        "tooltip":      "Modo claro",
    },
    "light": {
        "appearance":   "light",
        "vinho":        "#008ec2",
        "azul_hover":   "#006a94",
        "bg_card":      "#f0f0f0",
        "bg_app":       "#ffffff",
        "text_muted":   "#666660",
        "text_main":    "#111111",
        "border_result":"#cccccc",
        "border_total": "#bbbbbb",
        "icon":         "☾",
        "tooltip":      "Modo escuro",
    },
}

# Tamanhos de fonte
FONT = {
    "title":  18,
    "caixa":  16,
    "label":  16,
    "radio":  16,
    "button": 14,
    "text":   14,
}

# Palavras técnicas de TI que o corretor ortográfico deve ignorar.
# Adicione aqui qualquer termo específico do seu ambiente.
WHITELIST: set[str] = {
    # Inglês geral de TI
    "backup", "backups", "deploy", "deployed", "deployment",
    "firewall", "firewalls", "gateway", "gateways",
    "hardware", "software", "firmware",
    "vpn", "dns", "dhcp", "ip", "tcp", "udp", "ftp", "ssh", "ssl", "tls",
    "http", "https", "api", "apis", "rest", "json", "xml", "yaml",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "linux", "ubuntu", "debian", "windows", "macos",
    "python", "java", "javascript", "typescript",
    "docker", "kubernetes", "ansible", "terraform",
    "git", "github", "gitlab", "bitbucket",
    "cpu", "gpu", "ram", "ssd", "hdd",
    "switch", "switches", "router", "routers",
    "proxy", "proxies", "cluster", "clusters",
    "host", "hosts", "hostname", "server", "servers",
    "client", "clients", "endpoint", "endpoints",
    "script", "scripts", "log", "logs", "debug",
    "pipeline", "pipelines", "workflow", "workflows",
    "ticket", "tickets", "issue", "issues",
    "dashboard", "dashboards", "report", "reports",
    "alert", "alerts", "monitor", "monitoring",
    "onpremise", "onprem", "cloud", "saas", "paas", "iaas",
    "uptime", "downtime", "sla", "slo",
    "patch", "patches", "hotfix", "rollback",
    "staging", "production", "sandbox",
    "token", "tokens", "oauth", "jwt",
    "email", "emails", "gmat", "plugins", "plugin", "US", "whatsapp", "elvys", "glpi"
}
