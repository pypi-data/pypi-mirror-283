from thumbor.filters import BaseFilter, filter_method, PHASE_PRE_LOAD
import thumbor.filters.format
from thumbor.utils import logger

from thumbor_video_engine.compat import filter_retval


ALLOWED_FORMATS = list(thumbor.filters.format.ALLOWED_FORMATS) + [
    "webm",
    "mp4",
    "hevc",
    "h264",
    "h265",
    "vp9",
]


class Filter(BaseFilter):
    phase = PHASE_PRE_LOAD

    @filter_method(BaseFilter.String)
    def format(self, format):
        logger.debug("Setting format to %s" % format)
        if format.lower() not in ALLOWED_FORMATS:
            logger.warning("Format not allowed: %s" % format.lower())
            self.context.request.format = None
        else:
            logger.debug("Format specified: %s" % format.lower())
            self.context.request.format = format.lower()

        return filter_retval()
