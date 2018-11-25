import os
from subprocess import Popen

REGISTER_ARG = '({}, "{}", "", {})'
RUN_PLUGIN = "gimp -i -f {} -b '(python-fu-{} RUN-NONINTERACTIVE {})' -b '(gimp-quit 1)'"
TYPE_TO_DEFAULT_VALUE = {'PF_STRING': "\"\"", 'PF_INT': 0, 'PF_FLOAT': 0, 'PF_BOOL': False}
REGISTER = """register("{}", "", "", "", "", "", "", "", {}, [], plugin_main)\nmain()"""


class Plugin(object):

    def __init__(self, *, plugin_file, plugin_name, args, list_args=False):
        self.plugin_file = plugin_file
        self.args = args
        self.plugin_name = plugin_name
        self.list_args = list_args
        self.verbose = False

    def run(self, verbose=False):
        self.verbose = verbose
        self.create_or_update_plugin_file()
        self.run_plugin()

    def run_as_subprocess(self):
        self.create_or_update_plugin_file()
        pid = self.run_plugin_as_subprocess()
        return pid

    def create_or_update_plugin_file(self):
        with open(self.plugin_file) as f:
            plugin_body = f.read()

        register_part = REGISTER \
            .format(self.plugin_name, self.parse_register_arguments()) \
            .replace("'", "")

        plugin = plugin_body + '\n' + register_part

        with open(os.path.expandvars('$GIMP_PLUGIN') + '/' + self.plugin_name + '.py', 'w+') as f:
            f.write(plugin)

        os.system('chmod -R 700 "$GIMP_PLUGIN"')

    def run_plugin(self):
        cmd = self.get_cmd()
        os.system(cmd)

    def run_plugin_as_subprocess(self):
        cmd = self.get_cmd()
        return Popen(cmd, shell=True)

    def get_cmd(self):
        name = self.plugin_name.replace('_', '-')
        cmd = RUN_PLUGIN.format('--stack-trace-mode=always --verbose' if self.verbose else '',
                                name, self.parse_command_arguments())
        return cmd

    def parse_register_arguments(self):
        arguments = []
        for arg in self.arg_keys():
            gimp_type = self.get_type(self.value(arg))
            arguments.append(REGISTER_ARG.format(gimp_type, arg, TYPE_TO_DEFAULT_VALUE[gimp_type]))
        return arguments

    def value(self, arg):
        return dict(self.args)[arg] if self.list_args else getattr(self.args, arg)

    def arg_keys(self):
        return [param for param, value in self.args] if self.list_args else vars(self.args)

    @staticmethod
    def get_type(value):
        python_to_gimp_type = {
            str: 'PF_STRING',
            int: 'PF_INT',
            float: 'PF_FLOAT',
            bool: 'PF_BOOL'
        }
        for python, gimp in python_to_gimp_type.items():
            if isinstance(value, python):
                return gimp
        raise RuntimeError('unknown argument type for value: {}'.format(value))

    def parse_command_arguments(self):
        arguments = ''
        for arg in self.arg_keys():
            value = self.value(arg)
            if isinstance(value, str):
                arguments += '\"{}\" '.format(value)
            elif isinstance(value, bool):
                arguments += '{} '.format(int(value))
            else:
                arguments += '{} '.format(value)
        return arguments
