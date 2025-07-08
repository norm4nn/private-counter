.DEFAULT_GOAL := help

APP_ID := private_counter
APP_NAME := PrivateCounter
APP_VERSION := 1.0.0
APP_SECRET := 12345
APP_PORT := 9031

JSON_INFO := "{\"id\":\"$(APP_ID)\",\"name\":\"$(APP_NAME)\",\"daemon_config_name\":\"manual_install\",\"version\":\"$(APP_VERSION)\",\"secret\":\"$(APP_SECRET)\",\"port\":$(APP_PORT),\"routes\":[{\"url\":\".*\",\"verb\":\"GET, POST, PUT, DELETE\",\"access_level\":1,\"headers_to_exclude\":[]}]}"

.PHONY: register
register:
	docker exec -u www-data nextcloud php occ app_api:app:register $(APP_ID) manual_install --json-info $(JSON_INFO) --force-scopes --wait-finish
