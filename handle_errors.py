
'''
This function returns strings based on the error
'''
def handle_error(error):
    if "AccessDenied" in str(error):
        return "Access Denied: You do not have permission to access this resource."
    if "Throttling" in str(error):
        return "Throttling: You have exceeded the allowed request rate."
    return "An unknown error occurred. Please try again later."