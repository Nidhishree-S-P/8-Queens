from flask import Flask, render_template, jsonify, request 
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

BOARD_SIZE = 8

class QueensGame:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.reset_board()
    
    def reset_board(self):
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.queens_placed = 0
        logger.info("Game board reset.")
    
    def is_safe_position(self, row, col):
        for i in range(self.size):
            if self.board[row][i] == 'Q' or self.board[i][col] == 'Q':
                return False
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            r, c = row + dx, col + dy
            while 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] == 'Q':
                    return False
                r += dx
                c += dy
        return True

game = QueensGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_board():
    game.reset_board()
    return jsonify({
        'success': True, 
        'message': 'Game board reset successfully!', 
        'board': game.board
    })

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify(game.board)

@app.route('/move_queen', methods=['POST'])
def move_queen():
    data = request.get_json()
    old_row, old_col = data['old_row'], data['old_col']
    new_row, new_col = data['new_row'], data['new_col']

    if not (0 <= old_row < game.size and 0 <= old_col < game.size and 0 <= new_row < game.size and 0 <= new_col < game.size):
        return jsonify({'success': False, 'message': 'Invalid board position.'})

    if game.board[old_row][old_col] != 'Q':
        return jsonify({'success': False, 'message': 'No queen at the original position.'})

    if game.board[new_row][new_col] is not None:
        return jsonify({'success': False, 'message': 'Cell is already occupied.'})

    if not game.is_safe_position(new_row, new_col):
        return jsonify({'success': False, 'message': 'Invalid move! Queen cannot be placed here.'})

    game.board[old_row][old_col] = None
    game.board[new_row][new_col] = 'Q'

    return jsonify({'success': True, 'message': 'Queen moved successfully!', 'board': game.board})



@app.route('/place_queen', methods=['POST'])
def place_queen():
    data = request.get_json()
    row, col = data['row'], data['col']
    
    if not (0 <= row < game.size and 0 <= col < game.size):
        return jsonify({
            'success': False, 
            'message': 'Invalid board position.'
        })
    
    if game.board[row][col] is not None:
        return jsonify({
            'success': False, 
            'message': 'Invalid move! Queen placement conflicts with existing queens.'
        })
    
    if not game.is_safe_position(row, col):
        return jsonify({
            'success': False, 
            'message': 'Invalid move! Queen placement conflicts with existing queens.'
        })
    
    game.board[row][col] = 'Q'
    game.queens_placed += 1 
    
    logger.info(f"Queen placed at position ({row}, {col})")
    
    return jsonify({
        'success': True, 
        'message': f'Queen placed at {chr(col + 65)}{game.size - row}', 
        'board': game.board,
        'queens_placed': game.queens_placed
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
        
        logger.info(f"Queen removed from position ({row}, {col})")
        
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


@app.route('/check_win', methods=['GET'])
def check_win():
    try:
        remaining_queens = game.size - game.queens_placed
        if game.queens_placed == game.size:
            logger.info("Player has won the game!")
            return jsonify({
                'success': True,
                'message': 'Congratulations! All queens are placed without conflicts!'
            })
        return jsonify({
            'success': False,
            'message': f'Player lost the game! Could not place all 8 queens. {remaining_queens} queens remaining to be placed.'
        })
    except Exception as e:
        logger.error(f"Error checking win: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while checking the win.'})


if __name__ == '__main__':
    app.run(debug=True)
    
   