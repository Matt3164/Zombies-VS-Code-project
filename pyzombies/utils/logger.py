
import logging # needed
import sys # needed

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

logger = logging.getLogger("zombies")
