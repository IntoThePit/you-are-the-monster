import random #so I can do random shuffling
import itertools # For finding combinations of monster moves.
import time

deck = ["N","N","N","N","E","E","E","E","W","W","W","W","S","S","S","S", "NE","NW","SE","SW", "2N","2E","2W","2S"] #consider making this by setting variables for each class
handsize = 3
monster_hand = ["N", "N", "S", "S", "E", "E", "W", "W",] #I sorta figure this should be in the player class, but I can't figure out how to make that work.

#hand = random.sample(deck, 3) <-- An alternative idea for randomisation

random.shuffle(deck)#this shuffles the deck
random.shuffle(deck)#this shuffles the deck some more
random.shuffle(deck)#this shuffles the deck extra thoroughly

#
# This is about checking if the player is using too many of a certain move (i.e. you can't use three norths when the deck has two norths)
# 

def is_first_list_in_second_list(list1, list2):
        i = 0
        checkinglist = []
        for item in list2:
                checkinglist.append(item) #making a copy of the list so I can remove items from it while checking
        for val in list1:
                if val in checkinglist:
                        checkinglist.remove(val)
                        i += 1
                else:
                        return False
        if i == len(list1):
                return True
        else:
                return False

#
# This chooses a monster randomly.
#

def choose_monster(numberofplayers):
        numbered_list_of_players = []
        i = 1
        while i < numberofplayers + 1:
                numbered_list_of_players.append(i)
                i += 1
        random.shuffle(numbered_list_of_players)
        return numbered_list_of_players[0]

#
# This looks through the 2D array board and finds the coordinates of the first instance of a given symbol.
#

def find_object (list_array, symbol):
	rownumber = -1 #This is -1 because I want the first row to be 0 and I'm lazy.
	for row in list_array:
		rownumber += 1
		colnumber = -1
		for col in row:
			colnumber += 1
			if symbol == col:
				return [colnumber, rownumber]

#
# This says what the symbol is at certain coordinates.
#

def whats_at_these_coords(coordlist):
        col = coordlist[0]
        row = coordlist[1]
        return currentboard.board[row][col] 

class Board(object):

        def __init__(self, turn):
                self.board = [['X','X','X','X','X','X','X','X','X','X','X','X'],
                              ['X','.','.','X','.','.','.','.','.','.','.','X'],
                              ['X','.','.','.','.','.','X','.','.','p','.','X'],
                              ['X','.','.','.','.','.','X','X','X','X','.','X'],
                              ['X','.','.','.','.','.','.','.','.','.','.','X'],
                              ['X','.','.','X','.','.','H','X','X','X','.','X'],
                              ['X','.','.','X','.','.','.','.','X','.','.','X'],
                              ['X','.','.','X','.','.','.','p','.','.','.','X'],
                              ['X','.','.','X','.','H','.','.','M','.','.','X'],
                              ['X','.','.','p','.','.','.','.','.','.','.','X'],
                              ['X','.','.','.','.','.','.','.','.','.','.','X'],
                              ['X','X','X','X','X','X','X','X','X','X','X','X']] #Man I totes should've generated that.
                self.turn = turn
        
        def replace_at_coordinate(self,col,row,symbol):
                self.board[row][col] = symbol

        def move_object(self,newcol,newrow,symbol,instance_name):
                oldcol = find_object(self.board, symbol)[0]
                oldrow = find_object(self.board, symbol)[1]
                self.board[oldrow][oldcol] = instance_name.current_square
                self.replace_at_coordinate(newcol,newrow,symbol)
                # self.print_board(self.board)
                                       
        def print_board(self, board):
                for row in board:        
                        print " ".join(row)
                print "\n"

