#letter and word bonuses working!

import random
import numpy as np 
from copy import copy, deepcopy 
from collections import Counter
import time 
import os
os.system("clear")

n = 15 #size of scrabble board 
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
pretty_letters = ['🄰', '🄱', '🄲', '🄳', '🄴', '🄵', '🄶', '🄷', '🄸', '🄹', '🄺', '🄻', '🄼', '🄽', '🄾', '🄿', '🅀', '🅁', '🅂', '🅃', '🅄', '🅅', '🅆', '🅇', '🅈', '🅉']

#create set of letters (each letter occurs a specific number of times)
def create_letter_bag():
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
def printboard(board, letter_bonus, word_bonus):
    print("\n\n    1   2   3   4   5   6   7   8   9   10  11  12  13  14  15\n")
    for i in range(0, n):
        if i < 9:
            print(i+1, end = "   ")
        else:
            print(i+1, end = "  ")
        for j in range(0, n):
            if board[i][j] == '' and letter_bonus[i][j] == 1 and word_bonus[i][j] == 1: #empty square with no bonuses 
                print("\u25A0", end = "   ")
            elif board[i][j] == '' and letter_bonus[i][j] == 2: #double letter 
                print("\u25A7", end = "   ")
            elif board[i][j] == '' and letter_bonus[i][j] == 3: #triple letter
                print("\u25A8", end = "   ")
            elif board[i][j] == '' and word_bonus[i][j] == 2: #double word
                print("\u25A4", end = "   ")
            elif board[i][j] == '' and word_bonus[i][j] == 3: #triple word
                print("\u25A5", end = "   ")
            elif board[i][j] != '': #letters encoded as numbers from 1 to 26, so find index (from 0 to 25) in alphabet array 
                #print(board[i][j], end = "   ")
                print(pretty_letters[alphabet.index(board[i][j])], end = "   ")
        print("\n")

#keep track of letter bonuses
def assign_letter_bonuses(letter_bonus):
    #double letter bonuses 
    for i in range(0, 15):
        if i == 0 or i == 14:
            letter_bonus[i][3] = 2
            letter_bonus[i][11] = 2
        elif i == 2 or i == 12:
            letter_bonus[i][6] = 2
            letter_bonus[i][8] = 2
        elif i == 3 or i == 11:
            letter_bonus[i][0] = 2
            letter_bonus[i][7] = 2
            letter_bonus[i][14] = 2
        elif i == 6 or i == 8:
            letter_bonus[i][2] = 2
            letter_bonus[i][6] = 2
            letter_bonus[i][8] = 2
            letter_bonus[i][12] = 2
        elif i == 7:
            letter_bonus[i][3] = 2
            letter_bonus[i][11] = 2
    #triple letter bonuses
    for i in range(0, 15):
        if i == 1 or i == 13:
            letter_bonus[i][5] = 3
            letter_bonus[i][9] = 3
        elif i == 5 or i == 9:
            letter_bonus[i][1] = 3
            letter_bonus[i][5] = 3
            letter_bonus[i][9] = 3
            letter_bonus[i][13] = 3
    return letter_bonus 

#keep track of double/triple word bonuses
def assign_word_bonuses(word_bonus):
    #double word bonuses
    for i in range(0, 15):
        if i == 1 or i == 13:
            word_bonus[i][1] = 2
            word_bonus[i][13] = 2
        elif i == 2 or i == 12:
            word_bonus[i][2] = 2
            word_bonus[i][12] = 2 
        elif i == 3 or i == 11:
            word_bonus[i][3] = 2
            word_bonus[i][11] = 2
        elif i == 4 or i == 10:
            word_bonus[i][4] = 2
            word_bonus[i][10] = 2
        elif i == 7:
            word_bonus[i][7] = 2
    #triple word bonuses
    for i in range(0, 15):
        if i == 0 or i == 14:
            word_bonus[i][0] = 3
            word_bonus[i][7] = 3
            word_bonus[i][14] = 3
        elif i == 7:
            word_bonus[i][0] = 3
            word_bonus[i][14] = 3 
    return word_bonus 

