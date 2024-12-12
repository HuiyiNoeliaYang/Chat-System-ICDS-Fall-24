S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================

S_ALONE = 0
S_TALKING = 1

class Group:

    def __init__(self):
        self.members = {}
        """
        {Noelia: S_TALKING, Paul: S_Alone, ...}
        """
        self.chat_grps = {}
        """
        {0: [Noelia, Katy], 1: [Paul, Henry]}
        """
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        # ---- start your code ---- #
        return name in self.members #it can be so easily
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system, and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        name_in_group, group_key = self.find_group(name)
        if name_in_group:
            self.members.pop(name, None) #you should practice more dic & list method
            temp = self.chat_grps[group_key]
            temp.remove (name)
            self.chat_grps[group_key] = temp #Is there a better name for temp?





        # if self.is_member(name): #Use self when you want to use an class-affliated function
        #     self.members.pop(name, None) #you should practice more dic & list method
        #     for group_num in self.chat_grps.keys(): #can I simplify it?
        #         if name in self.chat_grps[group_num]:
        #             temp = self.chat_grps[group_num] #Is there a better name for temp?
        #             temp.remove (name)
        #             self.chat_grps[group_num] = temp
        #             # maybe I should add disconnect here
        # else:
            #!!!! Wait a bit how to remove it from the list
        # ---- end of your code --- #
        return

    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """

        found = False # I should learn from it, to a status machine
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        for group_idx in self.chat_grps.keys():
            #remember how to use get?
            if name in self.chat_grps[group_idx]:
                found = True
                group_key = group_idx 
                break
        # ---- end of your code --- #
        return found, group_key

    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)
        # IMPLEMENTATION
        # ---- start your code ---- #
        if not peer_in_group:
            self.grp_ever += 1
            current_grp = []
            current_grp = [peer, me]
            #Is it possible to combine the above 2 lines
            self.chat_grps[self.grp_ever] = current_grp
            self.members[me] = 1
            self.members[peer] = 1
        else: 
            peers_group = self.chat_grps[group_key]
            peers_group.append(me)
            self.grp_ever += 1
            self.chat_grps[self.grp_ever] = peers_group
            self.members[me] = 1
        # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        #check first if you are in a gc
        #put the number back to idle or 0
        #check if you are the only one in the gc, if yes, delete the gc, and assigning idle to the remaining person
    
        me_in_group, group_key = self.find_group(me)
        if me_in_group:
            self.chat_grps[group_key].remove(me)
            self.members[me] = 0
            if len(self.chat_grps[group_key]) == 1:
                remaining_peer = self.chat_grps[group_key][0]
                self.members[remaining_peer] = 0
                self.chat_grps.pop(group_key)
                
        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        return a list, "me" followed by other peers in my group
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        my_list.append(me)
        
        me_in_grp, grp_key = self.find_group(me) # you need a parenthesis to call a function
        for name in self.chat_grps[grp_key]:
            if name == me:
                continue
            my_list.append(name)
        # ---- end of your code --- #
        return my_list


if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    print(g.list_all())

    g.connect('a', 'b')
    print(g.list_all())
    g.connect('c', 'a')
    print(g.list_all())
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')
    print(g.list_all())
