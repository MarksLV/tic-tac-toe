import configparser
from db_connect_prc import get_db_connection

# DEFAULT PLAYER NAMES SETUP
def get_default_usernames():
    config = configparser.ConfigParser()
    config.read('default.ini')
    return config['players']['player1'], config['players']['player2']

# SHOWS EXISTING SCORE
def display_scores():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # RETRIVE PLAYERS AND THEIR SCORES - SET IN ORDER BY THE HIGH SCORE
    cursor.execute("SELECT id, username, score FROM players ORDER BY score DESC")
    results = cursor.fetchall()
    
    if not results:
        print("No scores found.")
    else:
        print("\nLeaderboard:")
        print(f"{'ID':<3} | {'Username':<15} | {'Score':<5}")
        print("-" * 30)
        for row in results:
            print(f"{row[0]:<3} | {row[1]:<15} | {row[2]:<5}")
    
    action = input("\nType 'exit' to return or 'remove' to delete a score: ").strip().lower()
    if action == 'remove':
        score_id = input("Enter the ID of the player to remove: ").strip()
        cursor.execute("DELETE FROM players WHERE id = %s", (score_id,))
        conn.commit()
        print("Player score removed successfully.")
    
    conn.close()

# MAIN GAME LOGIC
def play_game(player1, player2):
    board = [' ' for _ in range(9)]

    # PRINTING OUT BOARD
    def print_board():
        print("\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)]))
        print("-" * 9)

    # HOW TO WIN - CHECKUP
    def check_winner():
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],        # ROWS
            [0, 3, 6], [1, 4, 7], [2, 5, 8],        # COLUMNS
            [0, 4, 8], [2, 4, 6]                    # DIAGONALS
        ]
        for pos in winning_positions:
            if board[pos[0]] == board[pos[1]] == board[pos[2]] != ' ':
                return board[pos[0]]
        return None

    current_player, other_player = (player1, 'X'), (player2, 'O')
    print_board()

    for _ in range(9):
        try:
            move = int(input(f"{current_player[0]}'s turn ({current_player[1]}), enter position (1-9): ")) - 1
            if move < 0 or move >= 9 or board[move] != ' ':
                print("Invalid move. Try again.")
                continue
            board[move] = current_player[1]
            print_board()
            winner = check_winner()
            if winner:
                print(f"{current_player[0]} wins!")
                record_score(current_player[0])     # ADDING WINNER SCORE
                return
            current_player, other_player = other_player, current_player

        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")
            continue

    print("It's a draw!")

# ADDING WINNER SCORE INTO DATABASE
def record_score(winner):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # CHECK UP - PLAYER EXISTANCE
    cursor.execute("SELECT score FROM players WHERE username = %s", (winner,))
    result = cursor.fetchone()
    
    if result:
        # IF PLAYER EXIST - UPDATE PLAYER, UPDATE EXISTING + 1 POINT
        cursor.execute("UPDATE players SET score = score + 1 WHERE username = %s", (winner,))
    else:
        # IF PLAYER DOESN'T EXIST - ADD PLAYER, ADD POINT 1
        cursor.execute("INSERT INTO players (username, score) VALUES (%s, 1)", (winner,))
    
    conn.commit()
    conn.close()

# MAIN MENU
def main():
    while True:
        choice = input("Choose an option: Start, Score, Exit: ").lower()
        if choice == 'start':
            # BEFORE STARTING GAME - ASK USERNAME, ELSE DEFAULT
            player1, player2 = get_default_usernames()
            player1 = input(f"Please input player 1 username (Default username \"{player1}\"): ") or player1
            player2 = input(f"Please input player 2 username (Default username \"{player2}\"): ") or player2
            play_game(player1, player2)
        elif choice == 'score':
            display_scores()
        elif choice == 'exit':
            print("Hope to se you again!")
            break
        else:
            print("ERROR, please try again.")

if __name__ == "__main__":
    main()
