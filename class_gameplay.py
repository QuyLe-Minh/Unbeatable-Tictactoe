import copy
from itertools import combinations
from tkinter import *

class TicTacToe:
    winning_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    buttons = []

    def __init__(self):
        self.moves = [StringVar() for _ in range(9)]
        self.o_wins = 0
        self.x_wins = 0
        self.index = 0
        self.player = "X"
        self.board = [" "] * 9
        self.gameOver = False
        self.winning = []
        self.mapping(lambda s:s.set(" "), self.moves)
    
    def mapping(self, func, lists):
        for l in lists:
            func(l)

    #reflect on GUI
    def updateBoard(self):
        for i in range(9):
            self.moves[i].set(self.board[i])
    
    #check if match any combination
    def isWin(self, board):
        for c in self.winning_combinations:
            if board[c[0]] == board[c[1]] and board[c[1]] == board[c[2]] and board[c[0]] != " ":
                self.winning = c
                return board[c[0]]
        return None

    def gamePlay(self, move):
        self.index +=1
        if self.player == "X":
            self.board[move] = "X"
            info_text.set("O's turn")
            self.player = "O"
            if self.index < 9:
                self.ai()
        else:
            self.board[move] = "O"
            info_text.set("X's turn")
            self.player = "X"

        self.buttons[move].config(state= "disabled")
        
        if self.gameOver:
            return

        winner = self.isWin(self.board)
        if winner:
            if winner == "X":
                info_text.set("Congratulations !!!")
                self.x_wins +=1
            else:
                info_text.set("Gameover. Try again!!!")
                self.o_wins +=1

            self.gameOver = True
            for b in self.buttons:
                b.config(state = "disabled")
            self.mapping(lambda x: x.config(disabledforeground = "red"), [self.buttons[s] for s in self.winning])

        elif self.index >= 9:
            info_text.set("Draw")
            self.mapping(lambda x: x.config(disabledforeground = "red"), self.buttons)
            self.gameOver = True

        self.updateBoard()

    def reset(self):
        self.player = "X"
        self.index = 0
        self.gameOver = False

        info_text.set("X's turn")

        self.board = [" " for _ in self.board]
        self.updateBoard()

        for b in self.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")

    def get_enemy(self, player):
        if player == "X":
            return "O"
        return "X"

    def isLeft(self, gameboard):
        for i in range(9):
            if gameboard[i] == " ":
                return True
        return False

    # def evaluate(self, board):
    #     for c in self.winning_combinations:
    #         if board[c[0]] == board[c[1]] and board[c[1]] == board[c[2]] and board[c[0]] != " ":
    #             if board[c[0]] == "X":
    #                 return -100
    #             return 100
    #     return 0

    # def minimax(self, gameboard, isMax, player):
    #     board = copy.deepcopy(gameboard)
    #     score = self.evaluate(board)
    #     if score == 100 or score == -100:
    #         return score
    #     if not self.isLeft(board):
    #         return 0
        
    #     if isMax:
    #         best = -1000
    #         for i in range(9):
    #             if board[i] == " ":
    #                 board[i] = "O"
    #                 best = max(best, self.minimax(board, not isMax, self.get_enemy(player)))
    #                 board[i] = " "
    #     else:
    #         best = 1000
    #         for i in range(9):
    #             if board[i] == " ":
    #                 board[i] = "X"
    #                 best = min(best, self.minimax(board, not isMax, self.get_enemy(player)))
    #                 board[i] = " "
        
    #     return best

    # def ai(self, board):
    #     player = "O"
    #     bestMove = -1
    #     bestVal = -1000
    #     for i in range(9):
    #         if board[i] == " ":
    #             board[i] = "O"
    #             move = self.minimax(board, True, player)
    #             board[i] = " "

    #             if move > bestVal:
    #                 bestVal = move
    #                 bestMove = i

        
    #     self.gamePlay(bestMove)
    def ai(self):
        a = -2000
        b = 2000

        board_copy = copy.deepcopy(self.board)

        best_outcome = -200

        best_move = None

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, a, b)
                board_copy[i] = " "
                if val > best_outcome:
                    best_outcome = val
                    best_move = i

        self.gamePlay(best_move)

    # The minimax algorithm, with alpha-beta pruning
    def minimax(self, player, board, alpha, beta):
        board_copy = copy.deepcopy(board)

        # Check for a win
        winner = self.isWin(board_copy)

        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif not self.isLeft(board_copy):
            return 0

        best_outcome = -200 if player == "O" else 200

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, alpha, beta)
                board_copy[i] = " "
                if player == "O":
                    best_outcome = max(best_outcome, val)
                    alpha = min(alpha, best_outcome)
                else:
                    best_outcome = min(best_outcome, val)
                    beta = max(beta, best_outcome)

                if beta <= alpha:
                    return best_outcome

        return best_outcome


root = Tk()
root.title("Unbeatable Quy's Tictactoe")

game = TicTacToe()

welcome_text = StringVar()
welcome_text.set( "Welcome to Quy's Unbeatable Tictactoe")
welcome = Label(root, textvariable=welcome_text).grid(row = 0, column=0, columnspan=3)

count_text = StringVar()
count_text.set("X: " + str(game.x_wins) + "\tO: " + str(game.o_wins))
count = Label(root, textvariable=count_text)
count.grid(row=1, column=0, columnspan=3)

info_text = StringVar()
info_text.set("It is X's turn")
info = Label(root, textvariable=info_text, font= ("Heltica", 15)).grid(row=2, column=0, columnspan=3)

restart = StringVar()
restart.set("Restart")
restartButton = Button(root, textvariable=restart, command = game.reset).grid(row = 1, column=0)

for square in range(9):
    tmp = Button(root, textvariable = game.moves[square], font= ("Helvatica", 30), command = lambda s=square: game.gamePlay(s))
    tmp.grid(row=(square // 3) + 3, column=(square % 3), sticky=NSEW)
    game.buttons.append(tmp)

root.columnconfigure(0, minsize=200)
root.columnconfigure(1, minsize=200)
root.columnconfigure(2, minsize=200)
root.rowconfigure(3, minsize=200)
root.rowconfigure(4, minsize=200)
root.rowconfigure(5, minsize=200)


root.mainloop()
