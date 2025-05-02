from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate_account():
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ['account_number', 'bank_code']):
            return jsonify({
                'is_valid': False,
                'reason': 'Missing required fields'
            }), 400

        # Mock validation logic
        account_num = str(data['account_number'])
        bank_code = str(data['bank_code'])
        
        is_valid = (
            len(account_num) == 10 and 
            account_num.isdigit() and 
            len(bank_code) == 2 and
            bank_code.isalpha()
        )
        
        return jsonify({
            'is_valid': is_valid,
            'reason': 'Valid' if is_valid else 'Invalid account format',
            'anomaly': False  # Mock API doesn't detect anomalies
        })
        
    except Exception as e:
        return jsonify({
            'is_valid': False,
            'reason': f'Validation error: {str(e)}',
            'anomaly': False
        }), 400

if __name__ == "__main__":
    app.run(port=5000, threaded=True)