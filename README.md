# Bijou Benchmark Vote

A simple web application that allows users to vote on whether the Bijou benchmark should increase or decrease. The application features a real-time graph showing the voting trends.

## Features

- Vote for increase or decrease
- Real-time graph visualization
- SQLite database for vote storage
- Modern, responsive UI

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## How to Use

1. Click the "Increase" button to vote for an increase in the benchmark
2. Click the "Decrease" button to vote for a decrease in the benchmark
3. Watch the real-time graph update with the voting trends

The graph shows the cumulative count of increase and decrease votes over time.
