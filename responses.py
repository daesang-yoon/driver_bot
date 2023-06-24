

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!help':
        return "`I\'m a bot beep boop.`"
    
    else:
        return "default message"



