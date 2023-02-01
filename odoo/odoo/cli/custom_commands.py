import argparse, sys, os, unittest, threading
from tabulate import tabulate

import odoo
from odoo.modules.registry import Registry
from odoo.tools.config import config
from odoo.tests.loader import get_test_modules, unwrap_suite
from odoo.tests.runner import OdooTestResult
from .server import main
from .command import commands
from . import Command

import logging
_logger = logging.getLogger('CustomCommands')

class AbstractCommand(object):
    """ Generic Command to inherit from """

    @property
    def _name(self):
        raise NotImplementedError

    def run_command(self, cmdargs):
        raise NotImplementedError

    def get_parser_arguments(self):
        parser_arguments = []
        parser_arguments.append({
            'args': ['-c', '--config'],
            'kwargs': { 
                'dest': 'config',
                'required': True,
                'help': 'The configuration file to be used'
            }
        })
        parser_arguments.append({
            'args': ['-m', '--module'],
            'kwargs': {
                'dest': 'module',
                'default': None,
                'help': 'Specify the module name to be worked on'
            }
        })
        parser_arguments.append({
            'args': ['-mnf', '--module-names-file'],
            'kwargs': {
                'dest': 'module_names_file',
                'default': None,
                'help': 'Specify a file with module names to be worked on'
            }
        })
        return parser_arguments

    def get_module_names(self):
        module_names = []
        if self.args.module:
            module_names.append(self.args.module)
        if self.args.module_names_file:
            try:
                module_names_file = open(self.args.module_names_file, 'r')
                for module_name in module_names_file.readlines():
                    module_names.append(module_name.strip())
            except:
                _logger.error('It is not possible to read the file: %s' % self.args.module_names_file)
        return module_names

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog="%s %s" % (sys.argv[0].split(os.path.sep)[-1], self._name),
            description=self.__doc__
        )

        for parser_argument in self.get_parser_arguments():
            args = parser_argument['args']
            kwargs = parser_argument['kwargs']
            parser.add_argument(*args, **kwargs)

        self.args, unknown = parser.parse_known_args(args=cmdargs)
        config.parse_config(['--config', self.args.config])

        error = False
        registry = odoo.registry(config['db_name'])
        with registry.cursor() as cr:
            self.run_command(cmdargs)

class Install(Command, AbstractCommand):
    """ Install Command """

    @property
    def _name(self):
        return 'Install'

    def run_command(self, cmdargs):
        modules = env['ir.module.module'].search([('name','in', self.get_module_names())], limit=1)
        for module in modules:
            if module.state != 'installed':
                module.button_immediate_install()
                cr.commit()
            else:
                _logger.error('Module %s cannot be installed!' % self.args.module)

class Update(Command, AbstractCommand):
    """ Update Command """

    @property
    def _name(self):
        return 'Update'

    def run_command(self, cmdargs):
        module_names = self.get_module_names()
        update_key = module_names[0] if len(module_names) == 1 else "all"
        config["update"][update_key] = True
        Registry.new(config['db_name'], update_module=True)

class Test(Command, AbstractCommand):
    """ Test Command """

    @property
    def _name(self):
        return 'Test'

    def get_modules_to_test(self):
        modules = self.get_module_names()
        if not modules:
            cr.execute("SELECT name from ir_module_module WHERE state = 'installed'")
            for row in cr.fetchall():
                modules.append(row[0])
        return modules

    def run_test(self, module_name):
        global current_test
        current_test = module_name
        from odoo.tests.common import OdooSuite
        threading.currentThread().testing = True
        modules = get_test_modules(module_name)
        results = []
        for module in modules:
            tests = unwrap_suite(unittest.TestLoader().loadTestsFromModule(module))
            test_suite = OdooSuite(test for test in tests)
            _logger.info('Running test case %s.', module.__name__)
            result = test_suite(OdooTestResult())
            results.append({
                "module": module_name,
                "test_case":  module.__name__.split(".")[-1],
                "test_case_status": "Success" if result.wasSuccessful() else "Failed",
                "tests_run": result.testsRun
            })
        current_test = None
        threading.currentThread().testing = False
        return results

    def log_test_results(self, test_results):
        if not test_results:
            _logger.info("No tests to run - no results given!")
        else:
            test_result_headers = ['Module', 'Test Case', 'Tests Run', 'Test Case Status']
            formatted_test_results = []
            tests_run = 0
            for test_result in test_results:
                formatted_test_results.append([
                    test_result['module'],
                    test_result['test_case'],
                    test_result['tests_run'],
                    test_result['test_case_status']
                ])
                tests_run += test_result['tests_run']
            formatted_test_result = tabulate(formatted_test_results, tablefmt="github", headers=test_result_headers)
            _logger.info(f"\n\n{formatted_test_result}\n\nRan {tests_run} tests in total.\n\n")

    def run_command(self, cmdargs):
        config["test_enable"] = True
        modules = self.get_modules_to_test()
        test_results = []
        for module_name in modules:
            test_results.extend(self.run_test(module_name))
        self.log_test_results(test_results)
