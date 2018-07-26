Custom List Analyzer 1.1.1 (updated 8-19-17) by Kristopher Kyle (original program released 11-24-14)

Instructions:

To run the list analyzer you need the following:

1. A list dictionary.  List dictionaries can be created in any
spreadsheet software, but must be formatted in a particular way.  A list must be represented by one row, and the first column in the row should be the list name (this will be saved as the NAME of the list, but will not be counted as part of the list).  Finally, your spreadsheet MUST be saved as a tab-delimited text file. Note that single-word entries must be in lower case. (wildcards and n-grams can be either upper or lower, but the search is not case sensitive)

2. A folder that contains files to be analyzed.  You can only choose to analyze texts included in a particular folder (nested folders won't work).  So, if you want to analyze a group of texts, make sure they are in the same folder, then choose that folder using the input folder feature in the program.  All files must be .txt files in ASCII or UTF-8 format. 

3.  An output filename. This is the file that your results will be written to.



Enjoy!

Other important information:

1. For each target text, CLA will count the number list instances. CLA outputs a normed score, which is calculated as: Number of list instances/ Number of words in text. 

For example, if our list consisted of "a" and "an", and our target text was "This is a target sentence.", then CLA would find that list items occurred only once. There are five words in the target text, so CLA would produce a score of 0.20 (1 [number of list instances] / 5 [number of words in the text] = 0.20).

2. Your lists can include single words and/or n-grams.

3. For single words (or the first or last item in an n-gram) you can use a '*' wildcard at the end of a word, which will include the beginning of the word (everything before the '*' wildcard), and any characters that following until the end of the word boundary (a space or punctuation) AND/OR at the beginning of a word, which will include the end of the word and anything that comes before it.  

For example, if the item 'beginner' is in a list, the program will count all instances of 'beginner'.  If 'begin*' is in a list, the program will count all instances of 'begin', 'begins', 'beginner', 'beginners', 'beginning', etc. Or, if you want all words that end in -ingù, you could use a wildcard to get these (*ing).