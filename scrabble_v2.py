#any player can skip their turn and choose new letters instead 
#rows indexed by letters (i.e. input A A2)

import random
import numpy as np 
from copy import copy, deepcopy 
from collections import Counter
import os
os.system("clear")

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
pretty_letters = ['🄰', '🄱', '🄲', '🄳', '🄴', '🄵', '🄶', '🄷', '🄸', '🄹', '🄺', '🄻', '🄼', '🄽', '🄾', '🄿', '🅀', '🅁', '🅂', '🅃', '🅄', '🅅', '🅆', '🅇', '🅈', '🅉']

#create set of letters (each letter occurs a specific number of times)
def create_letter_bag(letter_bag):
    letter_bag = []
    #letter_bag = ['-', '-'] #two blanks 
    for let in alphabet:
        if let == 'A' or let == 'I':
            letter_bag += ([let] * 9)
        elif let == 'B' or let == 'C' or let == 'F' or let == 'H' or let == 'M' or let == 'P' or let == 'V' or let == 'W' or let == 'Y':
            letter_bag += ([let] * 2)
        elif let == 'G':
            letter_bag += ([let] * 3)
        elif let == 'D' or let == 'L' or let == 'S' or let == 'U':
            letter_bag += ([let] * 4)
        elif let == 'N' or let == 'R' or let == 'T':
            letter_bag += ([let] * 6)
        elif let == 'O':
            letter_bag += ([let] * 8)
        elif let == 'E':
            letter_bag += ([let] * 12)
        elif let == 'J' or let == 'K' or let == 'Q' or let == 'X' or let == 'Z':
            letter_bag += ([let])
    return letter_bag

#assign points to each letter 
def assign_points_to_letters(letter_bag, point_dict):
    #point_0_letters = ['-']
    point_1_letters = ['A', 'E', 'I', 'O', 'U', 'L', 'N', 'S', 'T', 'R']
    point_2_letters = ['D', 'G']
    point_3_letters = ['B', 'C', 'M', 'P']
    point_4_letters = ['F', 'H', 'V', 'W', 'Y']
    point_5_letters = ['K']
    point_8_letters = ['J', 'X']
    point_10_letters = ['Q', 'Z']
    for let in letter_bag:
        #if let in point_0_letters: #if we're allowing blanks 
            #point_dict[let] = 0
        if let in point_1_letters:
            point_dict[let] = 1
        elif let in point_2_letters:
            point_dict[let] = 2
        elif let in point_3_letters:
            point_dict[let] = 3
        elif let in point_4_letters:
            point_dict[let] = 4
        elif let in point_5_letters:
            point_dict[let] = 5
        elif let in point_8_letters:
            point_dict[let] = 8
        elif let in point_10_letters:
            point_dict[let] = 10
    return point_dict

#each player draws letters from the bag of letters so that they each have 7 letters 
def choose_letters_from_bag(letter_bag, player_1_letters, player_2_letters):

    if len(letter_bag) < 7-len(player_1_letters): #if letter bag has less letters remaining than required to top up player 1's letters
        new_player_1_letters = letter_bag #take all the letters in the bag 
    else: #otherwise 
        new_player_1_letters = random.sample(letter_bag, 7-len(player_1_letters)) #choose up to 7 letters at random from letter bag 
    for let in new_player_1_letters: #remove player 1's new letters from bag  
        letter_bag.pop(letter_bag.index(let)) #get rid of player 1's letters from bag
    player_1_letters += new_player_1_letters

    if len(letter_bag) < 7 - len(player_2_letters):
        new_player_2_letters = letter_bag
    else:
        new_player_2_letters = random.sample(letter_bag, 7-len(player_2_letters)) #choose up to 7 letters at random from letter bag 
    for let in new_player_2_letters: #remove player 2's new letters from bag 
        letter_bag.pop(letter_bag.index(let))
    player_2_letters += new_player_2_letters

    return player_1_letters, player_2_letters, letter_bag

#print board 
def printboard(board):
    print("\n\n    1   2   3   4   5   6   7   8   9   10  11  12  13  14  15\n")
    for i in range(0, n):
        print(alphabet[i], end = "   ")
        for j in range(0, n):
            if board[i][j] == '': #empty square 
                print("\u25A0", end = "   ")
            else: #letters encoded as numbers from 1 to 26, so find index (from 0 to 25) in alphabet array 
                #print(board[i][j], end = "   ")
                print(pretty_letters[alphabet.index(board[i][j])], end = "   ")
        print("\n")

