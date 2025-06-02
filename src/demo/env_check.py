"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Environment debugger
    - For debugging the system python installization.
    - Important due to the instability of Azure API calls.
    - I recomend not using conda/venv when making API calls.
"""

import sys
import platform


print(f"""Python metadata:
- Version: {platform.python_version()}
- Implementation: {platform.python_implementation()}
- OS: {platform.system()}
- OS Version: {platform.version()}
- Machine: {platform.machine()}
- Architecture: {platform.architecture()[0]}
- Executable Path: {sys.executable}
""")
