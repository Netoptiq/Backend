from django.contrib.auth import authenticate

# Example credentials
username = 'admin1'
password = 'admin1'

# Authenticate user
user = authenticate(username=username, password=password)

if user is not None:
    # Check if the user account is active
    if user.is_active:
        # The user account is active, proceed with authentication
        print("User is active. Authentication successful.")
    else:
        # The user account is not active
        print("User account is not active.")
else:
    # Authentication failed
    print("Authentication failed. No user found with the given credentials.")
