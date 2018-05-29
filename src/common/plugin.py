import os


class Plugin(object):
    DEFAULT = {'PF_STRING': "\"\"", 'PF_INT': 0, 'PF_FLOAT': 0, 'PF_BOOL': False}

    def __init__(self, plugin_file, args, plugin_name):
        self.plugin_file = plugin_file
        self.args = args
        self.plugin_name = plugin_name

    def run(self):
        self.create_or_update_plugin_file()
        self.run_plugin()

    def create_or_update_plugin_file(self):
        with open(self.plugin_file) as f:
            plugin_body = f.read()

        register_part = """register("{}", "", "", "", "", "", "", "", {}, [], plugin_main)\nmain()""".format(
            self.plugin_name, self.parse_register_arguments()).replace("'", "")

        plugin = plugin_body + '\n' + register_part

        with open(os.path.expandvars('$GIMP_PLUGIN') + '/' + self.plugin_name + '.py', 'w+') as f:
            f.write(plugin)

        os.system('chmod -R 700 $GIMP_PLUGIN')

    def run_plugin(self):
        name = self.plugin_name.replace('_', '-')
        command = "gimp -i -b '(python-fu-{} RUN-NONINTERACTIVE {})' -b '(gimp-quit 1)'".format(
            name, self.parse_command_arguments())
        os.system(command)

    def parse_register_arguments(self):
        arguments = []
        for arg in vars(self.args):
            gimp_type = self.get_type(getattr(self.args, arg))
            arguments.append('({}, "{}", "", {})'.format(gimp_type, arg, Plugin.DEFAULT[gimp_type]))
        return arguments

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
        for arg in vars(self.args):
            value = getattr(self.args, arg)
            if isinstance(value, str):
                arguments += '\"{}\" '.format(value)
            elif isinstance(value, bool):
                arguments += '{} '.format(int(value))
            else:
                arguments += '{} '.format(value)
        return arguments
