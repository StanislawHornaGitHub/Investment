# Promtail
It is logs scraper to collect and push application logs to [Loki](/Loki/README.md) instance.

All application logs are saved in shared folder on hosting machine (`./APP_LOG`), where they are scanned by promtail.

Promtail also provides unification of most common log fields like:
timestamp format or log level to allow easier browsing the logs. 