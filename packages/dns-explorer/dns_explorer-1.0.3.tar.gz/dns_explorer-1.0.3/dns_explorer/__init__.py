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
    Defines class DNSExplorer with attribute(s) and method(s).
    Loads a base info, creates a CLI interface and run operations.
'''

import sys
from typing import Any, List, Dict
from os.path import dirname, realpath
from argparse import Namespace

try:
    from ats_utilities.splash import Splash
    from ats_utilities.logging import ATSLogger
    from ats_utilities.cli import ATSCli
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from dns_explorer.pro import DNSProcessor
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


class DNSExplorer(ATSCli):
    '''
        Defines class DNSExplorer with attribute(s) and method(s).
        Loads a base info, creates a CLI interface and run operations.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | _CONFIG - Tool info file path.
                | _LOG - Tool log file path.
                | _LOGO - Logo for splash screen.
                | _OPS - List of tool options.
                | _logger - Logger object API.
            :methods:
                | __init__ - Initials DNSExplorer constructor.
                | process - Processes and runs tool operation.
    '''

    _TOOL_VERBOSE: str = 'DNS_EXPLORER'
    _CONFIG: str = '/conf/dns_explorer.cfg'
    _LOG: str = '/log/dns_explorer.log'
    _LOGO: str = '/conf/dns_explorer.logo'
    _OPS: List[str] = [
        '-d', '--domain', '-c', '--cluster', '-v', '--verbose'
    ]

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials DNSExplorer constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        current_dir: str = dirname(realpath(__file__))
        dns_explorer_property: Dict[str, str | bool] = {
            'ats_organization': 'vroncevic',
            'ats_repository': f'{self._TOOL_VERBOSE.lower()}',
            'ats_name': f'{self._TOOL_VERBOSE.lower()}',
            'ats_logo_path': f'{current_dir}{self._LOGO}',
            'ats_use_github_infrastructure': True
        }
        Splash(dns_explorer_property, verbose)
        base_info: str = f'{current_dir}{self._CONFIG}'
        super().__init__(base_info, verbose)
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init tool info']
        )
        self._logger: ATSLogger = ATSLogger(
            self._TOOL_VERBOSE.lower(), True, None, True, verbose
        )
        if self.is_operational():
            self.add_new_option(
                self._OPS[0], self._OPS[1], dest='domain',
                help='Domain name (provide name)'
            )
            self.add_new_option(
                self._OPS[2], self._OPS[3], dest='cluster',
                help='Cluster number (provide number)'
            )
            self.add_new_option(
                self._OPS[4], self._OPS[5], action='store_true',
                default=False, help='Activate verbose mode for tool'
            )

    def process(self, verbose: bool = False) -> bool:
        '''
            Processes and runs tool operation.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        status: bool = False
        if self.is_operational():
            try:
                args: Any | Namespace = self.parse_args(sys.argv)
                if not bool(getattr(args, 'domain')):
                    error_message(
                        [
                            f'{self._TOOL_VERBOSE.lower()}',
                            'missing domain argument'
                        ]
                    )
                    return status
                if not bool(getattr(args, 'cluster')):
                    error_message(
                        [
                            f'{self._TOOL_VERBOSE.lower()}',
                            'missing cluster argument'
                        ]
                    )
                    return status
                tool: DNSProcessor = DNSProcessor(
                    getattr(args, 'verbose') or verbose
                )
                status = tool.execute(
                    getattr(args, 'domain'),
                    int(getattr(args, 'cluster')),
                    getattr(args, 'verbose') or verbose
                )
                success_message([f'{self._TOOL_VERBOSE.lower()} done\n'])
                self._logger.write_log(
                    f'Check for {getattr(args, "domain")} done',
                    self._logger.ATS_INFO
                )
            except SystemExit:
                error_message(
                    [
                        f'{self._TOOL_VERBOSE.lower()}'
                        'expected arguments domain and cluster number'
                    ]
                )
                return status
        else:
            error_message(
                [f'{self._TOOL_VERBOSE.lower()} tool is not operational']
            )
            self._logger.write_log(
                'tool is not operational', self._logger.ATS_ERROR
            )
        return status
