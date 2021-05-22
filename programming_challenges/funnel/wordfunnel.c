'''
Challenge

Given two strings of letters, determine whether the second can be made from the first by removing one letter. The remaining letters must stay in the same order.
Examples

funnel("leave", "eave") => true
funnel("reset", "rest") => true
funnel("dragoon", "dragon") => true
funnel("eave", "leave") => false
funnel("sleet", "lets") => false
funnel("skiff", "ski") => false

Optional bonus 1

Given a string, find all words from the enable1 word list that can be made by removing one letter from the string. If there are two possible letters you can remove to make the same word, only count it once. Ordering of the output words doesnt matter.

bonus("dragoon") => ["dragon"]
bonus("boats") => ["oats", "bats", "bots", "boas", "boat"]
bonus("affidavit") => []

Optional bonus 2

Given an input word from enable1, the largest number of words that can be returned from bonus(word) is 5. One such input is "boats". There are 28 such inputs in total. Find them all.

Ideally you can do this without comparing every word in the list to every other word in the list. A good time is around a second. Possibly more or less, depending on your language and platform of choice - Python will be slower and C will be faster. The point is not to hit any specific run time, just to be much faster than checking every pair of words.
'''

'''
Challenge

A word funnel is a series of words formed by removing one letter at a time from a starting word, keeping the remaining letters in order. For the purpose of this challenge, a word is defined as an entry in the enable1 word list. An example of a word funnel is:

gnash => gash => ash => ah

This word funnel has length 4, because there are 4 words in it.

Given a word, determine the length of the longest word funnel that it starts. You may optionally also return the funnel itself (or any funnel tied for the longest, in the case of a tie).
Examples

funnel2("gnash") => 4
funnel2("princesses") => 9
funnel2("turntables") => 5
funnel2("implosive") => 1
funnel2("programmer") => 2

Optional bonus 1

Find the one word in the word list that starts a funnel of length 10.
Optional bonus 2

For this bonus, you are allowed to remove more than one letter in a single step of the word funnel. For instance, you may step from sideboard to sidebar by removing the o and the final d in a single step. With this modified rule, its possible to get a funnel of length 12:

preformationists =>
preformationist =>
preformations =>
reformations =>
reformation =>
formation =>
oration =>
ration =>
ratio =>
rato =>
rat =>
at

preformationists is one of six words that begin a modified funnel of length 12. Find the other five words.
'''

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define MAX 100

typedef struct TrieNode
{
	// number of times this string occurs in the corpus
	int count;

	// 26 TrieNode pointers, one for each letter of the alphabet
	struct TrieNode *children[26];

	// the co-occurrence subtrie for this string
	struct TrieNode *subtrie;
} TrieNode;

TrieNode *createTrieNode(void) {
	// create struct and check memory
	TrieNode *t = malloc(sizeof(TrieNode));
	if (t == NULL)
		return NULL;
	
	// initialize data
	t->count = 0;
	t->subtrie = malloc(sizeof(TrieNode));
	t->subtrie->count = 0;
	t->subtrie = NULL;
	
	return t;
}

// recursive function
void insertString(TrieNode *root, char *string) {
	if (string[0] == '\0') {
		root->count++;
		return;
	}
	
	// creates a child node if needed
	if (root->children[string[0] - 'a'] == NULL)
		root->children[string[0] - 'a'] = createTrieNode();
	
	insertString(root->children[string[0] - 'a'], string+1);
}

TrieNode *readFile() {
	
	FILE *ifp = fopen("dict.txt", "r");
	
	// create trie root
	TrieNode *dict = createTrieNode();
	if (dict == NULL) {
		fclose(ifp);
		return NULL;
	}
	
	char string[MAX];
	
	// scan file
	while (fscanf(ifp, "%s", string) != EOF) {
		//printf("%s\n", string);
		insertString(dict, string);
	}
	
	fclose(ifp);
	return dict;
}

// deletes one letter in string
void delete(char *ptr, char *word, int index, int len) {
	int count = 0;
	
	for (int i = 0; i < len; i++) {
		if (i == index)
			continue;
		ptr[count] = word[i];
		count++;
	}
	ptr[count] = '\0';
}

// deletes a letter in string
// compares to initial input
int funnel(char *input, char *test, char *ptr) {
	char buffer[MAX];
	int length = strlen(input);
	
	for (int i = 0; i < length; i++) {
		delete(ptr, input, i, length);
				
		if (strcmp(ptr, test) == 0)
			return 1;
	}
	
	return 0;
}

