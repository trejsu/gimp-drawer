import os
from subprocess import Popen, PIPE

REGISTER_ARG = '({}, "{}", "", {})'
RUN_PLUGIN = "gimp -i -b '(python-fu-{} RUN-NONINTERACTIVE {})' -b '(gimp-quit 1)'"
TYPE_TO_DEFAULT_VALUE = {'PF_STRING': "\"\"", 'PF_INT': 0, 'PF_FLOAT': 0, 'PF_BOOL': False}
REGISTER = """register("{}", "", "", "", "", "", "", "", {}, [], plugin_main)\nmain()"""


class Plugin(object):

    def __init__(self, plugin_file, plugin_name, args, dict_args=False):
        self.plugin_file = plugin_file
        self.args = args
        self.plugin_name = plugin_name
        self.dict_args = dict_args

    def run(self):
        self.create_or_update_plugin_file()
        self.run_plugin()

    def run_as_subprocess(self):
        self.create_or_update_plugin_file()
        pid = self.run_plugin_as_subprocess()
        return pid

    def create_or_update_plugin_file(self):
        with open(self.plugin_file) as f:
            plugin_body = f.read()

        register_part = REGISTER\
            .format(self.plugin_name, self.parse_register_arguments())\
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
        return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

    def get_cmd(self):
        name = self.plugin_name.replace('_', '-')
        cmd = RUN_PLUGIN.format(name, self.parse_command_arguments())
        return cmd

    def parse_register_arguments(self):
        arguments = []
        for arg in self.arg_keys():
            gimp_type = self.get_type(self.value(arg))
            arguments.append(REGISTER_ARG.format(gimp_type, arg, TYPE_TO_DEFAULT_VALUE[gimp_type]))
        return arguments

    def value(self, arg):
        return self.args[arg] if self.dict_args else getattr(self.args, arg)

    def arg_keys(self):
        return self.args.keys() if self.dict_args else vars(self.args)

    @staticmethod
    def get_type(value):
        if isinstance(value, str):
            return 'PF_STRING'
        elif isinstance(value, int):
            return 'PF_INT'
        elif isinstance(value, float):
            return 'PF_FLOAT'
        elif isinstance(value, bool):
            return 'PF_BOOL'
        else:
            raise RuntimeError('unknown argument type')

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
