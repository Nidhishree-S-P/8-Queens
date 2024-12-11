import pytest # type: ignore
from app import QueensGame, app  


@pytest.fixture # type: ignore

def game():
    return QueensGame()

def client():
    with app.test_client() as client:
        yield client


def test_reset_board(client):
    response = client.post('/reset')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'Game board reset successfully!'


def test_place_queen(client):
    response = client.post('/place_queen', json={'row': 0, 'col': 0})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'Queen placed at A8'
    assert data['queens_placed'] == 1


def test_move_queen(client):
   
    client.post('/place_queen', json={'row': 0, 'col': 0})
    response = client.post('/move_queen', json={'old_row': 0, 'old_col': 0, 'new_row': 1, 'new_col': 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'Queen moved successfully!'

ef test_remove_queen(client):
    # Place a queen first
    client.post('/place_queen', json={'row': 0, 'col': 0})
    
    # Remove it
    response = client.post('/remove_queen', json={'row': 0, 'col': 0})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'Queen removed from A8'
    assert data['queens_placed'] == 0


def test_invalid_move(client):
    # Try to move a queen without placing one first
    response = client.post('/move_queen', json={'old_row': 0, 'old_col': 0, 'new_row': 1, 'new_col': 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'No queen at the original position.'


def test_is_safe_position(self):
    self.assertTrue(game.is_safe_position(0, 0))  
    self.assertTrue(game.is_safe_position(7, 7))  
    game.board[1][1] = 'Q'  
    self.assertFalse(game.is_safe_position(0, 0)) 
    self.assertFalse(game.is_safe_position(0, 2))  
    self.assertFalse(game.is_safe_position(2, 0))  
    self.assertFalse(game.is_safe_position(2, 2)) 
    self.assertFalse(game.is_safe_position(2, 3))  
