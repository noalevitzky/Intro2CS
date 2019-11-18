import tkinter as tk
from .game import Game as Gm
from .ai import AI
from time import sleep


class Gui:
    PLAYERS_OPTION = ['Human vs. Human', 'Human vs. PC', 'PC vs. Human',
                      'PC vs. PC']
    CHOSEN_OPTION = None
    ROWS = 6
    COLS = 7
    MSG_DICT = {'illegal move': 'Error: Illegal move. Please try again.',
                'turn': 'Player {}\'s turn',
                'winner 1': 'The winner is player 1! (red)',
                'winner 2': 'The winner is player 2! (blue)',
                'game over': 'GAME OVER',
                'tie': 'The game ended with a tie!',
                'new game': 'Would you like to play another round?'}

    def __init__(self, root):
        self.root = root
        root.title('Four In A Row')

        # create objects
        self.frame = tk.Frame(self.root, bg='lemon chiffon')
        self.title_label = tk.Label(self.frame, width=25, height=2,
                                    bg='lemon chiffon',
                                    text='Please select players:',
                                    font=('Helvetica', 20))
        hum_vs_hum_b = tk.Button(self.frame, text=self.PLAYERS_OPTION[0],
                                 font=('Helvetica', 16))
        hum_vs_pc_b = tk.Button(self.frame, text=self.PLAYERS_OPTION[1],
                                font=('Helvetica', 16))
        pc_vs_hum_b = tk.Button(self.frame, text=self.PLAYERS_OPTION[2],
                                font=('Helvetica', 16))
        pc_vs_pc_b = tk.Button(self.frame, text=self.PLAYERS_OPTION[3],
                               font=('Helvetica', 16))
        space = tk.Label(self.frame, height=3, bg='lemon chiffon')

        hum_vs_hum_b.bind('<Button-1>', lambda event: self.__set_chosen_option(
            self.PLAYERS_OPTION[0]))
        hum_vs_pc_b.bind('<Button-1>', lambda event: self.__set_chosen_option(
            self.PLAYERS_OPTION[1]))
        pc_vs_hum_b.bind('<Button-1>', lambda event: self.__set_chosen_option(
            self.PLAYERS_OPTION[2]))
        pc_vs_pc_b.bind('<Button-1>', lambda event: self.__set_chosen_option(
            self.PLAYERS_OPTION[3]))

        # set layout of menu
        self.frame.pack()
        self.title_label.pack()
        hum_vs_hum_b.pack()
        hum_vs_pc_b.pack()
        pc_vs_hum_b.pack()
        pc_vs_pc_b.pack()
        space.pack()

        # variables of main gui (will be defined later on)
        self.__init_variables()

    def __init_variables(self):
        self.game = Gm()
        self.msg_label = None
        self.board_frame = None
        self.turn_label = None
        self.new_game_label = None
        self.operating_ais = []
        self.game_on = True

    def __set_chosen_option(self, option):
        if option == self.PLAYERS_OPTION[1]:
            self.operating_ais.append(AI(self.game, 2))
        elif option == self.PLAYERS_OPTION[2]:
            self.operating_ais.append(AI(self.game, 1))
        elif option == self.PLAYERS_OPTION[3]:
            self.operating_ais.append(AI(self.game, 1))
            self.operating_ais.append(AI(self.game, 2))
        self.__start_game(option)

    def __start_game(self, option):
        """
        init params for game
        """
        self.CHOSEN_OPTION = option
        self.frame.destroy()
        self.cell_dict = {}
        self.__init_main_gui()
        self.__game_by_chosen_option()

    def __init_main_gui(self):
        """
        create all main containers
        """
        self.frame = tk.Frame(self.root, width=400, height=60,
                              bg='lemon chiffon', padx=10,
                              pady=10)
        self.turn_label = tk.Label(self.frame, text='Player 1\'s turn',
                                   bg='lemon chiffon', font=('Helvetica', 16))
        self.msg_label = tk.Label(self.frame, text='', bg='lemon chiffon',
                                  font=('Helvetica', 16))
        self.board_frame = tk.Frame(self.frame, bg='lemon chiffon', padx=10,
                                    pady=10)

        # set layout of main containers
        self.frame.pack(fill=tk.X)
        self.turn_label.pack()
        self.msg_label.pack()
        self.board_frame.pack()
        self.__init_board()

    def __init_board(self):
        """
        creates board in gui
        """
        for i in range(self.ROWS):
            for j in range(self.COLS):
                row = int(i)
                column = int(j)
                b = tk.Button(self.board_frame, height=5, width=10, bg='white',
                              state=tk.NORMAL)
                b.grid(row=row, column=column)
                self.cell_dict[b] = (row, column)

    def __game_by_chosen_option(self):
        """
        if PC starts- func calls ai turn first.
        else, activate cells in board for human
        """
        if self.CHOSEN_OPTION == self.PLAYERS_OPTION[3]:
            # PC VS PC
            # while self.game_on:
            self.__ai_turn()

        elif self.CHOSEN_OPTION == self.PLAYERS_OPTION[2]:
            # PC VS HUMAN, thus pc starts
            self.__ai_turn()
        # actives buttons in board for human
        self.__activate_cells()

    def __next_player(self):
        self.game.set_player()
        self.__update_turn_label()

    def __on_click(self, column):
        """
        human turn- a cell was chosen.
        make move with chosen column
        """
        self.__reset_error_msg()
        self.__make_move_gui(column)

    def __make_move_gui(self, column):
        """
        try to make move in game, update gui if possible,
        set next player and checks if ai turn is next.
        if move is illegal, or game is over- except error and act by it
        """
        if not self.game_on:
            return
        try:
            self.game.make_move(column)
            cell = self.game.get_cur_placement()
            self.__set_disk(cell)
            self.__next_player()
            self.__ai_turn()
        except ValueError:
            # game is over, there's a winner or board is full
            self.__set_disk(self.game.get_cur_placement())
            self.__game_over()
        except IndexError:
            self.__illegal_move()

    def __ai_turn(self, i=0):
        """
        operates the ai turns if exist, iterating over a ais list saved
        in the gui object, and call for the ai to find a legal placement if
        its the specific ai turn (if not, the ai will raise a NameError)
        """
        try:
            ai = self.operating_ais[i]
            self.__reset_error_msg()
            column = ai.find_legal_move()
            if self.CHOSEN_OPTION == self.PLAYERS_OPTION[3]:
                # PC VS PC
                sleep(.5)
                self.root.update()
            self.__make_move_gui(column)
        except TypeError:
            # the ai will raise this if there are no pos
            # moves, meaning the game is over
            self.__game_over()
        except IndexError:
            return  # the operating ai in index i dont exist
        except NameError:
            # pass if this is not this ai player turn,
            # continue to second ai player (if exists)
            self.__ai_turn(i + 1 % 2)

    def __get_cell_of_coordinate(self, coordinate):
        """
        return cell with the given coordinates
        """
        for cell, location in self.cell_dict.items():
            if location == coordinate:
                return cell

    def __reset_error_msg(self):
        self.msg_label['text'] = ''

    def __set_disk(self, coordinate):
        """
        move is legal, reset error label and add player's disk to cell
        """
        cell = self.__get_cell_of_coordinate(coordinate)
        player = self.game.get_current_player()
        if player == 1:
            self.__set_player1_move(cell)
        if player == 2:
            self.__set_player2_move(cell)

    def __illegal_move(self):
        """
        sets menu's error label to 'illegal move'
        """
        self.msg_label.config(text=self.MSG_DICT['illegal move'])

    def __set_player1_move(self, cell):
        """
        RED PLAYER
        change button color to player's 1 color, and disable it
        """
        cell.config(bg='indian red', state=tk.DISABLED)

    def __set_player2_move(self, cell):
        """
        BLUE PLAYER
        change button color to player's 2 color, and disable it
        """
        cell.config(bg='RoyalBlue3', state=tk.DISABLED)

    def __update_turn_label(self):
        player = self.game.get_current_player()
        self.turn_label['text'] = self.MSG_DICT['turn'].format(player)

    def __on_enter(self, column):
        """
        change entered column color to player's color, for unoccupied cells
        """
        column_cells_lst = self.game.get_unoccupied_cells(column)
        for coordinate in column_cells_lst:
            cell = self.__get_cell_of_coordinate(coordinate)
            if cell['state'] != tk.DISABLED:
                if self.game.get_current_player() == 1:
                    self.__player1_enter(cell)
                elif self.game.get_current_player() == 2:
                    self.__player2_enter(cell)

    def __player1_enter(self, cell):
        """
        RED PLAYER
        change cell color to player's 1 color
        """
        cell.config(bg='RosyBrown1')

    def __player2_enter(self, cell):
        """
        BLUE PLAYER
        change cell color to player's 2 color
        """
        cell.config(bg='light blue')

    def __on_leave(self, column):
        """
        reset column color for unoccupied cells
        """
        column_cells = self.game.get_unoccupied_cells(column)
        for coordinate in column_cells:
            cell = self.__get_cell_of_coordinate(coordinate)
            cell.config(bg='white')

    def __game_over(self):
        """
        set gui msg according to ending reason (tie or winner),
        and offer starting a new game to player
        """
        self.game_on = False

        # highlight winner's set and update gui
        self.__set_game_over_msg()
        self.__highlight_winner_set()
        self.__deactivate_cells()
        self.__ask_player_new_game()

    def __set_game_over_msg(self):
        self.turn_label['text'] = self.MSG_DICT['game over']
        if self.game.get_winner() == 0:
            self.msg_label['text'] = self.MSG_DICT['tie']
        else:
            winner = self.game.get_winner()
            if winner == 1:
                self.__winner1()
            elif winner == 2:
                self.__winner2()

    def __winner1(self):
        self.msg_label['text'] = self.MSG_DICT['winner 1']

    def __winner2(self):
        self.msg_label['text'] = self.MSG_DICT['winner 2']

    def __highlight_winner_set(self):
        for coordinate in self.game.get_win_set():
            cell = self.__get_cell_of_coordinate(coordinate)
            cell.config(bg='yellow')

    def __activate_cells(self):
        for cell in self.cell_dict.keys():
            cell.bind('<Enter>', lambda event: self.__on_enter(
                self.cell_dict[event.widget][1]))
            cell.bind('<Leave>', lambda event: self.__on_leave(
                self.cell_dict[event.widget][1]))
            cell.bind('<Button-1>', lambda event: self.__on_click(
                self.cell_dict[event.widget][1]))

    def __deactivate_cells(self):
        for cell in self.cell_dict.keys():
            cell.unbind('<Enter>')
            cell.unbind('<Leave>')
            cell.unbind('<Button-1>')
            if cell['state'] != tk.DISABLED:
                cell.config(bg='white')
            cell['state'] = tk.DISABLED

    def __ask_player_new_game(self):
        self.new_game_label = tk.Label(self.frame,
                                       text=self.MSG_DICT['new game'],
                                       bg='lemon chiffon',
                                       font=('Helvetica', 16))
        self.new_game_yes_b = tk.Button(self.frame, text='Yes', height=2,
                                        width=16, bg='white',
                                        font=('Helvetica', 12))
        self.new_game_no_b = tk.Button(self.frame, text='No', height=2,
                                       width=16, bg='white',
                                       font=('Helvetica', 12))

        self.new_game_yes_b.bind('<Button-1>',
                                 lambda event: self.__restart_game())
        self.new_game_no_b.bind('<Button-1>', lambda event: self.__exit_game())

        self.new_game_label.pack()
        self.new_game_yes_b.pack(side=tk.RIGHT)
        self.new_game_no_b.pack(side=tk.LEFT)

    def __restart_game(self):
        self.__init_variables()
        self.__set_chosen_option(self.CHOSEN_OPTION)

    def __exit_game(self):
        self.root.destroy()
