
import sys
import json
from loguru import logger

# # ======================================
# #           Part 01
# # ======================================

# logger.remove(handler_id=0)
# logger.add(sink=sys.stdout, level="TRACE")

# logger.trace("A trace message.")
# logger.debug("A debug message.")
# logger.info("An info message.")
# logger.success("A success message.")
# logger.warning("A warning message.")
# logger.error("An error message.")
# logger.critical("A critical message.")

# # ======================================
# #            Part 02
# # ======================================

# logger.remove(handler_id=0)

# level = "INFO"
# sink = sys.stdout
# serialize = True

# fmt_line = "<cyan>{line}</cyan>"
# fmt_name = "<cyan>{name}</cyan>"
# fmt_time = "{time:YYYY-MM-DD HH:mm:ss}"
# fmt_level = "<level>{level: <8}</level>"
# fmt_message = "<level>{message}</level>"
# fmt_function = "<cyan>{function}</cyan>"
# format = f"{fmt_time} | {fmt_level} | {fmt_name}:{fmt_function}:{fmt_line} - {fmt_message}"

# logger.add(
#     sink=sink, 
#     level=level, 
#     format=format,
#     serialize=serialize
# )

# logger.info("An info message.")
# logger.warning("A warning message.")
# logger.error("An error message.")


# # ======================================
# #            Part 03
# # ======================================

# def serialize(record):
#     subset = {
#         "calendar": record["time"].strftime("%d-%m-%Y"),
#         "time": record["time"].strftime("%H:%M:%S"),
#         "message": record["message"],
#         "level": record["level"].name,
#         "name": record["name"],
#         "function": record["function"] if record["function"] != "<module>" else "",
#     }
#     return json.dumps(subset)


# def patching(record):
#     record["extra"]["serialized"] = serialize(record)


# # Parameters:
# _handler_id = 0
# _sink = sys.stdout
# _level = "WARNING"

# logger.remove(handler_id=_handler_id)
# logger = logger.patch(patcher=patching)

# logger.add(
#     sink=_sink, 
#     level=_level,
#     format="{extra[serialized]}",
# )

# logger.info("An info message.")
# logger.warning("A warning message.")
# logger.error("An error message.")

# # ======================================
# #            Part 04
# # ======================================

# def serialize(record):
#     subset = {
#         "calendar": record["time"].strftime("%d-%m-%Y"),
#         "time": record["time"].strftime("%H:%M:%S"),
#         "message": record["message"],
#         "level": record["level"].name,
#         "name": record["name"],
#         "function": record["function"] if record["function"] != "<module>" else "",
#         "line": record["line"],
#         "extra": record["extra"] if record["extra"] else {},
#     }
#     return json.dumps(subset)


# def patching(record):
#     record["extra"]["serialized"] = serialize(record)


# # Parameters:
# _handler_id = 0

# _serialize_stream = False
# _sink_stream = sys.stdout
# _level_stream = "DEBUG"
# _format_stream = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# _serialize_file = False
# _sink_file = "app.log"
# _level_file = "WARNING"
# _format_file = "{extra[serialized]}"

# logger.remove(handler_id=_handler_id)
# logger = logger.patch(patcher=patching)

# logger.add(
#     sink=_sink_stream, 
#     level=_level_stream,
#     format=_format_stream,
#     serialize=_serialize_stream,
# )

# logger.add(
#     sink=_sink_file, 
#     level=_level_file,
#     format=_format_file,
#     serialize=_serialize_file,
# )

# childLogger= logger.bind(user_id="800.100.200-22")

# logger.info("An info message.")
# childLogger.info("An info message.")

# logger.warning("A warning message.")
# childLogger.warning("A warning message.")

# logger.error("An error message.")
# childLogger.error("An error message.")

# ======================================
#            Part 05
# ======================================
import os
import sys

currentFilePath = os.path.abspath(__file__)
currentDirectory = os.path.dirname(currentFilePath)
pythonPath = os.path.dirname(currentDirectory)


def serialize(record):
    full_file_path = record["file"].path
    relative_file_path = full_file_path.replace(pythonPath, "")
    subset = {
        "calendar": record["time"].strftime("%d-%m-%Y"),
        "time": record["time"].strftime("%H:%M:%S"),
        "message": record["message"],
        "level": record["level"].name,
        "name": record["name"],
        "function": record["function"] if record["function"] != "<module>" else "",
        "line": record["line"],
        "extra": record["extra"] if record["extra"] else {},
        "exception": record["exception"] if record["exception"] else {},
        "file_name": record["file"].name,
        "file_path": relative_file_path,
    }
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)

def child_logger_info(msg):
    logger.info(msg)

def child_logger_warning(msg):
    logger.warning(msg)

def child_logger_error(msg):
    logger.error(msg)


# Parameters:
_handler_id = 0
_user_id = "800.100.200-22"

_serialize_stream = False
_sink_stream = sys.stdout
_level_stream = "DEBUG"
_format_stream = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

_serialize_file = False
_sink_file = "app.log"
_level_file = "WARNING"
_format_file = "{extra[serialized]}"

logger.remove(handler_id=_handler_id)
logger = logger.patch(patcher=patching)

logger.add(
    sink=_sink_stream, 
    level=_level_stream,
    format=_format_stream,
    serialize=_serialize_stream,
)

logger.add(
    sink=_sink_file, 
    level=_level_file,
    format=_format_file,
    serialize=_serialize_file,
)

with logger.contextualize(user_id=_user_id) as childLogger:
    child_logger_info("An info message.")
    child_logger_warning("A warning message.")
    child_logger_error("An error message.")









