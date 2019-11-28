# grafana-dashboard-transfer-tool

Small tool for export &amp; import grafana dashboards via grafana API  
How to get auth key: https://grafana.com/docs/http_api/auth/  

## Usage examples:

List all dashboards:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 13 --token $TOKEN --list`  

Export one dashboard to stdout:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 13 --token $TOKEN --exp $DASHBOARD_NAME`  
Export one dashboard to a dir:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 13 --token $TOKEN --exp $DASHBOARD_NAME -d ./result/`  
Export all dashboards to a dir:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 13 --token $TOKEN --exp_all -d ./result/`  
Import one dashboard:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 150 --token $TOKEN --imp ./result/dashboard.json`  
Import all dashboards from dir:  
`./dashboard_transfer.py --url "${GRAFANA_URL}" --org 150 --token $TOKEN --imp_all ./result/`

If you want to change datasource - use `sed`, Luke!:  
`sed -i 's/"datasource": "ds-old"/"datasource": "ds-new"/g' result/*.json`
