#!/usr/bin/python3

import quail

if not quail.helper.OS_WINDOWS:
    raise AssertionError("This test solution is windows only")

quail.run(
    solution=quail.SolutionGitHub("cmder.zip", "https://github.com/cmderdev/cmder"),
    installer=quail.Installer(
        name='Cmder',
        icon='Cmder.exe',
        binary='Cmder.exe',
        console=False
    ),
    builder=quail.builder.Builder(
        quail.builder.CmdIcon('icon.ico'),
    ),
    ui=quail.UiConsole()
)