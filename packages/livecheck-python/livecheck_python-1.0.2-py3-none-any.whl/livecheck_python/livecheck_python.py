import sys
import logging
import json
import requests
import traceback
import atexit
import pytz
from datetime import datetime

class LiveCheckStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream)
        self.previous_message_ended_with_newline = True

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream

            if not self.previous_message_ended_with_newline:
                stream.write('\n')

            stream.write(msg)
            if not msg.endswith('\n'):
                stream.write('\n')
                self.previous_message_ended_with_newline = False
            else:
                self.previous_message_ended_with_newline = True
            
            self.flush()
        except Exception:
            self.handleError(record)

livecheck_logger = logging.getLogger(__name__)
livecheck_logger.setLevel(logging.INFO)
livecheck_handler = LiveCheckStreamHandler()
livecheck_formatter = logging.Formatter('%(asctime)s - LiveCheck - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
livecheck_handler.setFormatter(livecheck_formatter)
livecheck_logger.addHandler(livecheck_handler)

class LiveCheckAPI:

    API_URL = 'https://api.livecheck.dev/log'
    TIME_FORMAT = '%Y%m%d%H%M%S'
    TZ = pytz.timezone('UTC')

    def get_current_time(self):
        current_time = datetime.now(self.TZ)
        return current_time, current_time.strftime(self.TIME_FORMAT)

    def calculate_time_difference(self, time_str1, time_str2):
        datetime1 = datetime.strptime(time_str1, self.TIME_FORMAT).replace(tzinfo=self.TZ)
        return (time_str2 - datetime1).total_seconds()

    def __init__(self):
        _, self.run_start = self.get_current_time()
        self.num_logs = 0
        self.last_log_time = 0
        self.last_save_time = 0
        self.logs = []

    def log(self, your_id, access_key, token, project_name, log_id, max_logs_per_save,
            max_logs_per_run, min_log_period, min_save_period, notification_period,
            hyperparams=None, data=None, exception=None, handle_exit=False, last=False):
        
        current_time, timestamp = self.get_current_time()

        if not handle_exit and exception is None:
            if self.last_log_time and self.calculate_time_difference(self.last_log_time, current_time) < min_log_period:
                livecheck_logger.warning('Time between two logs is too short. Must be longer than %d seconds.', min_log_period)
                return False, None
            self.last_log_time = timestamp

        if not handle_exit:
            log_entry = {'log_id': log_id, 'timestamp': timestamp}
            if hyperparams:
                log_entry['params'] = hyperparams
            if exception:
                log_entry['exception'] = exception
            elif data:
                log_entry['data'] = data
            self.logs.append(log_entry)

            if self.last_save_time and self.calculate_time_difference(self.last_save_time, current_time) < min_save_period and (len(self.logs) + self.num_logs) % max_logs_per_run != 0:
                return False, None
            
        if not self.logs:
            return False, None
        if len(self.logs) > max_logs_per_save:
            self.logs = self.logs[-max_logs_per_save:]
        
        payload = {
            'your_id': your_id,
            'access_key': access_key,
            'token': token,
            'project_name': project_name,
            'run_start': self.run_start,
            'noti_period': notification_period,
            'logs': self.logs}
        if last is True:
            payload['last'] = last
        payload_json = json.dumps(payload)
        
        response = requests.post(self.API_URL, data=payload_json)
        # TODO: Print response based on log level
        self.last_save_time = timestamp
        
        if response.status_code == 201:
            self.num_logs += len(self.logs)
            self.logs = []
            return True, response.json()
        return False, response.json()

class LiveCheck:

    def __init__(self, your_id, access_key, project_name='', hyperparams=None, notification_period=0):
        self.your_id = your_id
        self.access_key = access_key
        self.token = ''
        self.project_name = project_name
        self.hyperparams = self.process_parameters(hyperparams)
        self.notification_period = notification_period
        self.max_logs_per_save = 0
        self.max_logs_per_run = 0
        self.min_log_period = 0
        self.min_save_period = 0
        self.log_id = 0
        self.last_message = ''
        self.stop_log = False
        self.api = LiveCheckAPI()

        sys.excepthook = self.live_check_exception_handler
        atexit.register(self.exit_handler)

    def live_check_exception_handler(self, exc_type, exc_value, exc_traceback):
        exception_details = [
            {'name': 'exception', 'type': 'str', 'value': exc_type.__name__},
            {'name': '', 'type': 'str', 'value': str(exc_value)},
            {'name': 'traceback', 'type': 'str', 'value': ''.join(traceback.format_tb(exc_traceback, limit=-1))}
        ]

        is_successful, response = self.api.log(
            self.your_id, self.access_key, self.token, self.project_name, self.log_id + 1,
            self.max_logs_per_save, self.max_logs_per_run, self.min_log_period, self.min_save_period,
            self.notification_period, exception=exception_details, last=True
        )
        self.process_log_response(is_successful, response)
        self.stop_log = True

        traceback.print_exception(exc_type, exc_value, exc_traceback)

    def exit_handler(self):
        self.api.log(
            self.your_id, self.access_key, self.token, self.project_name, self.log_id + 1,
            self.max_logs_per_save, self.max_logs_per_run, self.min_log_period, self.min_save_period,
            self.notification_period, handle_exit=True, last=True
        )

    def process_parameters(self, params=None):
        if params is None:
            return None
        if not isinstance(params, dict):
            raise TypeError('Invalid object type. A dictionary object is required.')
        if not params:
            raise ValueError('Invalid value. The dictionary must not be empty.')
        
        processed_params = [{'name': name, 'type': type(value).__name__, 'value': value} 
                            for name, value in params.items() 
                            if isinstance(value, (int, float, bool, str))]
        if len(processed_params) != len(params):
            raise TypeError('Invalid object type. Only int, float, bool, and str are supported.')

        return processed_params
    
    def process_log_response(self, is_successful, response):
        if is_successful and response.get('success'):
            self.token = response['token']
            self.hyperparams = None
            self.max_logs_per_save = response['max_logs_per_save']
            self.max_logs_per_run = response['max_logs_per_run']
            self.min_log_period = response['min_log_period']
            self.min_save_period = response['min_save_period']
        elif response and 'message' in response:
            self.stop_log = True
            self.last_message = response['message']
            livecheck_logger.warning(self.last_message)

    def set_project_name(self, value):
        self.project_name = value

    def set_hyperparams(self, value):
        self.hyperparams = self.process_parameters(value)

    def set_notification_period(self, value):
        self.notification_period = value

    def log(self, value, log_id=None):
        if self.stop_log:
            livecheck_logger.warning(self.last_message)
            return
        
        data = self.process_parameters(value)
        self.log_id = log_id if log_id is not None else self.log_id + 1
        is_successful, response = self.api.log(
            self.your_id, self.access_key, self.token, self.project_name, self.log_id,
            self.max_logs_per_save, self.max_logs_per_run, self.min_log_period,
            self.min_save_period, self.notification_period, self.hyperparams, data=data
        )
        self.process_log_response(is_successful, response)