import pickle
import ast
from chat_utils import *

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        """
        ["1st_line", "2nd_line", "3rd_line", ...]
        Example:
        "How are you?\nI am fine.\n" will be stored as
        ["How are you?", "I am fine." ]
        """
        # you can always write some egs for yourself here 

        self.index = {}
        """
        {word1: [line_number_of_1st_occurrence,
                 line_number_of_2nd_occurrence,
                 ...]
         word2: [line_number_of_1st_occurrence,
                  line_number_of_2nd_occurrence,
                  ...]
         ...
        }
        """

        self.total_msgs = 0
        self.total_words = 0

    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    def add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.msgs.append(m)
        self.total_msgs += 1
        # ---- end of your code --- #
        return
    
    def poem_add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        current_message = m.strip()
        self.msgs.append(current_message)
        self.total_msgs += 1
        # ---- end of your code --- #
        return

    def poem_add_msg_and_index(self, m):
        self.poem_add_msg(m)
        line_at = self.total_msgs - 1
        self.poem_indexing(m, line_at)

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    def poem_indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        words = m.split() #be careful when you should write self
        for word in words:
            lst=self.index.get(word,[])
            lst.append(l)
            self.index[word]=lst
        self.total_words += len(words)
        # ---- end of your code --- #
        return
    
    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        words = parse_list(m)
        for word in words:
            # original version
            # if word in self.index.keys():
            #     self.index[word].append(l)
            # else:
            #    self.index[word] = [l]
            word = str(word)
            lst=self.index.get(word,[])
            lst.append(l)
            self.index[word]=lst
        self.total_words += len(words)
        # ---- end of your code --- #
        return
    # implement: query interface

    def search(self, term):
        """
        return a list of tupple.
        Example:
        if index the first sonnet (p1.txt),
        then search('thy') will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
        """
        msgs = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        
        # for msg in self.msgs:
        #     if term in msg:    
        #         msgs.append((l,msg)) #Remember to go back to the requirments
        #     else:
        #         continue
        # if len(msgs) == 0:
        #     return "The word doesn't exist"
        
        # More efficient
        #It's a hashing table
        for line in self.index.get(term, []):
            tuple = (line, self.msgs[line])
            msgs.append(tuple)
        # ---- end of your code --- #
        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('/Users/a1163139531/Documents/GitHub/Great_Chat_System_6/roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()

    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        with open("/Users/a1163139531/Documents/GitHub/Great_Chat_System_6/AllSonnets.txt", "r") as poems:
            for line in poems:
                self.poem_add_msg_and_index(line)
        # ---- end of your code --- #
        return

    def get_poem(self, p):
        """
        p is an integer, get_poem(1) returns a list,
        each item is one line of the 1st sonnet

        Example:
        get_poem(1) should return:
        ['I.', '', 'From fairest creatures we desire increase,',
         " That thereby beauty's rose might never die,",
         ' But as the riper should by time decease,',
         ' His tender heir might bear his memory:',
         ' But thou contracted to thine own bright eyes,',
         " Feed'st thy light's flame with self-substantial fuel,",
         ' Making a famine where abundance lies,',
         ' Thy self thy foe, to thy sweet self too cruel:',
         " Thou that art now the world's fresh ornament,",
         ' And only herald to the gaudy spring,',
         ' Within thine own bud buriest thy content,',
         " And, tender churl, mak'st waste in niggarding:",
         ' Pity the world, or else this glutton be,',
         " To eat the world's due, by the grave and thee.",
         '', '', '']
        """
        poem = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        end = self.get_msg_size() # Don't forget the parenthesis when using one method
        start_p = self.int2roman[p] + '.'
        next_p = self.int2roman[p+1] + '.'
        temp = self.search(start_p)
        if temp:
            [(line, m)] = temp
        cur_line_num = line
        # while cur_line_num < end:
        #     poem.append(self.msgs(cur_line_num))
        #     cur_line_num += 1
        #     if self.msg(cur_line_num) == next_p:
        #         break
        # Other more efficient way
        # What I learn from it? Use something to store these things temporarily
        while cur_line_num < end:
            temp_line = self.get_msg(cur_line_num)
            if temp_line == next_p:
                break
            poem.append(temp_line)
            cur_line_num += 1
        # ---- end of your code --- #
        return poem


if __name__ == "__main__":
    sonnets = PIndex("/Users/a1163139531/Documents/GitHub/Great_Chat_System_6/AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
