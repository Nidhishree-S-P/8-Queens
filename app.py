from flask import Flask, render_template, jsonify, request
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class QueensGame:
    def __init__(self, size=8):
        self.size = size
        self.reset_board()

    def reset_board(self):
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.queens_placed = 0
        logger.info("Game board reset.")

    def is_safe_position(self, row, col):
        for i in range(self.size):
            if self.board[row][i] or self.board[i][col]:
                return False
        for r, c in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            curr_r, curr_c = row + r, col + c
            while 0 <= curr_r < self.size and 0 <= curr_c < self.size:
                if self.board[curr_r][curr_c]:
                    return False
                curr_r += r
                curr_c += c
        return True

    def check_win(self):
        return self.queens_placed == self.size

game = QueensGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_board():
    game.reset_board()
    return jsonify({
        'success': True, 
        'message': 'Game reset! Place your first queen.', 
        'board': game.board
    })

@app.route('/place_queen', methods=['POST'])
def place_queen():
    data = request.get_json()
    row, col = data['row'], data['col']
    if not (0 <= row < game.size and 0 <= col < game.size):
        return jsonify({
            'success': False, 
            'message': 'Invalid board position.'
        })
    if game.board[row][col] or not game.is_safe_position(row, col):
        return jsonify({
            'success': False, 
            'message': 'Cannot place a queen here!'
        })
    game.board[row][col] = 'Q'
    game.queens_placed += 1 
    win_status = game.check_win()
    win_message = 'Congratulations! You solved the 8 Queens Challenge!' if win_status else ''
    return jsonify({
        'success': True, 
        'message': f'Queen placed at {chr(col + 65)}{game.size - row}', 
        'board': game.board,
        'queens_placed': game.queens_placed,
        'win': win_status,
        'win_message': win_message
    })

@app.route('/remove_queen', methods=['POST'])
def remove_queen():
    data = request.get_json()
    row, col = data['row'], data['col']
    if not (0 <= row < game.size and 0 <= col < game.size):
        return jsonify({
            'success': False, 
            'message': 'Invalid board position.'
        })
    if game.board[row][col] == 'Q':
        game.board[row][col] = None
        game.queens_placed -= 1
        return jsonify({
            'success': True, 
            'message': f'Queen removed from {chr(col + 65)}{game.size - row}', 
            'board': game.board,
            'queens_placed': game.queens_placed
        })
    return jsonify({
        'success': False, 
        'message': 'No queen at the selected position.'
    })

if __name__ == '__main__':
    app.run(debug=True)
    
   
