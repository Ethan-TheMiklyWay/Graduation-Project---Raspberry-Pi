import variable


def main():
    """"""
    from view.main_view import start_main_view
    start_main_view()

    """
    from view.login_view import start_login_view
    start_login_view()
    if variable.login_state:
        from view.main_view import start_main_view
        start_main_view()
    """

    """
    # this is for one line test
    
    from terminal.command_translate import Execute
    exe = Execute("terminal/host.ini")
    string = "node get all"
    # string = "node set 00101 status=0 mqttfinding_wait_interview=3000"
    exe.execute(string)
    """


    """
    # this is for terminal
    import terminal.host_main as cmd
    cmd.host_ini = "terminal/host.ini"
    cmd.main()
    """


if __name__ == "__main__":
    main()