int trieSearch(TrieNode *root, char *ptr, int option) {
	int index = 0, boolean = 0;
	char buffer[MAX];
	
	// keep copy of top of Trie and original input to compare
	TrieNode *search = root;

	// loop goes through each child
	for (int i = 0; i < 26; i++) {
			
		// skips if child does not exist
		if (search == NULL) 
			continue;
			
		// checks if child matches word index letter
		if (i == ptr[index] - 97) {
			
			// if match, add character to buffer
			buffer[index] = 'a' + i;
				
			// set string end
			buffer[index+1] = '\0';
			
			// increase position of string holding word
			index++;

			// increases to children of the matching letter
			search = search->children[i];
				
			// resets count to search new children
			i = -1;
		}
			
		// checks that word matches ptr and exists in dictionary
		if (search != NULL)
			if (strcmp(buffer, ptr) == 0 && search->count > 0) {
				if (option == 1)
					printf("%s\n", ptr);
				return 1;
			}
	}
	
	return 0;
}

// takes word
// deletes one letter
// search Trie for new word
void bonus(TrieNode *root, char *input, char *ptr, int length, int option) {
	char buffer[MAX];
	int count = 0;
	
	for (int i = 0; i < length; i++) {
		if (i != 0 && input[i] == input[i - 1])
			continue;
		
		delete(ptr, input, i, length);
		
		count += trieSearch(root, ptr, option);
		
	}
	if (count == 5 && option == 2)
		printf("%s\n", input);
	
}

// loops through each word 
// calls bonus if word length is 5 or higher
void bonus2(TrieNode *root, TrieNode *top, char *buffer, char *ptr, int index) {
	if (root == NULL)
		return;
	
	if (root->count > 0) {
		int len = strlen(buffer);
		if (len >= 5) {
			bonus(top, buffer, ptr, len, 2);
		}
	}
				
	buffer[index + 1] = '\0';
	
	for (int i = 0; i < 26; i++) {
		buffer[index] = 'a' + i;
		bonus2(root->children[i], top, buffer, ptr, index+1);
	}
	
	buffer[index] = '\0';
}

int funnel2(TrieNode *root, char *input, char *ptr, int len) {
	int f_count = 1, b_count = 1, match = 0;
	char copy[MAX], final[MAX];
	strcpy(copy, input);
	strcpy(final, input);
	
	// forward loop
	while (len > 1) {
		for (int i = 0; i < len; i++) {
			delete(ptr, input, i, len);

			match = trieSearch(root, ptr, 0);
			if (match) {
				f_count++;
				strcpy(input, ptr);
				break;
			}
			
		}

		if (match)
			len = strlen(ptr);
		else
			break;
	}
	
	ptr[0] = '\0';
	len = strlen(copy);
	
	// backward loop
	while (len > 1) {
		for (int i = len-1; i > -1; i--) {
			delete(ptr, copy, i, len);
			
			match = trieSearch(root, ptr, 0);
			if (match) {
				b_count++;
				strcpy(copy, ptr);
				len = strlen(ptr);
				break;
			}
		}
		if (!match)
			break;
	}

	if (f_count > b_count)
		return f_count;
	else
		return b_count;

}


void bonus3(TrieNode *root, TrieNode *top, char *buffer, char *ptr, int index) {
	if (root == NULL)
		return;
	
	if (root->count > 0) {
		int len = strlen(buffer);
		if (len > 10) {
			// keep copy of word
			char copy[MAX];
			strcpy(copy, buffer);
			int count = funnel2(top, copy, ptr, len);
			if (count == 10)
				printf("%s => %d\n", buffer, count);
		}
	}
				
	buffer[index + 1] = '\0';
	
	for (int i = 0; i < 26; i++) {
		buffer[index] = 'a' + i;
		bonus3(root->children[i], top, buffer, ptr, index+1);
	}
	
	buffer[index] = '\0';
}

void main(int argc, char *argv[]) {
	
	// measure time for program
	clock_t t = clock();
	
	// 0 or 1 for different functions
	int option = 0;
	
	// checks if input 2 can be made from input 1
	if (argc ==  3) {
		int length = strlen(argv[1]);
		char *word = malloc(sizeof(char) * length);
		int boolean = funnel(argv[1], argv[2], word);
		
		if (boolean)
			printf("True\n");
		else
			printf("False\n");
	}
	
	else if (argc == 2) {
		// create Trie
		TrieNode *dictionary = readFile();
		int length = strlen(argv[1]);
		char *word = malloc(sizeof(char) * length);
		
		// function gets how many 
		if (option) {
			strcpy(word, argv[1]);
			printf("%s => ", word);
			int count = funnel2(dictionary, argv[1], word, length);
			printf("%d\n", count);

		}
		else
			// returns how many words can be made from input word
			bonus(dictionary, argv[1], word, length, 1);
		
		free(dictionary);
		free(word);
	}
	
	else if (argc == 1) {
		// create Trie
		TrieNode *dictionary = readFile();
		char buffer[MAX], *word = malloc(sizeof(char) * MAX);
		
		// finds word that has 10 sub words
		if (option) {
			bonus3(dictionary, dictionary, buffer, word, 0);
		}
		
		// finds all words that can make 5 sub words
		else
			bonus2(dictionary, dictionary, buffer, word, 0);
		
		free(dictionary);
		free(word);
	}
	
	t = clock() - t;
	double time = ((double)t) / CLOCKS_PER_SEC;
	printf("time = %f\n", time);
	
	
	return;
}