def process(ans):
    ans = ans.split(',') #make into array eg. ['A 1 2', ' B 13 4']
    ans = [x.strip(' ') for x in ans] #get rid of stray spaces eg. ['A 1 2', 'B 13 4']
    ans = [x.split(' ') for x in ans] #nested array eg. [['A', '1', '2'], ['B', '13', '4']]

    #[['A', 'H1'], ['B', 'H2']] -> [['A', ['8', '1']], ['B', ['8', '2']]]
    for let in ans:
        num_pos = [x for x in let[1]]
        num_pos[0] = str(alphabet.index(num_pos[0])+1)
        let[1] = num_pos

    #flatten each sublist
    #[['A', ['8', '1']], ['B', ['8', '2']]] -> [['A', '8', '1'], ['B', '8', '2']]
    for i in range(0, len(ans)):
        ans[i] = [item for sublist in ans[i] for item in sublist]

    #convert positions to int and change to actual array index (starting from 0 instead of 1)
    #if letter was entered in lower-case, convert it to upper case 
    #eg. [['A', 0, 1], ['B', 12, 3]]
    for i in range(0, len(ans)):
        ans[i][0] = ans[i][0].upper()
        ans[i][1] = int(ans[i][1]) - 1
        ans[i][2] = int(ans[i][2]) - 1
    return ans

#check if the position is valid (i.e. on the board)
def is_pos_valid(ans, n):
    pos_valid = 0
    for i in range(0, len(ans)):
        if ans[i][1] < 0 or ans[i][1] >= n or ans[i][2] < 0 or ans[i][2] >= n:
            pos_valid = 1 #invalid position 
            print("\nTry again! [{0}][{1}] is an invalid position.\n".format(ans[i][1]+1, ans[i][2]+1))
            break
    return pos_valid 

#check if the player has all the letters they're trying to play 
def does_player_have_letter(ans, player_letters):
    does_not_have = 0
    for i in range(0, len(ans)):
        if ans[i][0] not in player_letters:
            does_not_have = 1
            print("\nTry again! You don't have the letter {0} .\n".format(pretty_letters[alphabet.index(ans[i][0])]))
            break
    return does_not_have #returns 0 if player has letters, 1 if player does not have a letter  

#if it's player 1's first move, check that one of their letters covers the centre square 
#centre square of board is board[3][3] for 7x7 
#centre square of board is board[7][7] for 15x15
#centre square of board is board[(n-1)/2][(n-1)/2] for nxn
def is_covering_centre(ans, n, move_counter):
    if move_counter == 1: #if player 1's first move 
        covering_centre = 0
        for i in range(0, len(ans)):
            if ans[i][1] == int((n-1)/2) and ans[i][2] == int((n-1)/2):
                covering_centre = 1
        return covering_centre #returns 1 if covering and 0 if not covering 
    else: #if not player 1's first move 
        return 1 #doesn't have to cover centre 

#check if first word in game is at least 2 letters 
#we only need to check this on the first go 
#because otherwise, since the word has to connect to another word, it'll at least have 2 letters 
def is_word_long_enough(ans, move_counter):
    if move_counter == 1 and len(ans) < 2:
        print("\nTry again! You need to make at least a 2-letter word.\n")
        return 1
    return 0 

#check if squares are free 
def are_squares_free(ans, board):
    free_check = 0
    for i in range(0, len(ans)):
        if board[ans[i][1]][ans[i][2]] != '': #if one of the entered positions isn't free 
            free_check = 1
            print("\nTry again! The square [{0}][{1}] is occupied.\n".format(ans[i][1]+1, ans[i][2]+1))
            break
    return free_check

#check if new words exist in both left-right (row) and up-down directions (col)
def do_new_words_exist(testboard, scrabble_words):

    words_on_board = []

    for row in testboard:
        words_in_row = ' '.join(row)
        words_in_row = words_in_row.strip(' ') #get rid of trailing whitespace 
        words_in_row = words_in_row.split('  ') #split into separate words
        words_in_row = [word.replace(' ', '') for word in words_in_row] #get rid of spaces in each separate word
        actual_words_in_row = []
        for word in words_in_row: #don't check words that are 0 or 1 letters 
            if len(word) >= 2:
                actual_words_in_row.append(word)
        for word in actual_words_in_row: #check if that word exists 
            if word not in scrabble_words:
                #print("\nTry again! The word '{0}' doesn't exist.\n".format(word))
                return 1, words_on_board
            else:
                words_on_board.append(word) 

    for col in testboard.T:
        col = list(col)
        words_in_col = ' '.join(col)
        words_in_col = words_in_col.strip(' ') 
        words_in_col = words_in_col.split('  ')
        words_in_col = [word.replace(' ', '') for word in words_in_col]
        actual_words_in_col = []
        for word in words_in_col:
            if len(word) >= 2:
                actual_words_in_col.append(word)
        for word in actual_words_in_col:
            if word not in scrabble_words:
                #print("\nTry again! The word '{0}' doesn't exist.\n".format(word))
                return 1, words_on_board
            else:
                words_on_board.append(word) 

    return 0, words_on_board #if no non-existent words found, it's ok 

