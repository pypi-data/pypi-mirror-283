# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
Copyright
    Copyright (C) 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    ats_coverage is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    ats_coverage is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ProCoverage with attribute(s) and method(s).
    Generates code coverage for project and add to README.md.
'''

import sys
from typing import Any, Dict, List, Optional
from os.path import exists, basename
from json import load
from unittest import TestLoader, TestSuite, TextTestRunner

try:
    from pathlib import Path
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_file_error import ATSFileError
    from coverage import Coverage
except ImportError as ats_error_message:
    # Force exit python #######################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/ats_coverage'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProCoverage(ATSChecker):
    '''
        Defines class ProCoverage with attribute(s) and method(s).
        Generates code coverage for project and add to README.md.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | _START_MARKER - README.md section for code coverage.
                | _END_MARKER - README.md section for docs.
            :methods:
                | __init__ - Initials ProCoverage constructor.
                | load_report - Loads report from report file.
                | find_root - Finds root package for project structure.
                | update_readme - Updates README.md file with code coverage.
    '''

    _TOOL_VERBOSE: str = 'ATS_COVERAGE::PRO::PRO_COVERAGE'
    _START_MARKER: str = '### Code coverage'
    _END_MARKER: str = '### Docs'
    _STMTS: str = 'num_statements'
    _MISS: str = 'missing_lines'
    _COVER: str = 'percent_covered_display'

    def __init__(
        self, pro_name: str, readme_path: str, verbose: bool = False
    ) -> None:
        '''
            Initials ProCoverage constructor.

            :param pro_name: Project name
            :type pro_name: <str>
            :param readme_path: Readme file path
            :type readme_path: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSFileError
        '''
        super().__init__()
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([
            ('str:pro_name', pro_name), ('str:readme_path', readme_path)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not exists(f'{pro_name}'):
            raise ATSFileError(f'missing {pro_name}')
        if not exists(f'{readme_path}'):
            raise ATSFileError(f'missing {readme_path}')
        cov = Coverage(source=[f'{pro_name}'])
        cov.start()
        tests: TestSuite = TestLoader().discover(
            f'{pro_name}/../', pattern='*_test.py'
        )
        test_runner = TextTestRunner(verbosity=2)
        test_runner.run(tests)
        cov.stop()
        cov.save()
        self._report_file_name: str = f'{pro_name}_coverage.json'
        self._readme_path: str = readme_path
        self._inside_block: bool = False
        verbose_message(
            verbose, [
                f'{self._TOOL_VERBOSE.lower()}',
                f'prepare code coverage for {pro_name}',
                f'update {readme_path}'
            ]
        )
        cov.json_report(outfile=self._report_file_name)
        success_message([
            f'{self._TOOL_VERBOSE.lower()}',
            f'generates coverage {self._report_file_name}'
        ])

    def load_report(self, verbose: bool = False) -> Dict[str, Any]:
        '''
            Loads report from report file.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Code coverage data report
            :rtype: <Dict[str, Any]>
            :exceptions: None
        '''
        data: Dict[str, Any] = {}
        with open(self._report_file_name, 'r', encoding='utf-8') as report:
            data = load(report)
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} coverage data {data}']
        )
        return data

    def find_root(
        self, module_path: str, verbose: bool = False
    ) -> Optional[Path]:
        '''
            Finds root package for project structure.

            :param module_path: Absolute path
            :type module_path: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Root package for module path
            :rtype: <Optional[Path]>
            :exceptions: ATSTypeError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([(
            'str:module_path', module_path
        )])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        root: Optional[Path] = None
        path: Path = Path(module_path).resolve()
        while path.parent != path:
            if (path / '__init__.py').exists():
                root = path
            path = path.parent
        verbose_message(
            verbose, [
                f'{self._TOOL_VERBOSE.lower()}',
                f' module path {module_path}',
                f'root package {root}'
            ]
        )
        return root

    def update_readme(self, verbose: bool = False) -> bool:
        '''
            Updates README.md file with code coverage.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        status: bool = False
        lines: List[str] = []
        with open(self._readme_path, 'r', encoding='utf-8') as current_file:
            lines = current_file.readlines()
        new_lines: List[str] = []
        coverage: Dict[str, Any] = self.load_report()
        for line in lines:
            if self._START_MARKER in line:
                self._inside_block = True
                new_lines.append(line)
                new_lines.append('\n')
                new_lines.append('| Name | Stmts | Miss | Cover |\n')
                new_lines.append('|------|-------|------|-------|\n')
                file_names: List[str] = coverage['files']
                for name in file_names:
                    root_package: str = basename(str(self.find_root(name)))
                    module: str = name[len(root_package):]
                    file_summary: Dict[str, Any] = coverage['files'][name]
                    report_line: str = f'| `{module}` |'
                    statements: str = file_summary['summary'][self._STMTS]
                    missing: str = file_summary['summary'][self._MISS]
                    covered: str = file_summary['summary'][self._COVER]
                    report_line += f' {statements} |'
                    report_line += f' {missing} |'
                    report_line += f' {covered}% |\n'
                    new_lines.append(report_line)
                    verbose_message(verbose, [report_line])
                total: str = '| **Total** |'
                total_statements: str = coverage['totals'][self._STMTS]
                total_missing: str = coverage['totals'][self._MISS]
                total_covered: str = coverage['totals'][self._COVER]
                total += f' {total_statements} |'
                total += f' {total_missing} |'
                total += f' {total_covered}% |\n'
                new_lines.append(total)
                continue
            elif self._END_MARKER in line:
                self._inside_block = False
                new_lines.append('\n')
                new_lines.append(line)
                continue
            if not self._inside_block:
                new_lines.append(line)
        with open(self._readme_path, 'w', encoding='utf-8') as update_file:
            update_file.writelines(new_lines)
            status = True
        return status
