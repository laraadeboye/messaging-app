from flask import Flask, request, jsonify
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
    if talktome is not None:
        log_current_time.delay()
        return "Current time logged."

    # If neither parameter is provided, return a message indicating how to use the endpoint.
    return "Specify ?sendmail=destination email or ?talktome"

# Define a route to fetch the logs.
@app.route('/logs')
def get_logs():
    log_file_path = '/var/log/messaging_system.log'
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()
        return jsonify(logs)
    except Exception as e:
        return str(e), 500

# Run the Flask application if this script is executed directly.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