#check if letters are connected to each other/to another word on the board 
def are_letters_connected(ans, testboard):
    row_no = []
    col_no = []
    consec_valid = 0
    for i in range(0, len(ans)):
        row_no.append(ans[i][1])
        col_no.append(ans[i][2])
    if row_no[1:] == row_no[:-1]: #all letters are in the same row 
        col_no.sort()
        #if any two entered letters have a space between them on the board (and not a letter), then invalid
        #start from testboard[row_no[0]][col_no[0]] and go to testboard[row_no[0]][col_no[len(col_no)-1]] and check for spaces
        #all row_no[i] are the same here
        for i in range(col_no[0], col_no[len(col_no)-1]+1):
            if testboard[row_no[0]][i] == '':
                consec_valid = 1
                break
    elif col_no[1:] == col_no[:-1]: #all letters are in the same col 
        row_no.sort()
        #all col_no[i] are the same here
        for i in range(row_no[0], row_no[len(row_no)-1]+1):
            if testboard[i][col_no[0]] == '':
                consec_valid = 1 
                break
    else: #all letters are not in the same row or col 
        consec_valid = 1 
    return consec_valid 

#check if word connects to some other word that's already on the board 
def does_word_connect_to_others(ans, board, move_counter):
    if move_counter != 1:
        connect_check = 1
        for i in range(0, len(ans)): #check if some neighbouring square has a letter 
            if ans[i][1]+1 >= 0 and ans[i][1]+1 < n: #if there is a neighbouring square on that side 
                if board[ans[i][1]+1][ans[i][2]] != '': #if the neighbouring square has a letter 
                    connect_check = 0 #it connects to some other word! 
                    break
            if ans[i][1]-1 >= 0 and ans[i][1]-1 < n:
                if board[ans[i][1]-1][ans[i][2]] != '':
                    connect_check = 0
                    break
            if ans[i][2]+1 >= 0 and ans[i][2]+1 < n:
                if board[ans[i][1]][ans[i][2]+1] != '':
                    connect_check = 0
                    break
            if ans[i][2]-1 >= 0 and ans[i][2]-1 < n:
                if board[ans[i][1]][ans[i][2]-1] != '':
                    connect_check = 0
                    break
        return connect_check 
    else: #if first move, it doesn't have to connect to anything 
        return 0

#see which letters each player has used up after each turn and remove them
def remove_played_letters(ans, player_letters):
    played_letters = []
    for i in range(0, len(ans)):
        played_letters.append(ans[i][0])
    for let in played_letters:  
        player_letters.pop(player_letters.index(let)) 
    return player_letters 

#calculate number of points for each new word and assign to player 
def calculate_points(ans, point_dict, new_words):

    points_for_words = 0 
    for word in new_words:
        wordarr = [x for x in word]
        for let in wordarr:
            points_for_words += point_dict[let]

    #os.system("clear")
    #print("\nNice one! You get {0} points for {1}.".format(points_for_words, ', '.join(new_words)))
    return points_for_words

#play word on board 
def play_word(ans, board):
    for i in range(0, len(ans)):
        board[ans[i][1]][ans[i][2]] = ans[i][0]
    return board 

#calculate sum of points from unplayed letters
def unplayed_letter_points(player_letters):
    unplayed_sum = 0
    for let in player_letters:
        unplayed_sum += point_dict[let]
    return unplayed_sum

#figuring out who won 
def calculate_winner(player_1_points, player_2_points, player_1_letters, player_2_letters):

    #store point total at end of game (before unplayed letter addition/subtraction)
    points_before_unplayed_player_1 = player_1_points
    points_before_unplayed_player_2 = player_2_points 

    #calculate sum of unplayed letters of each player
    unplayed_sum_player_1 = unplayed_letter_points(player_1_letters)
    unplayed_sum_player_2 = unplayed_letter_points(player_2_letters)

    #subtract sum of unplayed letters from each player's points 
    player_1_points -= unplayed_sum_player_1
    player_2_points -= unplayed_sum_player_2

    #if one player has used up all their letters, add the sum of unplayed letters of the other player to their points 
    if len(player_1_letters) == 0:
        player_1_points += unplayed_sum_player_2
    if len(player_2_letters) == 0:
        player_2_points += unplayed_sum_player_1

    #to calculate the winner, see who has the most points
    #if it's a tie, see who has the most points before adding/subtracting unplayed letters 
    if player_1_points > player_2_points:
        return 1 
    elif player_2_points > player_1_points:
        return 2
    else:
        if points_before_unplayed_player_1 > points_before_unplayed_player_2:
            return 1 
        elif points_before_unplayed_player_2 > points_before_unplayed_player_1:
            return 2
        else:
            return 0 

