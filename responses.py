from assign import assign_rides_back
from assign import assign_rides_going
from assign import announce_rides_going
from assign import announce_rides_back
from assign import get_areas
from assign import update_signups

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!help':
        return "`I\'m a bot that helps out with soon rides!`"
    
    elif p_message == "!assign_rides_back":
        return str(assign_rides_back())

    elif p_message == "!update_areas":
        get_areas()
        return str('updated spreadsheet for DROPPING OFF people')

    elif p_message == "!assign_rides_going":
        return str(assign_rides_going())

    elif p_message == "!announce_rides_going":
        return str(announce_rides_going())
    
    elif p_message == "!announce_rides_back":
        return str(announce_rides_back())
    
    elif p_message == "!update_signups":
        return str(update_signups())

    else:
        return "default message"
        # return ''



