import logging
from typing import Optional

from aio_pika import Channel

# infrastructure things

logger = logging.getLogger("tasks-api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

rabbit_channel: Optional[Channel] = None
