import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="The Legend of Ellie Kemper",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["audio/", "data/", "font/", "graphics/",
                                            "map/", "base_level_class.py","cloud.py",
                                            ]}},
    executables = executables

    )