#update letter/word bonus boards to remove used ones 
def update_bonus(ans, letter_bonus, word_bonus):
    for i in range(0, len(ans)):
        if letter_bonus[ans[i][1]][ans[i][2]] == 2:
            letter_bonus[ans[i][1]][ans[i][2]] = 1 
        elif letter_bonus[ans[i][1]][ans[i][2]] == 3:
            letter_bonus[ans[i][1]][ans[i][2]] = 1 
        if word_bonus[ans[i][1]][ans[i][2]] == 2:
            word_bonus[ans[i][1]][ans[i][2]] = 1 
        elif word_bonus[ans[i][1]][ans[i][2]] == 3:
            word_bonus[ans[i][1]][ans[i][2]] = 1 
    return letter_bonus, word_bonus 

#process user input 
def process(ans):
    ans = ans.split(',') #make into array eg. ['A 1 2', ' B 13 4']
    ans = [x.strip(' ') for x in ans] #get rid of stray spaces eg. ['A 1 2', 'B 13 4']
    ans = [x.split(' ') for x in ans] #nested array eg. [['A', '1', '2'], ['B', '13', '4']]

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
    letters_can_play = deepcopy(player_letters)
    does_not_have = 0
    for i in range(0, len(ans)):
        if ans[i][0] not in letters_can_play:
            does_not_have = 1
            print("\nTry again! You don't have the letter {0} .\n".format(pretty_letters[alphabet.index(ans[i][0])]))
            break
        else:
            letters_can_play.remove(ans[i][0])
    return does_not_have #returns 0 if player has letters, 1 if player does not have a letter  s

#if it's the first move, check that one of their letters covers the centre square 
#centre square of board is board[3][3] for 7x7 
#centre square of board is board[7][7] for 15x15
#centre square of board is board[(n-1)/2][(n-1)/2] for nxn
def is_covering_centre(ans, move_counter):
    if move_counter == 1: #if player 1's first move 
        covering_centre = 0
        for i in range(0, len(ans)):
            if ans[i][1] == int((n-1)/2) and ans[i][2] == int((n-1)/2):
                covering_centre = 1
        return covering_centre #returns 1 if covering and 0 if not covering 
    else: #if not the first move 
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
def do_new_words_exist(testboard, ans, scrabble_words):

    words_on_board = []
    new_word_letters = []

    row_number = -1
    for row in testboard:
        row_number += 1
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
                return 1, words_on_board, new_word_letters
            else:
                words_on_board.append(word) 
                wordarr = [x for x in word] #split word into list 
                silly_row = deepcopy(row)
                for i in range(0, len(silly_row)):
                    if silly_row[i] == '':
                        silly_row[i] = '.'
                joined_row = ''.join(silly_row)
                starting_index = joined_row.index(word) #where that word starts in the row
                used_ans = []
                for j in range(starting_index, starting_index+len(wordarr)):
                    for i in range(0, len(ans)):
                        if row_number == ans[i][1] and j == ans[i][2] and silly_row[j] == ans[i][0]: 
                            #word uses the letter ans[i][0]
                            used_ans.append(ans[i])
                new_word_letters.append([word, used_ans])

    col_number = -1
    for col in testboard.T:
        col_number += 1 
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
                return 1, words_on_board, new_word_letters
            else:
                words_on_board.append(word) 
                wordarr = [x for x in word] #split word into list 
                silly_col = deepcopy(col)
                for i in range(0, len(silly_col)):
                    if silly_col[i] == '':
                        silly_col[i] = '.'
                joined_col = ''.join(silly_col)
                starting_index = joined_col.index(word) #where that word starts in the row 
                used_ans = []
                for j in range(starting_index, starting_index+len(wordarr)):
                    for i in range(0, len(ans)):
                        if col_number == ans[i][2] and j == ans[i][1] and silly_col[j] == ans[i][0]: 
                            used_ans.append(ans[i])
                new_word_letters.append([word, used_ans])

    return 0, words_on_board, new_word_letters #if no non-existent words found, it's ok 

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
def calculate_points(ans, point_dict, new_words, new_word_letters):

    #if anything in ans lies on a double/triple word score, x2 or x3 the points of that word 
    #after we've done that, update the word bonus table so we get rid of that 
    #right now we're not calculating the points using ans, but we can incorporate this 

    points = 0 

    actual_new_word_letters = []
    for pair in new_word_letters:
        if pair[1] != []: #get rid of empties (words not formed in that round by letters in ans)
            actual_new_word_letters.append(pair)

    for item in actual_new_word_letters: #item = [word, letters]

        #keeps track of the points we get for each word 
        word_points = 0

        #for each word, add up each letter, with bonuses for those in letters that lie on bonus squares 
        wordarr = [x for x in item[0]]

        #first, add up all the letters in the word (including ones on the board)
        for let in wordarr:
            word_points += point_dict[let] 

        #then, check if any of the added letters are on letter bonus squares 
        for let_pos in item[1]: 
            if letter_bonus[let_pos[1]][let_pos[2]] == 2:
                word_points += point_dict[let_pos[0]] #add that letter again => double letter bonus!
            elif letter_bonus[let_pos[1]][let_pos[2]] == 3:
                word_points += 2 * point_dict[let_pos[0]] #add that letter twice more => triple letter bonus!

        #finally, check if any of the added letters are on word bonus squares
        #we need to include the points after adding letter bonuses, before we double/triple the score for word bonuses 
        for let_pos in item[1]:
            if word_bonus[let_pos[1]][let_pos[2]] == 2:
                word_points += word_points #add that word again => double word bonus!
            elif word_bonus[let_pos[1]][let_pos[2]] == 3:
                word_points += 2 * word_points #add that word twice more => triple word bonus!

        points += word_points #total points for that word including all bonuses 

    return points

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

