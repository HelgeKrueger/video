from .video_file_segments import VideoFileSegments
from .meta_information import MetaInformation
from .processing_information import ProcessingInformation
from .object_data_for_video import ObjectDataForVideo
try:
    from .video_file import VideoFile
except Exception:
    print("No ffmpeg installed, not all features will be available")
