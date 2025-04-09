from app import app, db, Vote
from datetime import datetime, timedelta
import random

def add_dummy_data():
    with app.app_context():
        # Clear existing data
        Vote.query.delete()
        db.session.commit()

        # Generate data for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        current_date = start_date
        while current_date <= end_date:
            # Generate 5-15 votes per day
            num_votes = random.randint(5, 15)
            
            for _ in range(num_votes):
                # Randomly choose increase or decrease
                vote_type = random.choice(['increase', 'decrease'])
                
                # Add some randomness to the time within the day
                random_hours = random.randint(0, 23)
                random_minutes = random.randint(0, 59)
                vote_time = current_date.replace(
                    hour=random_hours,
                    minute=random_minutes
                )
                
                new_vote = Vote(
                    vote_type=vote_type,
                    timestamp=vote_time
                )
                db.session.add(new_vote)
            
            current_date += timedelta(days=1)
        
        db.session.commit()
        print("Dummy data added successfully!")

if __name__ == "__main__":
    add_dummy_data() 