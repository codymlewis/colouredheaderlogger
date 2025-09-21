# Coloured Header Logger
[![Tests](https://github.com/codymlewis/colouredheaderlogger/actions/workflows/main.yml/badge.svg)](https://github.com/codymlewis/colouredheaderlogger/actions/workflows/main.yml)

A formatter to colour only the header part of logs according to severity.

This package provides 1 function and 1 class:
- The function `get_ansi_colour(fg=None, bg=None, style=None)`, returns the ansi colour code string corresponding to the specified foreground (fg), background (bg), and style, for each provided.
- The class `ColouredFormatter` is a formatter to be used within a logging stream handler to provide the coloured header format. The constructor for ColouredFormatter can optionally be provided with string arguments specifying the colour of each level of output, this can be either a direct ansi string, the output of `get_ansi_colour`, or the name of the foreground colour.

## Usage Example

The following example provides the format to a simple logger that outputs to stdout:

```python
import logging
import sys

import chl

logger = logging.getLogger("chl usage example")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(chl.ColouredFormatter(fmt="[chl example - %(levelname)s] %(message)s", info="yellow"))
logger.addHandler(sh)
logger.info("test")
```

The output should be `[chl example - INFO] test` where `[chl example - INFO]` is yellow and `test` is the default font colour of your terminal/console.
