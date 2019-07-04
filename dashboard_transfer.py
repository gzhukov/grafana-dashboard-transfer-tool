#!/usr/bin/env python3
import argparse
import logging
import requests
import os
import json
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s')


def list_dashboards(api_url, header):
    url = urljoin(api_url, "api/search")
    r = requests.get(url, headers=header)
    return r.json()


def set_org(api_url, header, org_id):
    url = urljoin(api_url, "api/user/using/{}".format(org_id))
    r = requests.post(url, headers=header)
    logging.info(r.json())
    return r.status_code


def get_dashboard(api_url, header, uid):
    url = urljoin(api_url, "api/dashboards/uid/{}".format(uid))
    r = requests.get(url, headers=header)
    json_data = r.json()
    logging.debug(json_data)
    if 'meta' in json_data:
        json_data.pop('meta')
    if 'dashboard' not in json_data:
        return None
    json_data['dashboard']['id'] = None
    json_data['dashboard']['uid'] = None
    json_data.update({"overwrite": False})
    json_data.update({"message": "Imported"})
    return json_data


def import_dashboard(api_url, header, file):
    with open(file, 'rb') as payload:
        headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
        headers.update(header)
        url = urljoin(api_url, 'api/dashboards/db')
        r = requests.post(url, data=payload, headers=headers)
        logging.info(r.json())
        return r.status_code


def main():
    parser = argparse.ArgumentParser(description='Datasource-to-grafana adder')

    parser.add_argument('--url', help='Grafana url. Example: https://play.grafana.org', required=True)
    parser.add_argument('--org', help='(dst) org id name', required=True)
    parser.add_argument('--token', '-t', help='token', required=True)
    parser.add_argument('--list', '-l', help='list dashboards', action='store_true')
    parser.add_argument('--exp', '-e', help='export dashboard')
    parser.add_argument('--exp_all', help='export all dashboards to dir', action='store_true')
    parser.add_argument('--imp', '-i', help='import dashboard')
    parser.add_argument('--imp_all', help='import all dashboards from dir', action='store_true')

    parser.add_argument('--dir', '-d', help='dir for importing/exporting dashboards')

    args = parser.parse_args()

    auth_header = {'Authorization': 'Bearer ' + args.token}

    set_org(args.url, auth_header, args.org)

    if args.list:
        for dash in list_dashboards(args.url, auth_header):
            print(dash['title'])

    if args.exp:
        for dash in list_dashboards(args.url, auth_header):
            if dash['title'] == args.exp:
                dash_data = get_dashboard(args.url, auth_header, dash['uid'])
                if args.dir:
                    logging.info(dash['title'])
                    with open(os.path.join(args.dir, dash['title'].replace('/', '') + ".json"), 'w') as file:
                        file.write(json.dumps(dash_data))
                else:
                    print(json.dumps(dash_data))

    if args.exp_all:
        for dash in list_dashboards(args.url, auth_header):
            dash_data = get_dashboard(args.url, auth_header, dash['uid'])
            if args.dir:
                logging.info(dash['title'])
                with open(os.path.join(args.dir, dash['title'].replace('/', '') + ".json"), 'w') as file:
                    file.write(json.dumps(dash_data))
            else:
                print(json.dumps(dash_data))

    if args.imp:
        import_dashboard(args.url, auth_header, args.imp)

    if args.imp_all and args.dir:
        for file in os.listdir(args.dir):
            import_dashboard(args.url, auth_header, os.path.join(args.dir, file))


if __name__ == "__main__":
    main()
