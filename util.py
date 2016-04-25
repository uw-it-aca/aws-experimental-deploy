import settings


def set_ansible_display():
    from ansible.utils.display import Display
    verbosity = getattr(settings, 'VERBOSITY', 0)
    display = Display(verbosity=verbosity)
    return display
