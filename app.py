from flask import Flask, request
from tasks import send_email, log_current_time

# Create a new Flask application instance.
app = Flask(__name__)

# Define the root route.
@app.route('/')
def index():
    # Get the 'sendmail' parameter from the query string.
    sendmail = request.args.get('sendmail')

    # Get the 'talktome' parameter from the query string.
    talktome = request.args.get('talktome')

    # If 'sendmail' parameter is provided, queue the send_email task.
    if sendmail:
        send_email.delay(sendmail)
        return f"Email to {sendmail} queued for sending."

    # If 'talktome' parameter is provided, queue the log_current_time task.
    if talktome:
        log_current_time.delay()
        return "Current time logged."

    # If neither parameter is provided, return a message indicating how to use the endpoint.
    return "Specify ?sendmail=destination email or ?talktome=1"

# Run the Flask application if this script is executed directly.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
