# PathlibIO

CLI functionality of Python's Pathlib module

A single script `pathlibio` contains the functionality, a wrapper around most of `pathlib.Path`'s methods and properties

Help is available at `pathlibio -h`

Reads from stdin if `-` is passed as the path, performing actions on each line read as a path. In this case test-like functions such as `is_socket` cause the script to exit after the first false result.
