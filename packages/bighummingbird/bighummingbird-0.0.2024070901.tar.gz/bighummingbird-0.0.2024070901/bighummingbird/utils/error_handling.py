import sys
from .constants import BASE_CLIENT_URL, BASE_DOC_URL
# Move this to environment variable like BASE_URL? 
SHOW_STACK_TRACE = False

from .display_util import blue, blue_underline, red_check, reset_color, orange_exclamation, orange, bold, reset_font, right_angle

DISCORD_CHANNEL = "https://discord.gg/sfDFaHYT"
error_code_message_map = {
    'failed_to_create_evaluation': f'{red_check()}Oops! Something went wrong on our side.{reset_color()} We couldn\'t create an evaluation set. \n Please reach out to us at {blue_underline(DISCORD_CHANNEL)}. We\'re here to help!',
    'invalid_api_key': f'🚧 {orange()}Invalid API Key.{reset_color()} Please verify your API Key or generate a new one at {blue_underline(BASE_CLIENT_URL)} Workspace Settings tab.',
    'exceed_storage_limit': f'🚧 {orange()}You\'ve reached your storage limit!{reset_color()} To keep everything running smoothly, please visit our Pricing Page {blue_underline(f"{BASE_CLIENT_URL}/pricing")} to explore upgrade options that suit your needs.',
    'unexpected_error': f'{red_check()}Oops! Something went wrong on our end.{reset_color()} Please reach out to us at {blue_underline(DISCORD_CHANNEL)}. We\’re here to help!{reset_color()}',
    'scoring_func_invalid_return_type': f'{red_check()} Something went wrong while scoring.{reset_color()} Please double check that the passing function passed to the judge returns either an int or float type.',
    'passing_func_invalid_return_type': f'{red_check()} Something went wrong while determining whether the score passed or not.{reset_color()} Please double check that the passing_criteria function passed to the judge returns a bool type.',
}

class BHBCustomException(Exception):
    def __init__(self, code, message=None):
        super().__init__(code)
        self.code = code
        self.message = message
    
    def __str__(self):
        if self.code == 'judge_not_found':
            return f'{red_check()} Cannot find judge {bold()}{self.message}{reset_font()}.{reset_color()} Please check out our documentation at {blue_underline(f"{BASE_DOC_URL}/docs/concepts/judge")} for more information on how to create a judge.'
        if self.code == 'failed_create_judge':
            return f'{red_check()} Failed to create judge {bold()}{self.message}{reset_font()}.{reset_color()} Please check out out documentation {blue_underline(f"{BASE_DOC_URL}/docs/concepts/judge")} for more information on how to create a judge.'
        elif self.code == 'dataset_tag_not_found':
            return f'{red_check()} Oops! We couldn\'t find dataset {bold()}{self.message}{reset_font()} when creating the judge.{reset_color()} Please double-check the dataset tag for any typos. If you\'re still having trouble, our documentation might have the answer! {blue_underline(f"{BASE_DOC_URL}/docs/concepts/dataset")}'
        elif self.code == 'failed_download_dataset':
            return f'{red_check()} Oops! Something went wrong on our side. We couldn\'t download dataset {bold()}{self.message}{reset_font()}.{reset_color()} \n Please reach out to us at {blue_underline(DISCORD_CHANNEL)}. We\'re here to help!'
        elif error_code_message_map[self.code]:
            return error_code_message_map[self.code]
        else:
            return error_code_message_map['unexpected_error']


def on_crash(exctype, value, traceback):
    if SHOW_STACK_TRACE or exctype != BHBCustomException:
        sys.__excepthook__(exctype, value, traceback)
    else:
        print(value)
sys.excepthook = on_crash