class Player(object):
        
        def __init__(self, num, name):
                self.ismonster = False #True if the player is the monster
                self.num = num #the player number
                self.name = name #the player name
                self.stored_boost_direction = 0 #this is what you've got stored up
                self.to_be_shuffled = [] #this is what to return to the deck at the end of the player's turn
                self.direction = "" #this is the card that they chose from their hand this turn
                self.final_move = [] #this is what each player settles on (including boosts)
                self.final_monster_move = []
                self.my_hand = []

        def is_this_player_the_monster(self):
                if chosen_monster == self.num:
                        self.ismonster = True
                else:
                        self.ismonster = False
                
        def drawcards(self):
                currentboard.print_board(currentboard.board)
                self.my_hand = []
                cards_drawn = 0
                while cards_drawn < handsize:
                        self.my_hand.append(deck.pop(0))
                        cards_drawn += 1
                return self.my_hand
                
        def choosecard(self, hand):
                self.is_this_player_the_monster() #this bit probably makes more sense in the monster bit, but for debugging it can go here
                print "\n", self.name, str(self.ismonster) #this will eventually be taken out of this loop and replaced with a screen clear + board draw
                print hand
                choice = raw_input("Which rover movement card do you want? ").upper() 
                while choice not in hand:
                        choice = raw_input("Try again. Which rover movement card do you want? ").upper()
                else:
                        print "So, you chose", choice
                        self.my_hand.remove(choice)
                        self.to_be_shuffled += self.my_hand
                        return choice

        def useboost(self, direction, stored_boost_direction):
                valid_choices = ["Y","N"]
                if self.stored_boost_direction == 0:
                        self.final_move = [direction]
                else:
                        print "Your chosen movement card is %s and you have a %s boost stored." % (self.direction, self.stored_boost_direction) 
                choice = raw_input("Do you want to use the boost? (y/n)(This is in addition to your movement)").upper()
                while choice not in valid_choices:
                        choice = raw_input("Try again. Press y or n. ").upper()
                else:
                        if choice == "N":
                                self.final_move = [direction]
                        else:
                                if choice == "Y" and self.direction != self.stored_boost_direction:
                                        order_choice = raw_input("Which order do you want to use your boost in? \n 1. %s and then %s \n 2. %s and then %s \n" % (self.direction, self.stored_boost_direction, self.stored_boost_direction, self.direction))
                                        valid_order_choices = ["1","2"]
                                        while order_choice not in valid_order_choices:
                                                order_choice = raw_input("Try again. Press 1 or 2. ")
                                        if order_choice == "1":
                                                print "You went for %s then %s" % (self.direction, self.stored_boost_direction)
                                                self.final_move = [self.direction, self.stored_boost_direction]
                                                print self.final_move
                                        else:
                                                print "You went for %s then %s" % (self.stored_boost_direction, self.direction)
                                                self.final_move = [self.stored_boost_direction, self.direction]
                                                print self.final_move
                                else:
                                        print "You went for %s twice!" % (self.direction)
                                        self.final_move = [self.stored_boost_direction, self.direction]
                                        print self.final_move
                                        
                                self.stored_boost_direction = 0

                print self.final_move                
                self.to_be_shuffled += self.final_move
                print self.to_be_shuffled
                        
        def storeboost(self, direction, stored_boost_direction): #something's going wrong here to do with returning cards to the shuffle pile.
                valid_choices = ["Y","N"]
                if self.stored_boost_direction == 0:
                        print "You don't have a boost stored. Storing a boost means you won't move this turn."
                else:
                        print "You have a %s boost stored. Storing another boost will overwrite this." % (self.stored_boost_direction) 

                choice = raw_input("Do you want to store %s as a boost? (y/n) " % (direction)).upper()
                while choice not in valid_choices:
                        choice = raw_input("Try again. Press y or n. ").upper()
                else:
                        if choice == "Y":
                                if self.stored_boost_direction != 0:
                                        self.to_be_shuffled.append(self.stored_boost_direction)
                                        print self.stored_boost_direction
                                        print self.to_be_shuffled
                                self.stored_boost_direction = direction
                                print self.stored_boost_direction + " has been stored. You will not move."
                        elif self.stored_boost_direction != 0:
                                self.useboost(direction, stored_boost_direction)
                        else:
                                self.final_move = [self.direction]
                                print "You will move %s" % direction
                                print self.final_move
                                self.to_be_shuffled += self.final_move

        def monstermove(self, options):
                choice = raw_input("Choose 4 from these options: \n N, N, E, E, S, S, W, W \n").upper()
                while not(len(choice) == 4 and is_first_list_in_second_list(list(choice), options) == True):
                        choice = raw_input("Choose 4 from these options: \n N, N, E, E, S, S, W, W \n").upper()
                else:
                        print "Your chosen monster move is %s" % (choice.upper())
                        self.final_monster_move = choice.upper()