#exchange player 1 letters (chosen by player)
def exchange_player_1_letters(ans, player_1_letters, letter_bag):

    #if too many letters
    if len(ans)-1 > 7:
        print("\nTry again! You're trying to exchange too many letters.\n")
        return 0

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
        return 0 

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

    print("\nYou've got {0} new letters!\n".format(len(letters_to_exchange)))

    return 1

#exchange player 2 letters (chosen randomly)
def exchange_player_2_letters(player_2_letters, letter_bag):
                
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

    print("\nI've got {0} new letters!\n".format(len(letters_to_exchange)))

    return 

#see if we need to check this row for possible new word-making 
def check_this_row(row, row_number, move_counter):

    #don't bother looking at blank rows (unless it's the first move), because we can't play there anyway 
    not_just_blanks = 0
    for let in row:
        if let != '': #if something other than a blank space 
            not_just_blanks = 1

    if move_counter != 1 and not_just_blanks == 0: 
        return 1 #look at next row 

    elif move_counter == 1 and row_number != int((n-1)/2): #if it's the first move, must play in centre square 
        return 1 

    return 0 

#find possible words we can make from each row's letters and player 2's letters
def find_possible_words(row, player_2_letters, scrabble_words):

    row_string = ''.join(row) #'FE'
    row_letters = [x for x in row_string] #['F', 'E']
    possible_letters = row_letters + player_2_letters #['F', 'E', 'A', 'R']
    possible_words = []

    for word in scrabble_words:
        wordarr = [x for x in word]
        if set(wordarr).issubset(set(possible_letters)):
            possible_words.append(word)

    return possible_words 

#see if we can fit word in, starting from a letter
def fit_word_in_start_letter(player_2_letters, wordarr, i, testrow, not_fit):
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
    return not_fit

#see if we can fit word in, starting from a blank space
def fit_word_in_start_blank(player_2_letters, wordarr, i, testrow, not_fit):
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
    return not_fit 

#trying out word in testrow
def play_word_in_testrow(testrow, added_letters, i, wordarr, x):
    for j in range(x, len(wordarr)):
        if testrow[i+j] != wordarr[j]:
            added_letters.append(wordarr[j])
        testrow[i+j] = wordarr[j]
    return testrow, added_letters 

#creating ans for computer
def create_ans(wordarr, i, row, row_number, looking_at_rows):
    ans = []
    for j in range(0, len(wordarr)):
        each_letter = []
        if row[i+j] == '': #if this is a letter we're adding 
            each_letter.append(wordarr[j])
            if looking_at_rows == 1: #if we're looking at rows of the board 
                each_letter.append(row_number) #rows (each row of testboard is a row)
                each_letter.append(i+j) #cols 
            else: #if we're looking at cols of the board 
                each_letter.append(i+j) #row 
                each_letter.append(row_number) #col (each row of testboard.T is a column)
            ans.append(each_letter)
    return ans 

#updating best word found so far (and associated points)
def is_word_best_option(best_points_so_far, best_word, word, ans, added_letters, previous_words_on_board, words_on_board, new_word_letters):

    #calculate the points you get for that word 
    points = 0

    c1 = Counter(words_on_board)
    c2 = Counter(previous_words_on_board)
    diff = c1-c2
    new_words = list(diff.elements())

    points = calculate_points(ans, point_dict, new_words, new_word_letters)
    if len(added_letters) == 7: #if all of player 2's letters have been used up, bonus points! 
        points += 50 

    #if this is the best word we've found so far
    if points > best_points_so_far:
        best_word = []
        best_word.append([word, ans, added_letters, points, words_on_board, new_words, new_word_letters])
        best_points_so_far = points 

    return best_points_so_far, best_word  

