import sys
import argparse
import pprint
from requests import get
import ipapi

# Original source and credit: https://github.com/ipapi-co


def main(argv=None):
    argv = argv or sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='IP Address Location & Geolocation API : https://ipapi.co/ by Kloudend, Inc.')

    parser.add_argument('-i', '--ip', dest='ip', help='IP Address (IPv4 or IPv6) that you wish to locate.'
                                                      ' If omitted, it defaults to the your machine\'s IP')
    parser.add_argument('-k', '--key', dest='key',
                        help='API key (for paid plans). Omit it for free plan')
    parser.add_argument('-o', '--output', dest='output', help='Output format i.e. either json|csv|xml|yaml or '
                        'Specific location field i.e. city|region|country etc. '
                        'See https://ipapi.co/api for field details')

    args = parser.parse_args(argv)

    pprint.pprint(ipapi.location(args.ip, args.key, args.output), indent=4)


field_list = ['ip', 'city', 'region', 'region_code', 'country', 'country_code', 'country_code_iso3',
              'country_capital', 'country_tld', 'country_name', 'continent_code', 'in_eu', 'postal',
              'latitude', 'longitude', 'timezone', 'utc_offset', 'country_calling_code', 'currency',
              'currency_name', 'languages', 'country_area', 'country_population', 'latlong',
              'asn', 'org']


def build_url(ip, key, output):
    url = 'https://ipapi.co/'

    if ip:
        url = '{}{}/'.format(url, ip)

    url = '{}{}/'.format(url, output)

    if key:
        url = '{}?key={}'.format(url, key)

    return url


def parse_response(resp):
    if resp.headers['Content-Type'] == 'application/json':
        return resp.json()
    else:
        return resp.text


def location(ip=None, key=None, output=None, options=None):
    ''' 
    Get Geolocation data and related information for an IP address 
    - ip      : IP Address (IPv4 or IPv6) that you wish to locate.
                If omitted, it defaults to the your machine's IP
    - key     : API key (for paid plans).
                Omit it or set key=None for usage under free IP Location tier.
    - output  : The desired output from the API.
                For complete IP location object, valid values are json, csv, xml, yaml.
                To retrieve a specific field (e.g. city, country etc. as text), valid values are [1].
                If omitted or None, gets the entire location data as json
    - options : request options supported by python requests library

    '''

    if output is None:
        output = 'json'

    if options is None:
        options = {}

    url = build_url(ip, key, output)

    headers = {
        'user-agent': 'ipapi.co/#ipapi-python-v1.0.4'
    }

    resp = get(url, headers=headers, **options)

    data = parse_response(resp)


if __name__ == "__main__":
    sys.exit(main())
