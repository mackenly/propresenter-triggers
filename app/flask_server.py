from flask import Flask, render_template, request, jsonify
from main import execute_triggers
import logging
import json

app = Flask(__name__)


@app.route('/')
def home():
    # You may want a page to create actions
    # get template from same directory as this script
    return render_template('index.html')


@app.route('/trigger', methods=['POST'])
def execute_action():
    # You may want an endpoint to execute actions
    try:
        data = json.loads(request.data)
    except Exception as e:
        logging.error("Invalid API request JSON")
        return jsonify({'message': 'Invalid JSON'}), 400
    triggers = data.get("triggers")
    triggers_result = execute_triggers(triggers)
    if not triggers_result:
        logging.error("Error executing triggers via API")
        return jsonify({'message': 'Error executing triggers via API'}), 500
    return jsonify({'message': 'Triggers executed successfully'}), 200


if __name__ == "__main__":
    print("Starting Flask server")
    app.run(debug=True)
