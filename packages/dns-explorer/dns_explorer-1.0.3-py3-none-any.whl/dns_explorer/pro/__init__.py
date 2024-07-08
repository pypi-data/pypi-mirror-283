# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
Copyright
    Copyright (C) 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    dns_explorer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    dns_explorer is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class DNSProcessor with attribute(s) and method(s).
    Performs dns check by domain name and cluster number.
'''

import sys
from typing import List, Tuple, Optional
from os.path import dirname, realpath
from re import search, Match
from socket import gethostbyaddr, herror

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.pro_config import ProConfig
    from ats_utilities.config_io.yaml.yaml2object import Yaml2Object
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from dns.resolver import Answer, NoAnswer, resolve, NXDOMAIN
    from dns.exception import Timeout
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/dns_explorer'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/dns_explorer/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DNSProcessor(FileCheck, ProConfig):
    '''
        Defines class DNSProcessor with attribute(s) and method(s).
        Performs dns check by domain name and cluster number.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | _SUB_DNS_CONFIG - List of subdomains.
            :methods:
                | __init__ - Initials DNSProcessor constructor.
                | _reverse_dns - Reverse DNS by IP address.
                | _dns_request - Executes dns request.
                | execute - Executes exploration of dns.
    '''

    _TOOL_VERBOSE: str = 'DNS_EXPLORER::PRO::DNS_PROCESSOR'
    _SUB_DNS_CONFIG: str = '/../conf/subdomains.yaml'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials DNSProcessor constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        FileCheck.__init__(self, verbose)
        ProConfig.__init__(self, verbose)
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init dns processor']
        )
        current_dir: str = dirname(realpath(__file__))
        net_config: str = f'{current_dir}{self._SUB_DNS_CONFIG}'
        self.check_path(net_config, verbose)
        self.check_mode('r', verbose)
        self.check_format(net_config, 'yaml', verbose)
        if self.is_file_ok():
            yml2obj = Yaml2Object(net_config)
            self.config = yml2obj.read_configuration()

    def _reverse_dns(
        self, ip: str, verbose: bool = False
    ) -> Optional[List[str]]:
        '''
            Reverse DNS by IP address.

            :param ip: IP address
            :type ip: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: List of dns names | None
            :rtype: <Optional[List[str]]>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([('str:ip', ip)])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(ip):
            raise ATSValueError('missing ip address')
        try:
            verbose_message(
                verbose, [f'{self._TOOL_VERBOSE.lower()} check IP {ip}']
            )
            result: Tuple[str, List[str], List[str]] = gethostbyaddr(ip)
            return [result[0]] + result[1]
        except herror:
            return None

    def _dns_request(self, domain: str, verbose: bool = False) -> None:
        '''
            Executes dns request.

            :param domain: Domain name
            :type domain: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([('str:domain', domain)])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(domain):
            raise ATSValueError('missing domain name')
        try:
            result: Answer = resolve(domain)
            if result:
                ip_address: Optional[str] = None
                pattern: str = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
                match: Match[str] | None = search(pattern, str(result.rrset))
                if match:
                    ip_address = match.group(0)
                if bool(ip_address):
                    dns_reverse: List[str] | None = self._reverse_dns(
                        ip_address, verbose
                    )
                    if dns_reverse:
                        success_message([
                            f'{self._TOOL_VERBOSE.lower()}',
                            f'{domain}: {ip_address} => {dns_reverse}'
                        ])
        except (NXDOMAIN, Timeout, NoAnswer):
            pass

    def execute(
        self, domain: str, cluster: int, verbose: bool = False
    ) -> bool:
        '''
            Executes exploration of dns.

            :param domain: Domain name
            :type domain: <str>
            :param cluster: Cluster number
            :type cluster: <int>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([
            ('str:domain', domain), ('int:cluster', cluster)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(domain):
            raise ATSValueError('missing domain name')
        if cluster <= 0:
            raise ATSValueError('set cluster number')
        if not bool(self.config):
            return False
        success_message([
            f'\n{self._TOOL_VERBOSE.lower()} Checking dns {domain}\n'
        ])
        for sub_domain in self.config['subdomains']:
            sub_domain_final: str = f'{sub_domain}.{domain}'
            self._dns_request(sub_domain_final, verbose)
            for i in range(0, cluster):
                sub_domain_multi: str = f'{sub_domain}{str(i)}.{domain}'
                self._dns_request(sub_domain_multi, verbose)
        return True
