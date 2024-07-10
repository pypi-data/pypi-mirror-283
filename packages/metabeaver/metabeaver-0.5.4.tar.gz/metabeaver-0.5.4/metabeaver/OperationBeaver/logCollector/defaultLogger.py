import logging
from logging.handlers import RotatingFileHandler
import os
import inspect

class Logger:


    _instance = None
    log_counter = 0

    # Instantiate this class as a Singleton class.
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # Create a long with a datetimestamp, index, calling script filename, log severity level, and log message.
    def log(self, message, level=logging.DEBUG, logFolder='logFile', loggerName='metabeaver'):
        ## Determine the highest level of the project, which may contain multiple levels.
        # Set the root directory to /app if run within Docker
        if self.is_docker():
            root_dir = '/app'
        # Traverse until we hit setup.py or a .git file, and terminate on assumption of highest level directory.
        else:
            root_dir = self.get_project_root()

        # Define the path for the log directory + file
        log_dir = os.path.join(root_dir, logFolder)
        os.makedirs(log_dir, exist_ok=True) # Creates directory if not exists, otherwise chills out if already there.
        log_file_path = os.path.join(log_dir, 'log.txt')

        # Configure a logger with a name and log all types of log messages with the logging.DEBUG sensitivity level.
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)

        # Check if the logger already has handlers (to prevent duplicate handlers in case of multiple calls)
        if not logger.handlers:
            handler = RotatingFileHandler(log_file_path,
                                          maxBytes=100000000, #Maximum number of bytes per log. 10^8 = 100MB.
                                          backupCount=5 #Number of log files to keep .
                                          )
            # Define and set the expected format of debug messages
            formatter = logging.Formatter('%(asctime)s - %(index)d - %(filename)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        ## Get the name of the script that called logPrint
        # Go up a level from the function call stack to get the script name
        frame = inspect.stack()[1]
        # Tries to get the module from the second entry in inspect.stack()
        module = inspect.getmodule(frame[0])
        # Default "unknown" if we could not get filename
        script_name = module.__file__ if module else "unknown"

        # Create a log record
        log_record = logger.makeRecord(
            name=loggerName,
            level=level,
            fn=script_name,
            lno=frame.lineno,
            msg=message,
            args=(),
            exc_info=None,
            extra={
                'index': self.log_counter,
            }
        )

        # Log to file
        logger.handle(log_record)

        # Print to console
        print(f"{log_record.name}: "
              f"{log_record.asctime} - "
              f"{log_record.index} - "
              f"{log_record.filename} - "
              f"{log_record.levelname} - "
              f"{log_record.message}"
              )

        self.log_counter += 1

        return log_record

    def is_docker(self) -> bool:
        """Detect if the script is running in a Docker container"""

        # Check for a known Docker path and return true if found
        paths = ["/proc/self/cgroup", "/proc/1/cgroup", "/proc/self mounts"]
        for path in paths:
            if os.path.exists(path):
                with open(path) as file:
                    for line in file:
                        if "docker" in line:
                            return True

        # Check for a known Docker environmental variable and return true if found
        env_vars = ["DOCKER.Runtime", "CONTAINER_runtime"]
        for env_var in env_vars:
            if env_var in os.environ:
                return True

        # Return False for running in Docker if could not find a Docker path or environmental variable
        return False

    def get_project_root(self):
        """Determine the root directory of the project."""

        # Get the current directory
        current_dir = os.path.abspath(os.path.dirname(__file__))
        # Traverse until we reach a .git or setup.py file. Assumes existence.
        while current_dir != os.path.dirname(current_dir):  # Traverse up until reaching the filesystem root
            if any(os.path.isfile(os.path.join(current_dir, marker)) for marker in ['.git', 'setup.py']):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return current_dir  # Fallback to the highest level if no markers found

if __name__ == '__main__':
    beaversLoveLogs = Logger()
    beaversLoveLogs.log('HELLO WORLD I AM A BIG LOG!!!')