#finding all possible words that player 2 can make on the board 
def find_best_word(testboard, player_2_letters, move_counter, previous_words_on_board):

    best_points_so_far = 0
    best_word = []

    row_number = -1
    for row in testboard:

        row_number += 1 
        
        #don't bother looking at blank rows (unless first move), because we can't play there anyway 
        not_just_blanks = 0
        for let in row:
            if let != '': #if something other than a blank space 
                not_just_blanks = 1
        if move_counter != 1 and not_just_blanks == 0: 
            continue #look at next row 
        elif move_counter == 1 and row_number != int((n-1)/2): #if it's the first move, must play in centre square 
            continue

        row_string = ''.join(row) #'FE'
        row_letters = [x for x in row_string] #['F', 'E']
        possible_letters = row_letters + player_2_letters #['F', 'E', 'A', 'R']
        possible_words = []

        for word in scrabble_words:
            wordarr = [x for x in word]
            if set(wordarr).issubset(set(possible_letters)):
                possible_words.append(word)

        for word in possible_words:

            test_word_on_board = deepcopy(testboard)

            #put in each word into row
            wordarr = [x for x in word]

            not_fit = 0
            starting_point = 0
            testrow = deepcopy(row)

            #words that start with a letter that's on the board 
            for i in range(0, len(testrow)):
                if testrow[i] == wordarr[0]: 
                    starting_point = 1
                    not_fit = 0
                    #if number of spaces left in row is less than the length of the word we're trying to fit
                    if n-i < len(wordarr):
                        break
                    copy_player_2_letters = deepcopy(player_2_letters)
                    blank_counter = 0
                    for j in range(1, len(wordarr)):
                        if testrow[i+j] == '':
                            blank_counter += 1 
                        #if there's enough blank spaces/correct letters on the board to play the word
                        if testrow[i+j] != '' and testrow[i+j] != wordarr[j]: 
                            not_fit = 1
                            break
                        elif testrow[i+j] == '' and wordarr[j] not in copy_player_2_letters:
                            not_fit = 1
                            break
                        elif j == len(wordarr)-1 and blank_counter == 0: #if there are no spaces to play letters 
                            not_fit = 1
                            break
                        elif wordarr[j] in copy_player_2_letters: #if we've used up that letter 
                            copy_player_2_letters.remove(wordarr[j])

                if starting_point == 1 and not_fit == 0: #if found a starting point and the word fits 

                    added_letters = []
                    for j in range(1, len(wordarr)):
                        if testrow[i+j] != wordarr[j]:
                            added_letters.append(wordarr[j])
                        testrow[i+j] = wordarr[j]

                    #test if that word works
                    test_word_on_board[row_number] = testrow

                    #first, check if it exists 
                    exist, words_on_board = do_new_words_exist(test_word_on_board, scrabble_words)
                    if exist == 0: #the word exists in all directions! 
                        #then, check if it's connected to a word on the board 

                        #first, create an 'ans' type list which tells us each letter and its position 
                        ans = []
                        for j in range(0, len(wordarr)):
                            each_letter = []
                            each_letter.append(wordarr[j])
                            each_letter.append(row_number) #row
                            each_letter.append(i+j) #col 
                            ans.append(each_letter)

                        if does_word_connect_to_others(ans, test_word_on_board, move_counter) == 0:

                            #calculate the points you get for that word 
                            points = 0
                            c1 = Counter(words_on_board)
                            c2 = Counter(previous_words_on_board)
                            diff = c1-c2
                            new_words = list(diff.elements())
                            points = calculate_points(ans, point_dict, new_words)
                         
                            #if this is the best word we've found so far
                            if points > best_points_so_far:
                                best_word = []
                                best_word.append([word, ans, added_letters, points])
                                best_points_so_far = points 

                    test_word_on_board = deepcopy(testboard) #reset board 
                    break

            not_fit = 0
            starting_point = 0
            testrow = deepcopy(row)
            #words that start with one of the player's letters
            for i in range(0, len(testrow)):
                if testrow[i] == '': #look for a blank space
                    starting_point = 1
                    not_fit = 0
                    if n-i < len(wordarr):
                        break 
                    copy_player_2_letters = deepcopy(player_2_letters)
                    blank_counter = 0
                    for j in range(0, len(wordarr)):
                        if testrow[i+j] != '': #we need at least one letter on the board (unless it's the first move)
                            blank_counter += 1 
                        if testrow[i+j] != '' and testrow[i+j] != wordarr[j]:
                            not_fit = 1
                            break
                        elif testrow[i+j] == '' and wordarr[j] not in copy_player_2_letters:
                            not_fit = 1
                            break
                        elif move_counter != 1 and j == len(wordarr)-1 and blank_counter == 0:
                            not_fit = 1
                            break
                        elif wordarr[j] in copy_player_2_letters:
                            copy_player_2_letters.remove(wordarr[j])

                if starting_point == 1 and not_fit == 0:

                    added_letters = []
                    for j in range(0, len(wordarr)):
                        if testrow[i+j] != wordarr[j]:
                            added_letters.append(wordarr[j])
                        testrow[i+j] = wordarr[j]

                    #test if that word works
                    test_word_on_board[row_number] = testrow

                    #first, check if it exists 
                    exist, words_on_board = do_new_words_exist(test_word_on_board, scrabble_words)
                    if exist == 0: #the word exists in all directions! 
                        #then, check if it's connected to a word on the board 

                        #first, create an 'ans' type list which tells us each letter and its position 
                        ans = []
                        for j in range(0, len(wordarr)):
                            each_letter = []
                            each_letter.append(wordarr[j])
                            each_letter.append(row_number) #row
                            each_letter.append(i+j) #col 
                            ans.append(each_letter)

                        if does_word_connect_to_others(ans, test_word_on_board, move_counter) == 0:

                            #calculate the points you get for that word 
                            points = 0
                            c1 = Counter(words_on_board)
                            c2 = Counter(previous_words_on_board)
                            diff = c1-c2
                            new_words = list(diff.elements())
                            points = calculate_points(ans, point_dict, new_words)

                            #if this is the best word we've found so far
                            if points > best_points_so_far:
                                best_word = []
                                best_word.append([word, ans, added_letters, points])
                                best_points_so_far = points 

                    test_word_on_board = deepcopy(testboard) #reset board 
                    break

    #now look at columns (which are rows of testboard.T)
    row_number = -1
    for row in testboard.T:

        row_number += 1 
        
        #don't bother looking at blank rows (unless it's the first move), because we can't play there anyway 
        not_just_blanks = 0
        for let in row:
            if let != '': #if something other than a blank space 
                not_just_blanks = 1
        if move_counter != 1 and not_just_blanks == 0: 
            continue #look at next row 
        elif move_counter == 1 and row_number != int((n-1)/2): #if it's the first move, must play in centre square 
            continue

        row_string = ''.join(row) #'FE'
        row_letters = [x for x in row_string] #['F', 'E']
        possible_letters = row_letters + player_2_letters #['F', 'E', 'A', 'R']
        possible_words = []

        for word in scrabble_words:
            wordarr = [x for x in word]
            if set(wordarr).issubset(set(possible_letters)):
                possible_words.append(word)

        for word in possible_words:

            #put in each word into row
            wordarr = [x for x in word]

            not_fit = 0
            starting_point = 0
            testrow = deepcopy(row)
            #words that start with a letter that's on the board 
            for i in range(0, len(testrow)):
                if testrow[i] == wordarr[0]: 
                    starting_point = 1
                    not_fit = 0
                    #if number of spaces left in row is less than the length of the word we're trying to fit
                    if n-i < len(wordarr):
                        break
                    copy_player_2_letters = deepcopy(player_2_letters)
                    blank_counter = 0
                    for j in range(1, len(wordarr)):
                        if testrow[i+j] == '':
                            blank_counter += 1 
                        #if there's enough blank spaces/correct letters on the board to play the word
                        if testrow[i+j] != '' and testrow[i+j] != wordarr[j]: 
                            not_fit = 1
                            break
                        elif testrow[i+j] == '' and wordarr[j] not in copy_player_2_letters:
                            not_fit = 1
                            break
                        elif j == len(wordarr)-1 and blank_counter == 0:
                            not_fit = 1
                            break
                        elif wordarr[j] in copy_player_2_letters:
                            copy_player_2_letters.remove(wordarr[j])

                if starting_point == 1 and not_fit == 0: #if found a starting point and the word fits 

                    added_letters = []
                    for j in range(1, len(wordarr)):
                        if testrow[i+j] != wordarr[j]:
                            added_letters.append(wordarr[j])
                        testrow[i+j] = wordarr[j]
                    
                    #test if that word works
                    test_word_on_board.T[row_number] = testrow

                    #first, check if it exists 
                    exist, words_on_board = do_new_words_exist(test_word_on_board.T, scrabble_words)
                    if exist == 0: #the word exists in all directions! 
                        #then, check if it's connected to a word on the board 

                        #first, create an 'ans' type list which tells us each letter and its position 
                        ans = []
                        for j in range(0, len(wordarr)):
                            each_letter = []
                            each_letter.append(wordarr[j])
                            each_letter.append(i+j) #row
                            each_letter.append(row_number) #col (because each row of testboard.T is a column)
                            ans.append(each_letter)

                        if does_word_connect_to_others(ans, test_word_on_board.T, move_counter) == 0:

                            #calculate the points you get for that word 
                            points = 0
                            c1 = Counter(words_on_board)
                            c2 = Counter(previous_words_on_board)
                            diff = c1-c2
                            new_words = list(diff.elements())
                            points = calculate_points(ans, point_dict, new_words)

                            #if this is the best word we've found so far
                            if points > best_points_so_far:
                                best_word = []
                                best_word.append([word, ans, added_letters, points])
                                best_points_so_far = points 

                    test_word_on_board = deepcopy(testboard) #reset board 
                    break

            not_fit = 0
            starting_point = 0
            testrow = deepcopy(row)
            #words that start with one of the player's letters
            for i in range(0, len(testrow)):
                if testrow[i] == '': #look for a blank space
                    starting_point = 1
                    not_fit = 0
                    if n-i < len(wordarr):
                        break
                    copy_player_2_letters = deepcopy(player_2_letters)
                    blank_counter = 0
                    for j in range(0, len(wordarr)):
                        if testrow[i+j] != '':
                            blank_counter += 1 
                        if testrow[i+j] != '' and testrow[i+j] != wordarr[j]:
                            not_fit = 1
                            break
                        elif testrow[i+j] == '' and wordarr[j] not in copy_player_2_letters:
                            not_fit = 1
                            break
                        elif move_counter != 1 and j == len(wordarr)-1 and blank_counter == 0:
                            not_fit = 1
                            break
                        elif wordarr[j] in copy_player_2_letters:
                            copy_player_2_letters.remove(wordarr[j])

                if starting_point == 1 and not_fit == 0:
                    
                    added_letters = [] #this array stores the letters player 2 must add to the board to create this word 
                    for j in range(0, len(wordarr)):
                        if testrow[i+j] != wordarr[j]:
                            added_letters.append(wordarr[j])
                        testrow[i+j] = wordarr[j]

                    #test if that word works
                    test_word_on_board.T[row_number] = testrow

                    #first, check if it exists 
                    exist, words_on_board = do_new_words_exist(test_word_on_board.T, scrabble_words)
                    if exist == 0: #the word exists in all directions! 
                        #then, check if it's connected to a word on the board 

                        #first, create an 'ans' type list which tells us each letter and its position 
                        ans = []
                        #print("added_letters =", added_letters)
                        for j in range(0, len(wordarr)):
                            each_letter = []
                            each_letter.append(wordarr[j])
                            each_letter.append(i+j) #row
                            each_letter.append(row_number) #col (because each row of testboard.T is a column)
                            ans.append(each_letter)

                        if does_word_connect_to_others(ans, test_word_on_board.T, move_counter) == 0:

                            #calculate the points you get for that word 
                            points = 0

                            c1 = Counter(words_on_board)
                            c2 = Counter(previous_words_on_board)
                            diff = c1-c2
                            new_words = list(diff.elements())
                            points = calculate_points(ans, point_dict, new_words)

                            #if this is the best word we've found so far
                            if points > best_points_so_far:
                                best_word = []
                                best_word.append([word, ans, added_letters, points])
                                best_points_so_far = points 

                    test_word_on_board = deepcopy(testboard) #reset board 
                    break

    #play the word that gets you the most points 
    if len(best_word) != 0: #if a word has been found 
        best_word = best_word[0] #it's the first element of the (nested) list 
    #print("\nYour best option is to play", best_word)
    return best_word

