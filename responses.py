from assign import assign_rides_back
from assign import assign_rides_going
from assign import announce_rides
from assign import get_areas

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!help':
        return "`I\'m a bot beep boop.`"
    
    elif p_message == "!assign_rides_back":
        return str(assign_rides_back())

    elif p_message == "!update_areas":
        get_areas()
        return str('updated spreadsheet for DROPPING OFF people')

    elif p_message == "!assign_rides_going":
        return str(assign_rides_going())

    elif p_message == "!announce_rides":
        return str(announce_rides())

    else:
        return "default message"
        # return ''