#finding all possible words that player 2 can make on the board 
def find_best_word(testboard, player_2_letters, move_counter, previous_words_on_board):

    best_points_so_far = 0
    best_word = []

    row_number = -1 #keeps track of which row we're on 
    for row in testboard:

        row_number += 1 
        
        #do we need to check this row?
        if check_this_row(row, row_number, move_counter) == 1:
            continue 

        #find words we can make using the letters in that row and player_2_letters 
        possible_words = find_possible_words(row, player_2_letters, scrabble_words)

        for word in possible_words:

            test_word_on_board = deepcopy(testboard)

            #put in each word into row
            wordarr = [x for x in word]

            #(1) can we make a word on a row, starting with a letter that's on the board? 

            #go through elements of row, looking for places to start our word 
            #try every possible place to see what gets the most points 
            for i in range(0, len(row)):

                not_fit = 0 
                starting_point = 0

                testrow = deepcopy(row) #we'll modify row, so make a copy that we can modify instead 

                if testrow[i] == wordarr[0]: #we've found a starting point for our word 

                    starting_point = 1
                    not_fit = 0

                    #if number of spaces left in row is less than the length of the word we're trying to fit
                    if n-i < len(wordarr):
                        break
                    
                    #check if word can fit in here, and if not return 1, else return 0 
                    not_fit = fit_word_in_start_letter(player_2_letters, wordarr, i, testrow, not_fit)

                if starting_point == 1 and not_fit == 0: #if found a starting point and the word fits 

                    #create an 'ans' type list which tells us each letter and its position 
                    ans = create_ans(wordarr, i, row, row_number, 1)

                    added_letters = [] #this array stores the letters player 2 must add to the board to create this word 
                    testrow, added_letters = play_word_in_testrow(testrow, added_letters, i, wordarr, 1)

                    #test if that word works
                    test_word_on_board[row_number] = testrow

                    #check if the word exists 
                    exist, words_on_board, new_word_letters = do_new_words_exist(test_word_on_board, ans, scrabble_words)
                    if exist == 0: #the word exists in all directions!

                        #then, check if it's connected to a word on the board 
                        #update best_word and best_points_so_far if this word is the best option (highest-scoring) so far 
                        if does_word_connect_to_others(ans, test_word_on_board, move_counter) == 0:
                            best_points_so_far, best_word = is_word_best_option(best_points_so_far, best_word, word, ans, added_letters, previous_words_on_board, words_on_board, new_word_letters)  
                    test_word_on_board = deepcopy(testboard) #reset board 

            #(2) can we make a word on a row, starting with an empty space on the board? 

            for i in range(0, len(row)):

                not_fit = 0 
                starting_point = 0

                testrow = deepcopy(row)

                if testrow[i] == '': #look for a blank space to start our word 
                    starting_point = 1
                    not_fit = 0
                    if n-i < len(wordarr):
                        break 
                    not_fit = fit_word_in_start_blank(player_2_letters, wordarr, i, testrow, not_fit)

                if starting_point == 1 and not_fit == 0: #if we've found where to start our word 

                    ans = create_ans(wordarr, i, row, row_number, 1)
                    
                    #we only need to check if it's covering centre for first move
                    #so we only need this check if we're starting from an empty space in rows/cols 
                    if is_covering_centre(ans, move_counter) == 0:
                        continue

                    added_letters = []
                    testrow, added_letters = play_word_in_testrow(testrow, added_letters, i, wordarr, 0)
                    test_word_on_board[row_number] = testrow

                    exist, words_on_board, new_word_letters = do_new_words_exist(test_word_on_board, ans, scrabble_words)
                    if exist == 0: 
                        if does_word_connect_to_others(ans, test_word_on_board, move_counter) == 0:
                            best_points_so_far, best_word = is_word_best_option(best_points_so_far, best_word, word, ans, added_letters, previous_words_on_board, words_on_board, new_word_letters)  
                    test_word_on_board = deepcopy(testboard) 

    #now look at columns (which are rows of testboard.T)
    row_number = -1 #keeps track of which column (row of testboard.T) we're on 
    for row in testboard.T:

        row_number += 1 
        if check_this_row(row, row_number, move_counter) == 1:
            continue
        possible_words = find_possible_words(row, player_2_letters, scrabble_words)

        for word in possible_words:

            test_word_on_board = deepcopy(testboard)
            wordarr = [x for x in word]

            #(3) can we make a word on a col, starting with a letter that's on the board? 

            for i in range(0, len(row)):

                not_fit = 0 
                starting_point = 0               

                testrow = deepcopy(row)

                if testrow[i] == wordarr[0]: 
                    starting_point = 1
                    not_fit = 0
                    if n-i < len(wordarr):
                        break
                    not_fit = fit_word_in_start_letter(player_2_letters, wordarr, i, testrow, not_fit) 

                if starting_point == 1 and not_fit == 0: 
                    ans = create_ans(wordarr, i, row, row_number, 0) 
                    added_letters = []
                    testrow, added_letters = play_word_in_testrow(testrow, added_letters, i, wordarr, 1)
                    test_word_on_board.T[row_number] = testrow
                    exist, words_on_board, new_word_letters = do_new_words_exist(test_word_on_board, ans, scrabble_words)
                    if exist == 0: 
                        if does_word_connect_to_others(ans, test_word_on_board.T, move_counter) == 0:
                            best_points_so_far, best_word = is_word_best_option(best_points_so_far, best_word, word, ans, added_letters, previous_words_on_board, words_on_board, new_word_letters)  
                    test_word_on_board = deepcopy(testboard) 

            #(4) can we make a word on a col, starting with an empty space on the board? 

            for i in range(0, len(row)):

                not_fit = 0 
                starting_point = 0

                testrow = deepcopy(row) 
                if testrow[i] == '':
                    starting_point = 1
                    not_fit = 0
                    if n-i < len(wordarr):
                        break
                    not_fit = fit_word_in_start_blank(player_2_letters, wordarr, i, testrow, not_fit) 

                if starting_point == 1 and not_fit == 0:
                    ans = create_ans(wordarr, i, row, row_number, 0)
                    if is_covering_centre(ans, move_counter) == 0:
                        continue 
                    added_letters = [] 
                    testrow, added_letters = play_word_in_testrow(testrow, added_letters, i, wordarr, 0)
                    test_word_on_board.T[row_number] = testrow                              
                    exist, words_on_board, new_word_letters = do_new_words_exist(test_word_on_board, ans, scrabble_words)
                    if exist == 0: 
                        if does_word_connect_to_others(ans, test_word_on_board.T, move_counter) == 0:
                            best_points_so_far, best_word = is_word_best_option(best_points_so_far, best_word, word, ans, added_letters, previous_words_on_board, words_on_board, new_word_letters)                  
                    test_word_on_board = deepcopy(testboard) 

    #play the word that gets you the most points 
    if len(best_word) != 0: #if a word has been found 
        best_word = best_word[0] #it's the first element of the (nested) list 
    #print("\nYour best option is to play", best_word)
    return best_word

