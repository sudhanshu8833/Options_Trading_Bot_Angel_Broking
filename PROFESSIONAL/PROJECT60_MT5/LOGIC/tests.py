from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()

# Replace the time part with midnight
midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

print("Current date and time:", now)
print("Midnight today:", midnight_today)
