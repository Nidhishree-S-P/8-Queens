from app import QueensGame, app

import pytest  # type: ignore


@pytest.fixture
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


def test_remove_queen(client):
    client.post('/place_queen', json={'row': 0, 'col': 0})
    response = client.post('/remove_queen', json={'row': 0, 'col': 0})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'Queen removed from A8'
    assert data['queens_placed'] == 0


def test_invalid_move(client):
    response = client.post('/move_queen', json={'old_row': 0, 'old_col': 0, 'new_row': 1, 'new_col': 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'No queen at the original position.'


def test_is_safe_position(game):
    assert game.is_safe_position(0, 0)
    assert game.is_safe_position(7, 7)
    game.board[1][1] = 'Q'
    assert not game.is_safe_position(0, 0)
    assert not game.is_safe_position(0, 2)
    assert not game.is_safe_position(2, 0)
    assert not game.is_safe_position(2, 2)
    game.reset_board()


if __name__ == "__main__":
    pytest.main()


