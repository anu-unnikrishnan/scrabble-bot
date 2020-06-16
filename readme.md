
Guide to Scrabble Bot.
--------------------------------------

This repository contains Python code for building Scrabble Bot, an AI opponent for Scrabble.

1) scrabble.py - code for the game of Scrabble. 
2) scrabble_words.txt - all the words in the Collins Scrabble dictionary. 

Each player has to make words on the Scrabble board using their seven letters. Each new addition to the board must give valid words in both the left-right and up-down directions. Every letter has associated points, and the points for each word is the sum of the points of letters in all new words. Some spaces on the board give you bonus points.

To build the AI player, we look through all possible words in the dictionary that can be made on each row and each column of the board, and play the highest-scoring word. 