class MovableThing(object):

        north = [0,-1]
        south = [0,1]
        east = [1,0]
        west = [-1,0]
        north_east = [1,-1]
        north_west = [-1,-1]
        south_east = [1,1]
        south_west = [-1,1]

        def __init__(self, symbol, starting_position):
                self.symbol = symbol
                self.starting_position = starting_position
                self.current_position = self.starting_position
                self.current_square = ""
                self.square_to_move_to = []
                self.current_direction = 0
                

# This next bit physically pains me. Find a way to make the rover inherit from this so there's no stupid code duplication.

        def move_thing(self, move, symbol):
                current_direction = 0
                if move == "N":
                        self.current_direction = self.north
                elif move == "S":
                        self.current_direction = self.south
                elif move == "E":
                        self.current_direction = self.east
                elif move == "W":
                        self.current_direction = self.west
                elif move == "NE":
                        self.current_direction = self.north_east
                        compound_direction = True
                elif move == "NW":
                        self.current_direction = self.north_west
                        compound_direction = True
                elif move == "SE":
                        self.current_direction = self.south_east
                        compound_direction = True
                elif move == "SW":
                        self.current_direction = self.south_west
                        compound_direction = True
                elif move == "2N":
                        rover_moves.insert(rover_move_index,"N")
                        rover_moves.insert(rover_move_index,"N") #I am a bad, bad man.
                        return "Move Skipped"
                elif move == "2S":
                        rover_moves.insert(rover_move_index,"S")
                        rover_moves.insert(rover_move_index,"S")
                        return "Move Skipped"
                elif move == "2E":
                        rover_moves.insert(rover_move_index,"E")
                        rover_moves.insert(rover_move_index,"E")
                        return "Move Skipped"
                elif move == "2W":
                        rover_moves.insert(rover_move_index,"W")
                        rover_moves.insert(rover_move_index,"W")
                        return "Move Skipped"

                self.current_position = find_object(currentboard.board, symbol)
                col = self.current_position[0]
                row = self.current_position[1]
                self.square_to_move_to = whats_at_these_coords([col + self.current_direction[0],row + self.current_direction[1]])
                # print "Current position is %s" % self.current_position
                # print currentboard.print_board(currentboard.board)
                # print "Position to move to is %s" % [col + self.current_direction[0],row + self.current_direction[1]]
                # print "This is the symbol at the desitnation: %s" % self.square_to_move_to              

# This next bit needs to be entirely refactored to use the MovableThing Class properly.

class Rover(MovableThing):
      
        def __init__(self):
                self.starting_position = [8,6]
                self.current_position = self.starting_position
                self.ignore_next_move = False
                self.collected_parts = 0
                self.current_square = ""

        def place_rover(self):
                currentboard.board[self.starting_position[0]][self.starting_position[1]] = "R"

        def move_rover(self, move):
                current_direction = 0
                compound_direction = False
                if self.ignore_next_move == True:
                        print "Move Skipped"
                        self.ignore_next_move = False
                        return "Move Skipped"
                elif move == "N":
                        current_direction = self.north
                elif move == "S":
                        current_direction = self.south
                elif move == "E":
                        current_direction = self.east
                elif move == "W":
                        current_direction = self.west
                elif move == "NE":
                        current_direction = self.north_east
                        compound_direction = True
                elif move == "NW":
                        current_direction = self.north_west
                        compound_direction = True
                elif move == "SE":
                        current_direction = self.south_east
                        compound_direction = True
                elif move == "SW":
                        current_direction = self.south_west
                        compound_direction = True
                elif move == "2N":
                        rover_moves.insert(rover_move_index,"N")
                        rover_moves.insert(rover_move_index,"N") #I am a bad, bad man.
                        return "Move Skipped"
                elif move == "2S":
                        rover_moves.insert(rover_move_index,"S")
                        rover_moves.insert(rover_move_index,"S")
                        return "Move Skipped"
                elif move == "2E":
                        rover_moves.insert(rover_move_index,"E")
                        rover_moves.insert(rover_move_index,"E")
                        return "Move Skipped"
                elif move == "2W":
                        rover_moves.insert(rover_move_index,"W")
                        rover_moves.insert(rover_move_index,"W")
                        return "Move Skipped"

                self.current_position = find_object(currentboard.board, "R")
                col = self.current_position[0]
                row = self.current_position[1]
                square_to_move_to = whats_at_these_coords([col + current_direction[0],row + current_direction[1]])
                print "Current position is %s" % self.current_position
                print currentboard.print_board(currentboard.board)
                print "Position to move to is %s" % [col + current_direction[0],row + current_direction[1]]
                print "This is the symbol at the desitnation: %s" % square_to_move_to
                
                if square_to_move_to == ("." or "p" or "H" or "M"):
                        print "Not an X"
                        self.current_square = "."
                        self.current_position = [self.current_position[0] + current_direction[0], self.current_position[1]+ current_direction[1]]
                        col = self.current_position[0]
                        row = self.current_position[1]
                        currentboard.move_object(col,row,"R",rover)
                        if square_to_move_to == "p":
                                self.collected_parts += 1
                                if self.collected_parts == 3:
                                        victorystate = "Players"
                        elif square_to_move_to == "H":
                                self.current_square = "H"
                                self.ignore_next_move = True
                        elif square_to_move_to == "M":
                                victorystate = "Monster"
                                
                elif square_to_move_to == "X" and compound_direction == True:
                        print "Compound move into an X!"
                        first_part = move[0]
                        second_part = move[1]
                        rover_moves.insert(rover_move_index,first_part)
                        rover_moves.insert(rover_move_index + 1,second_part)
                        compound_direction = False
                else:
                        print "An X move!"