print("\nWelcome to 🅂  🄲  🅁  🄰  🄱  🄱  🄻  🄴 !\n")
time.sleep(0.75)
print("You'll be playing against me, a super clever computer.\n")
time.sleep(1.5)
print("My brain contains only two things:")
print("1. the entire dictionary of Scrabble words\n2. sassy comebacks.")
time.sleep(2)
play = input("\nAre you sure you want to challenge me? (y/n) ")
if play == 'n':
    print("\nYeah, that's probably a smart decision. I wouldn't want to hurt your pride!\n")
    exit()
else:
    os.system("clear")
    print("\nAll right, let's do this!")
    time.sleep(0.5)
    print("\nThis is the board.")
    print("\u25A0 blank space, \u25A7 double letter bonus, \u25A8 triple letter bonus, \u25A4 double word bonus, \u25A5 triple word bonus.")

    letter_bag = create_letter_bag()

    point_dict = {}
    point_dict = assign_points_to_letters(letter_bag, point_dict)

    player_1_letters = []
    player_2_letters = []
    player_1_letters, player_2_letters, letter_bag = choose_letters_from_bag(letter_bag, player_1_letters, player_2_letters)

    letter_bonus = np.ones(shape = [n, n]) #board that keeps track of double/triple letter bonuses 
    letter_bonus = assign_letter_bonuses(letter_bonus)

    word_bonus = np.ones(shape = [n, n]) #board that keeps track of double/triple word bonuses 
    word_bonus = assign_word_bonuses(word_bonus)

    board = np.zeros(shape = [n, n], dtype = str)
    printboard(board, letter_bonus, word_bonus)
    time.sleep(1)

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
        time.sleep(1)
        previous_words_on_board = deepcopy(words_on_board)
        valid = 0
        while valid == 0:

            #player 1 enters letters to play and their positions 
            print("\nYour letters are  {0} .\n".format(pretty_player_1_letters))
            ans = input("Enter each letter followed by the row and column where you want to play it (eg. A 1 2, B 13 4), or Exch followed by the letters you want to exchange (eg. Exch A B) :\n")
            
            ans = ans.strip(' ')
            ans = ans.split(' ')

            if ans[0] == 'Exch':
                #if successfully exchanged letters 
                if exchange_player_1_letters(ans, player_1_letters, letter_bag) == 1:
                    break #skip the turn 
                else:
                    continue #try again 

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
            if is_covering_centre(ans, move_counter) == 0:
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
            exist, words_on_board, new_word_letters = do_new_words_exist(testboard, ans, scrabble_words)
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
            points = calculate_points(ans, point_dict, new_words, new_word_letters)
            if len(player_1_letters) == 0: #bonus points if used all letters 
                points += 50
            player_1_points += points

            os.system("clear")
            if points <= 5:
                print("\n\nHmmmm, you're not very good at this, are you? You only get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points <= 15:
                print("\n\nEh, that's a pretty average move. You get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points <= 30:
                print("\n\nOkay, I've got to admit, that's a pretty good move. You get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points < 50:
                print("\n\nUgh, you're actually really good at this. You get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points >= 50:
                print("\n\nWOW! You're not supposed to be this good, you're a human! You get a whopping {0} points for {1}.".format(points, ', '.join(new_words)))

            #get rid of used letter/word bonuses
            letter_bonus, word_bonus = update_bonus(ans, letter_bonus, word_bonus) 

            #see which letters player 1 has used up and remove them from their letters 
            player_1_letters = remove_played_letters(ans, player_1_letters)
            
            printboard(board, letter_bonus, word_bonus)

        #player 2 plays
        #all the same stuff here
        previous_words_on_board = deepcopy(words_on_board)
        valid = 0
        while valid == 0:

            #print("Player 2, your letters are  {0} .\n".format(pretty_player_2_letters))
            print("\nIt's my turn! Let me think...")

            #try out all possible words 

            testboard = deepcopy(board) 
            best_word = find_best_word(testboard, player_2_letters, move_counter, previous_words_on_board)

            #if computer can't make any words with those letters, choose a random number of new letters 
            if best_word == []:
                exchange_player_2_letters(player_2_letters, letter_bag)
                break 

            ans = best_word[1]
            added_letters = best_word[2]
            points = best_word[3]
            words_on_board = best_word[4]
            new_words = best_word[5]
            new_word_letters = best_word[6]
            testboard = play_word(ans, testboard)

            board = play_word(ans, board)
            valid = 1
            move_counter += 1 
            player_2_points += points

            os.system("clear")
            if points <= 5:
                print("\n\nWell, this is embarrassing. I only get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points <= 15:
                print("\n\nOops, I couldn't find anything better. Don't judge me. I get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points <= 30:
                print("\n\nHmmmm, I'm moderately proud of myself. I get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points < 50:
                print("\n\nDon't you wish you were as clever as me? I get {0} points for {1}.".format(points, ', '.join(new_words)))
            elif points >= 50:
                print("\n\nWOW! Have you ever met a smarter AI than I? I get a whopping {0} points for {1}.".format(points, ', '.join(new_words)))

            letter_bonus, word_bonus = update_bonus(ans, letter_bonus, word_bonus) 

            for let in added_letters:
                player_2_letters.remove(let)

            printboard(board, letter_bonus, word_bonus)

        #after both players have played once
        player_1_letters, player_2_letters, letter_bag = choose_letters_from_bag(letter_bag, player_1_letters, player_2_letters)

        print("\nPOINTS : You [{0} points], Me [{1} points].\n".format(player_1_points, player_2_points))
        print("------------------------------------------------------------\n")

    #when game ends, figure out who won 
    winner = calculate_winner(player_1_points, player_2_points, player_1_letters, player_2_letters)
    if winner == 1:
        print("\nWHAT! You're the winner? Congratulations, I guess.\n")
    elif winner == 2:
        print("\nI'm the winner! What a surprise. Congratulations to me!\n")
    else: #winner = 0 
        print("\nIt's a tie?!?!\n")