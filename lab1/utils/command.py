def get_command_attr(command, arg_name):
    arg = command.split(arg_name)
    if len(arg) == 2:
        attr = arg[1].strip()
        return attr
    else:
        return None
