from flask import Flask, render_template, jsonify, request
from generator import SudokuGenerator

app = Flask(__name__)
sg = SudokuGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new_puzzle')
def new_puzzle():
    difficulty = request.args.get('difficulty', default=0.5, type=float)
    solution = sg.generate_sudoku()
    board = sg.redact_sudoku(solution, difficulty)
    return jsonify({
        'board': board.tolist(),
        'solution': solution.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)