print("\n             🅂    🄲    🅁    🄰    🄱    🄱    🄻    🄴")

letter_bag = []
letter_bag = create_letter_bag(letter_bag)

point_dict = {}
point_dict = assign_points_to_letters(letter_bag, point_dict)

player_1_letters = []
player_2_letters = []
player_1_letters, player_2_letters, letter_bag = choose_letters_from_bag(letter_bag, player_1_letters, player_2_letters)

n = 15 #size of scrabble board 
board = np.zeros(shape = [n, n], dtype = str)
printboard(board)

player_1_points = 0
player_2_points = 0

#load all allowed scrabble words 
f = open('scrabble_words.txt', 'r+')
scrabble_words = [line.strip('\n') for line in f.readlines()]
f.close() 

move_counter = 1

words_on_board = []

#keep playing if either letter bag is not empty, OR letter bag is empty and both player 1 and player 2 have letters 
while letter_bag != [] or (letter_bag == [] and player_1_letters != [] and player_2_letters != []):

    #make new letters pretty (like scrabble tiles)
    pretty_player_1_letters = []
    pretty_player_2_letters = []
    for let in player_1_letters:
        pretty_player_1_letters.append(pretty_letters[alphabet.index(let)])
    for let in player_2_letters:
        pretty_player_2_letters.append(pretty_letters[alphabet.index(let)])
    pretty_player_1_letters = '  '.join(pretty_player_1_letters)
    pretty_player_2_letters = '  '.join(pretty_player_2_letters)

    #player 1 plays 
    previous_words_on_board = deepcopy(words_on_board)
    valid = 0
    while valid == 0:

        #player 1 enters letters to play and their positions 
        print("\nPlayer 1, your letters are  {0} .\n".format(pretty_player_1_letters))
        ans = input("Enter each letter followed by the row and column where you want to play it (eg. A H2, B D3), or Exch followed by the letters you want to exchange (eg. Exch A B) :\n")
        
        ans = ans.strip(' ')
        ans = ans.split(' ')
        if ans[0] == 'Exch':

            #if too many letters
            if len(ans)-1 > 7:
                print("\nTry again! You're trying to exchange too many letters.\n")
                continue

            #if they don't have any of those letters 
            #OR if they're trying to remove eg. 2 As when they only have 1 A 
            invalid_choice = 0
            letters_to_exchange = []
            copy_player_1_letters = deepcopy(player_1_letters) 
            for i in range(1, len(ans)):
                if ans[i] not in copy_player_1_letters:
                    invalid_choice = 1
                    print("\nTry again! You don't have the letter {0}.\n".format(ans[i]))
                    break
                else:
                    letters_to_exchange.append(ans[i])
                    copy_player_1_letters.pop(copy_player_1_letters.index(ans[i]))
            if invalid_choice == 1: 
                continue

            #get rid of the letters from player 1's letters 
            #put the letters back in the letter bag
            for let in letters_to_exchange:
                player_1_letters.pop(player_1_letters.index(let)) #just get rid of one of them 
                letter_bag += let    

            #choose that many new letters from letter bag (top up player 1's letters)
            if len(letter_bag) < 7-len(player_1_letters): #if letter bag has less letters remaining than required to top up player 1's letters
                new_player_1_letters = letter_bag #take all the letters in the bag 
            else: #otherwise 
                new_player_1_letters = random.sample(letter_bag, 7-len(player_1_letters)) #choose up to 7 letters at random from letter bag 
            for let in new_player_1_letters: #remove player 1's new letters from bag  
                letter_bag.pop(letter_bag.index(let)) #get rid of player 1's letters from bag
            player_1_letters += new_player_1_letters

            print("\nYou've got {0} new letters, Player 1!\n".format(len(letters_to_exchange)))

            break #skip the turn 

        #if we're not exchanging, process the input (we won't get to this point if we exchange because of the continue)
        ans = ' '.join(ans)
        ans = process(ans) #convert input string to nested array with correct indices eg. [['A', 0, 1], ['B', 12, 3]]

        #check if those positions are valid (i.e. on the board)
        if is_pos_valid(ans, n) == 1:
            continue

        #check if the first player in their first move has made at least a 2-letter word
        #we don't need to check this for player 2 
        if is_word_long_enough(ans, move_counter) == 1:
            continue 

        #check if those squares are free
        if are_squares_free(ans, board) == 1:
            continue
        
        #check if the player actually has those letters
        if does_player_have_letter(ans, player_1_letters) == 1:
            continue

        #if player 1's first turn, check if one of the letters is covering the centre square
        if is_covering_centre(ans, n, move_counter) == 0:
            print("\nTry again! The first word has to cover the centre square.\n")
            continue

        #if the above tests pass, then try playing the word
        testboard = deepcopy(board) #make a copy that doesn't affect the original 
        for i in range(0, len(ans)):
            testboard[ans[i][1]][ans[i][2]] = ans[i][0]

        #check if the entered indices are consecutive
        if are_letters_connected(ans, testboard) == 1: 
            print("\nTry again! You have to enter consecutive letters.\n")
            continue

        #check if the word connects to some word on the board
        #as long as it's not the first move
        if does_word_connect_to_others(ans, board, move_counter) == 1:
            print("\nTry again! Your word has to connect to another word on the board.\n")
            continue 

        #figure out the new words created in each move 
        #keep track of the words that exist on the board 
        #in every round, when a new word is created, add it to the end of the array 
        #find the difference between previous and new versions of the array 
        #check if it's a real word in both the left-right and up-down directions 
        exist, words_on_board = do_new_words_exist(testboard, scrabble_words)
        c1 = Counter(words_on_board)
        c2 = Counter(previous_words_on_board)
        diff = c1-c2
        new_words = list(diff.elements()) #new words on board 
        if exist == 1:
            print("\nTry again! You've made a word that doesn't exist.\n") #new words aren't counted 
            words_on_board = deepcopy(previous_words_on_board) #set words_on_board back to before 
            continue

        #if valid word, play there
        board = play_word(ans, board)
        valid = 1
        move_counter += 1

        #calculate number of points for that word and assign to player 1 
        points_for_words_1 = calculate_points(ans, point_dict, new_words)
        player_1_points += points_for_words_1
        print("\n\nNice one! You get {0} points for {1}.".format(points_for_words_1, ', '.join(new_words)))

        #see which letters player 1 has used up and remove them from their letters 
        player_1_letters = remove_played_letters(ans, player_1_letters)
        if len(player_1_letters) == 0: #bonus points if used all letters 
            player_1_points += 50

        printboard(board)

    #player 2 plays
    #all the same stuff here
    previous_words_on_board = deepcopy(words_on_board)
    valid = 0
    while valid == 0:

        print("Player 2, your letters are  {0} .\n".format(pretty_player_2_letters))
        print("Thinking...\n")

        #try out all possible words 

        testboard = deepcopy(board) 
        best_word = find_best_word(testboard, player_2_letters, move_counter, previous_words_on_board)

        #if computer can't make any words with those letters, choose a random number of new letters 
        if best_word == []:

            #don't exchange high-scoring letters Q, Z, J, X, K (from 5-10 points)
            good_letters = ['Q', 'Z', 'J', 'X', 'K']
            not_very_good_letters = []
            for let in player_2_letters:
                if let not in good_letters:
                    not_very_good_letters.append(let)

            #choose a random number of not_very_good_letters
            num_random_letters = random.randint(1, len(not_very_good_letters)) 
            letters_to_exchange = random.sample(player_2_letters, num_random_letters) 

            #get rid of the letters from player 2's letters 
            #put the letters back in the letter bag
            for let in letters_to_exchange:
                player_2_letters.pop(player_2_letters.index(let)) #just get rid of one of them 
                letter_bag += let  

            #take new letters from letter bag 
            if len(letter_bag) < 7-len(player_2_letters): #if letter bag has less letters remaining than required to top up player 2's letters
                new_player_2_letters = letter_bag #take all the letters in the bag 
            else: 
                new_player_2_letters = random.sample(letter_bag, 7-len(player_2_letters)) #choose up to 7 letters at random from letter bag 
            for let in new_player_2_letters: #remove player 1's new letters from bag  
                letter_bag.pop(letter_bag.index(let)) #get rid of player 1's letters from bag
            player_2_letters += new_player_2_letters

            print("\nYou've got {0} new letters, Player 2!\n".format(len(letters_to_exchange)))

            break 

        pos = best_word[1]
        added_letters = best_word[2]
        points = best_word[3]
        testboard = play_word(pos, testboard)

        #check if it's a real word in both the left-right and up-down directions 
        exist, words_on_board = do_new_words_exist(testboard, scrabble_words)
        c1 = Counter(words_on_board)
        c2 = Counter(previous_words_on_board)
        diff = c1-c2
        new_words = list(diff.elements())
        if exist == 1: #word does not exist 
            words_on_board = deepcopy(previous_words_on_board)
            continue

        board = play_word(pos, board)
        valid = 1
        move_counter += 1 
        points_for_words_2 = calculate_points(ans, point_dict, new_words)
        player_2_points += points_for_words_2
        print("\nNice one! You get {0} points for {1}.".format(points_for_words_2, ', '.join(new_words)))

        for let in added_letters:
            player_2_letters.remove(let)
        if len(player_2_letters) == 0:
            player_2_points += 50 

        printboard(board)

    #after both players have played once
    player_1_letters, player_2_letters, letter_bag = choose_letters_from_bag(letter_bag, player_1_letters, player_2_letters)

    print("\nPOINTS : Player 1 [{0} points], Player 2 [{1} points].\n".format(player_1_points, player_2_points))
    print("------------------------------------------------------------\n")

#when game ends, figure out who won 
winner = calculate_winner(player_1_points, player_2_points, player_1_letters, player_2_letters)
if winner == 1:
    print("\nPlayer 1 is the winner! Congratulations.\n")
elif winner == 2:
    print("\nPlayer 2 is the winner! Congratulations.\n")
else: #winner = 0 
    print("\nIt's a tie!\n")
