class Monster(MovableThing):
        def __init__(self):
                self.starting_position = [8,8]
                self.current_position = self.starting_position
                self.current_square = ""
                self.symbol = "M"
                self.current_direction = 0
                self.north_count = 0
                self.south_count = 0
                self.east_count = 0
                self.west_count = 0

        def pick_monster_moves(self,monster_moves,non_monster_moves,turn):
                self.north_count = 0
                self.south_count = 0
                self.east_count = 0
                self.west_count = 0
                moves_done = 0
                if turn < 2:
                        monster_moves_to_take = 2
                        non_monster_moves_to_take = 2
                else:
                        monster_moves_to_take = 3
                        non_monster_moves_to_take = 1

                if possible_to_kill_rover(self, rover_position, monster_moves, non_monster_moves, monster_moves_to_take, non_monster_moves_to_take) != "Nope":
                        return True #this will be the moves done in the final program
                else:
                
                        while moves_done < 4:
                                count_monster_moves(non_monster_moves)
                                move_options = {"N" : self.north_count, "S" : self.south_count, "E" : self.east_count, "W" : self.west_count}
                                move_to_do = max(move_options, key=move_options.get)
                                if move_to_do in monster_moves:
                                        monster_moves.remove(move_to_do)
                                        final_monster_move.append(move_to_do)
                                        moves_done += 1

        def possible_to_kill_rover(self, rover_position, monster_moves, non_monster_moves, monster_moves_to_take, non_monster_moves_to_take):
                monster_col = self.current_position[0]
                monster_row = self.current_position[1]
                rover_col = rover_position[0]
                rover_row = rover_position[1]
                col_difference = monster_col - rover_col
                row_difference = monster_row - rover_row
                col_difference_size = abs(col_difference)
                row_difference_size = abs(row_difference)
                minimum_norths = 0
                minimum_souths = 0
                minimum_easts = 0
                minimum_wests = 0
                different_orderings = []
                
                # This is how many moves that don't get you closer to the target you can have. If the rover is 4 away, no moves can be irrelevant.
                
                if col_difference_size + row_difference_size > 4:
                        print "Too far away"
                        return "Nope"
                elif col_difference_size + row_difference_size == 1:
                        print "Only one square separating"
                        return "The required set of moves"
                else:
                        # This establishes what the bare minimum requirements are to kill the rover
                        if col_difference < 0:
                                minimum_easts = col_difference_size
                        elif col_difference > 0:
                                minimum_wests = col_difference_size
                        if row_difference > 0:
                                minimum_norths = row_difference_size
                        elif row_difference < 0:
                                minimum_souths = row_difference_size

                        print "At least %s norths needed" % minimum_norths
                        print "At least %s souths needed" % minimum_souths
                        print "At least %s easts needed" % minimum_easts
                        print "At least %s wests needed" % minimum_wests

                        # Remember that this check doesn't rule out all impossible cases: e.g. if the easts and norths available all come from the monster hand
                        if (minimum_easts > easts_available) or (minimum_wests > wests_available) or (minimum_norths > norths_available) or (minimum_souths > souths_available):
                                print minimum_easts
                                return "Nope"
                        #
                        # This next bit figures out what are valid, unique combinations of monster moves.
                        #
                        else:
                                possible_monster_combinations = list(set(itertools.combinations(monster_moves, monster_moves_to_take)))
                                non_monster_moves_string = []
                                for moves in non_monster_moves:
                                        for i in moves:
                                                non_monster_moves_string.append(i)
                                # print "This is the non_monster_moves_string: %s" % non_monster_moves_string
                                possible_non_monster_combinations = list(set(itertools.combinations(sorted(non_monster_moves_string), non_monster_moves_to_take)))
                                # Now we've got a list of tuples, we want a list of strings.
                                possible_monster_combinations_strings = []
                                possible_non_monster_combinations_strings = []
                                for i in possible_monster_combinations:
                                        possible_monster_combinations_strings.append("".join(i))
                                for i in possible_non_monster_combinations:
                                        possible_non_monster_combinations_strings.append("".join(i))

                                possible_monster_combinations_strings_sorted = []
                                for i in possible_monster_combinations_strings:
                                        possible_monster_combinations_strings_sorted.append("".join(sorted(i)))
                                possible_non_monster_combinations_strings_sorted = []
                                for i in possible_non_monster_combinations_strings:
                                        possible_non_monster_combinations_strings_sorted.append("".join(sorted(i)))
                                
                                # print possible_monster_combinations_strings_sorted
                                # print possible_non_monster_combinations_strings_sorted
                                all_possible_combinations = list(set(itertools.combinations(sorted(possible_monster_combinations_strings_sorted + possible_non_monster_combinations_strings_sorted),2)))
                                all_possible_combinations_strings = []
                                for i in all_possible_combinations:
                                        all_possible_combinations_strings.append("".join(sorted("".join(sorted(i)))))
                                        
                                all_possible_combinations_strings = list(set(all_possible_combinations_strings))

                                moves_to_check = []
                                for i in all_possible_combinations_strings:
                                        north_count = 0
                                        east_count = 0
                                        south_count = 0
                                        west_count = 0
                                        for l in i:
                                                if l == "E":
                                                        east_count +=1
                                                elif l == "N":
                                                        north_count +=1
                                                elif l == "S":
                                                        south_count +=1
                                                elif l == "W":
                                                        west_count +=1
                                                        
                                        if (north_count >= minimum_norths) and (south_count >= minimum_souths) and (east_count >= minimum_easts) and (west_count >= minimum_wests):
                                                moves_to_check.append(i)
                                                
                                # print moves_to_check
                                # print len(moves_to_check)

                                
                                for i in moves_to_check:
                                        for stuff in (list(set(itertools.permutations(i,4)))):
                                                different_orderings.append("".join(stuff))
                                        

                                # print different_orderings
                                # print len(different_orderings)

                        self.monster_simulate(different_orderings)

                # print "The horizontal distance between rover and monster is %s." % col_difference
                # print "The vertical distance is %s." % row_difference
                
                # Idea: find what combinations of things would produce the difference between the rover and monster position (discount any directions that are not in either list),
                #       then check which ones are possible combinations, then check if any of them hit walls 
                # print rover_position
                # print monster_moves
                # print non_monster_moves
                # print monster_moves_to_take
                # print non_monster_moves_to_take
                return "Nope"

        def count_monster_moves(self,list_to_count):
                for move in non_monster_moves:
                        if move == "N":
                                self.north_count +=1
                        if move == "S":
                                self.south_count +=1
                        if move == "E":
                                self.east_count +=1
                        if move == "W":
                                self.west_count +=1

        def monster_simulate(self,different_orderings): # This bit doesn't reset the thing as it should.
                stored_position = self.current_position
                # print "stored_position is %s" % stored_position
                stored_square = self.current_square
                stored_board = []
                row_number = 0
                for row in currentboard.board:
                        stored_board.append([])
                        for col in row:
                                stored_board[row_number].append(col) 
                        row_number += 1

                # print stored_board
                for set_of_moves in different_orderings:                      
                        self.move_monster(set_of_moves)
                        
                        self.current_position = stored_position
                        self.current_square = stored_square
                        currentboard.board = []
                        current_board_row_number = 0
                        for row in stored_board:
                                currentboard.board.append([])
                                for col in row:
                                        currentboard.board[current_board_row_number].append(col) 
                                current_board_row_number += 1
                        # print "Now the stored_position is %s" % stored_position
                        # print currentboard.board
                        # print "Here's the stored board:"
                        # print stored_board
                
        def move_monster(self, final_monster_move):
                for move in final_monster_move:
                        super(Monster,self).move_thing(move,self.symbol)
                        if self.square_to_move_to in [".","p","H","R"]:
                                self.current_square = "."
                                self.current_position = [self.current_position[0] + self.current_direction[0], self.current_position[1]+ self.current_direction[1]]
                                col = self.current_position[0]
                                row = self.current_position[1]
                                if self.square_to_move_to == "p":
                                        self.current_square = "p"
                                elif self.square_to_move_to == "H":
                                        self.current_square = "H"
                                elif self.square_to_move_to == "R":
                                        victorystate = "Monster"
                                        print "MONSTER WINS!"
                                currentboard.move_object(col,row,self.symbol,monster)

                
