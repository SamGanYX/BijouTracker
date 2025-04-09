from flask import Flask, render_template, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bijou_votes.db'
db = SQLAlchemy(app)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'increase' or 'decrease'
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    # Check if user has voted today
    last_vote = request.cookies.get('last_vote')
    if last_vote:
        last_vote_date = datetime.fromisoformat(last_vote)
        if datetime.now() - last_vote_date < timedelta(days=1):
            return jsonify({'error': 'You can only vote once per day'}), 400

    vote_type = request.json.get('vote_type')
    if vote_type not in ['increase', 'decrease']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    new_vote = Vote(vote_type=vote_type)
    db.session.add(new_vote)
    db.session.commit()
    
    # Set cookie for 24 hours
    response = make_response(jsonify({'message': 'Vote recorded successfully'}))
    response.set_cookie('last_vote', datetime.now().isoformat(), 
                       max_age=86400,  # 24 hours in seconds
                       httponly=True,
                       samesite='Strict')
    return response

@app.route('/get_votes')
def get_votes():
    # Get all votes from the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    votes = Vote.query.filter(Vote.timestamp >= thirty_days_ago).order_by(Vote.timestamp).all()
    
    # Group votes by day
    daily_votes = {}
    for vote in votes:
        day = vote.timestamp.strftime('%Y-%m-%d')
        if day not in daily_votes:
            daily_votes[day] = {'increase': 0, 'decrease': 0}
        daily_votes[day][vote.vote_type] += 1
    
    # Convert to list format for the frontend
    result = []
    for day in sorted(daily_votes.keys()):
        result.append({
            'date': day,
            'increase': daily_votes[day]['increase'],
            'decrease': daily_votes[day]['decrease']
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 