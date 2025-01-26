import streamlit as st


# Function to initialize the game board
def initialize_board():
    return [["" for _ in range(3)] for _ in range(3)]


# Function to check for a win
def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None


# Function to check if the board is full
def is_full(board):
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True


# Main game logic
def main():
    # Initialize session state for the game
    if 'board' not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.turn = "X"
        st.session_state.winner = None
        st.session_state.game_over = False

    board = st.session_state.board
    turn = st.session_state.turn
    winner = st.session_state.winner
    game_over = st.session_state.game_over

    # Display the Tic-Tac-Toe board as a grid of buttons
    st.write(f"Current Turn: {turn}")

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            # If the cell is empty, display a button
            if board[i][j] == "":
                button = cols[j].button("", key=f"{i}-{j}")
                if button and not game_over:
                    board[i][j] = turn
                    # Switch turn
                    st.session_state.turn = "O" if turn == "X" else "X"
                    # Check if the game has a winner
                    winner = check_winner(board)
                    if winner:
                        st.session_state.winner = winner
                        st.session_state.game_over = True
                    elif is_full(board):
                        st.session_state.game_over = True
            else:
                # Display the symbol in the cell if already filled
                cols[j].write(board[i][j])

    # Display the winner or a tie message
    if winner:
        st.write(f"Player {winner} wins!")
    elif game_over:
        st.write("It's a tie!")

    # Reset the game button
    if st.button("Reset Game"):
        st.session_state.board = initialize_board()
        st.session_state.turn = "X"
        st.session_state.winner = None
        st.session_state.game_over = False


# Run the game
if __name__ == "__main__":
    main()