turn = 1
rover = Rover()
monster = Monster()
currentboard = Board(turn)              
number_of_players = 4
chosen_monster = choose_monster(number_of_players)
rover.place_rover()

#
# Test Area
#

##rover_position = [8,6]
##monster_moves = ["W","W","N","N",]
##non_monster_moves = [["N","N","W","W",],["N","W","N","W",],["N","N","W","W",]]
##easts_available = 4
##wests_available = 4
##norths_available = 4
##souths_available = 4
##monster_moves_to_take = 2
##non_monster_moves_to_take = 2
##monster_time_before = int(time.time())
##monster.possible_to_kill_rover(rover_position, monster_moves, non_monster_moves, monster_moves_to_take, non_monster_moves_to_take)
##monster_time_after = int(time.time())
##
##print(monster_time_after - monster_time_before)

#
# End of test Area
#

player1 = Player(1, "John")
player2 = Player(2, "Jane")
player3 = Player(3, "Jack")
player4 = Player(4, "The blood god Khorne") #eventually this should be generated from the number_of_players variable

list_of_players = [player1,player2,player3,player4]

victorystate = "None"

while victorystate == "None":
        
        monster_moves = []
        non_monster_moves = []#clears out the previous turn's non_monster_moves
        rover_moves = []
      
        cards_drawn = player1.drawcards()
        player1.direction = player1.choosecard(cards_drawn)
        player1.storeboost(player1.direction, player1.stored_boost_direction)
        player1.monstermove(monster_hand)

        cards_drawn = player2.drawcards()
        player2.direction = player2.choosecard(cards_drawn)
        player2.storeboost(player2.direction, player2.stored_boost_direction)
        player2.monstermove(monster_hand)

        cards_drawn = player3.drawcards()
        player3.direction = player3.choosecard(cards_drawn)
        player3.storeboost(player3.direction, player3.stored_boost_direction)
        player3.monstermove(monster_hand)

        cards_drawn = player4.drawcards()
        player4.direction = player4.choosecard(cards_drawn)
        player4.storeboost(player4.direction, player4.stored_boost_direction)
        player4.monstermove(monster_hand)

        for player in list_of_players:
                rover_moves += player.final_move
                if player.ismonster == True:
                        monster_moves = [player.final_monster_move]
                else:
                        non_monster_moves.append(player.final_monster_move)
                print rover_moves

        rover_move_index = 0        
        for move in rover_moves:
                rover_move_index += 1 
                rover.move_rover(move)
                
        print monster_moves
        monster.move_monster(monster_moves)

        for player in list_of_players:
                print player.to_be_shuffled
                for i in player.to_be_shuffled:
                        deck.append(i)
                player.to_be_shuffled = []

        

else:
        if victorystate == "Players":
                print "The players blast off! The monster was INSERT GUILTY PARTY"
        else:
                print "The monster devours the rover. Congratulations INSERT GUILTY PATY!"

