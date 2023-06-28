from assign import assign_rides_back

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!help':
        return "`I\'m a bot beep boop.`"
    
    elif p_message == "!assign_rides_back":
        return str(dict(assign_rides_back()))

    else:
        return "default message"



