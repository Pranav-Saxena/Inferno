'''
Games
'''

import random
import discord 
from discord.ext import commands 
import time
import asyncio
from datetime import datetime

def is_it_me(ctx):
  return ctx.author.id == 704174691757064304

#-----------TicTacToe - buttons---------------------
async def checkplayerticbutton(mem2, ctx, client):
    while True:
        def check(m):
            return m.author == mem2 and m.channel.id == ctx.channel.id

        try:
            message = await client.wait_for('message', timeout=60, check=check)
        except Exception as e:
            return "timeout"

        if message.content.lower() in ["y", "yes"]:
            return "yes"
        elif message.content.lower() in ["n", "no"]:
            return "no"
        else:
            return "retry"

class TicTacToeExit(discord.ui.Button['TicTacToe']):
    def __init__(self,style : discord.ButtonStyle, label : str,row :int ,custom_id :str,ctx,mem2):
        super().__init__(style = style,label = label,row=row,custom_id=custom_id)
        self.style = style
        self.label = label
        self.row = row
        self.custom_id=custom_id
        self.ctx = ctx
        self.mem2 = mem2
        self.player_choice= {'X': ctx.author, 'O': mem2}
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if interaction.user not in [self.mem2,self.ctx.author]:
            await interaction.response.send_message(content = "Only the users who started the game can play",ephemeral = True)
            return
        if self.player_choice["X"]==interaction.user:
            await interaction.response.edit_message(content=f"{self.player_choice['X'].mention} Forfeited.\n Hence, {self.player_choice['O'].mention} has Won!! ", view=view)
            view.stop()
        else:
            await interaction.response.edit_message(content=f"{self.player_choice['O'].mention} Forfeited.\n Hence, {self.player_choice['X'].mention} has Won!! ",view=view)
            view.stop()

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int,ctx,mem2):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.ctx = ctx
        self.mem2 = mem2
        self.player_choice= {'X': ctx.author, 'O': mem2}

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if interaction.user not in [self.mem2,self.ctx.author]:
            await interaction.response.send_message(content = "Only the users who started the game can play",ephemeral = True)
            return
        if interaction.user != self.player_choice[view.cur_player]:
            await interaction.response.send_message(content = f"It's {self.player_choice[view.cur_player].name}'s turn",ephemeral = True)
            return
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            view.cur_player = "O"
            content = f"It is now {self.player_choice[view.cur_player].mention}'s turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            view.cur_player = "X"
            content = f"It is now {self.player_choice[view.cur_player].mention}'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"{self.ctx.author.mention} Won!!"
            elif winner == view.O:
                content = f"{self.mem2.mention} Won!! "
            else:
                content = "It's a Tie!"

            for child in view.children:
                assert isinstance(child, discord.ui.Button) # just to shut up the linter
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self,ctx,mem2:discord.Member):
        self.ctx = ctx
        self.mem2 = mem2
        super().__init__()
        self.current_player = self.X
        self.counter = 1
        self.cur_player = "X"
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y,self.ctx,self.mem2))

        self.add_item(TicTacToeExit(discord.ButtonStyle.danger,"EXIT",4,"exit",self.ctx,self.mem2))


    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


#-----------TICTACTOE---------
async def print_tic_tac_toe(values,msg):
    embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"```\t     |     |\n\t  {values[0]}  |  {values[1]}  |  {values[2]}\n\t_____|_____|_____ \n\t     |     |\n\t  {values[3]}  |  {values[4]}  |  {values[5]}\n\t_____|_____|_____ \n\t     |     |\n\t  {values[6]}  |  {values[7]}  |  {values[8]}\n\t     |     |```",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embednew.set_footer(text="Game in Progress!!")
    await msg.edit(embed=embednew)

    # print(f"\t     |     |\n\t  {values[0]}  |  {values[1]}  |  {values[3]}\n\t_____|_____|_____ \n\t     |     |\n\t  {values[3]}  |  {values[4]}  |  {values[5]}\n\t_____|_____|_____ \n\t     |     |\n\t  {values[6]}  |  {values[7]}  |  {values[8]}\n\t     |     |")
    return embednew

def check_win(player_pos, cur_player):
    # All possible winning combinations
    soln = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

    # Loop to check if any winning combination is satisfied
    for x in soln:
        if all(y in player_pos[cur_player] for y in x):
            # Return True if any winning combination satisfies
            return True
    # Return False if no combination is satisfied
    return False


# Function to check if the game is drawn
def check_draw(player_pos):
    if len(player_pos['X']) + len(player_pos['O']) == 9:
        return True
    return False
async def checkplayer2(mem2,ctx,client):
  while True:
    def check(m):
      return m.author == mem2 and m.channel.id == ctx.channel.id 
    try:
      message = await client.wait_for('message',timeout=60,check=check)
    except Exception as e :
      return "timeout"

    if message.content.lower() in ["y","yes"]:
      # try:
      #   await message.delete()
      # except Exception as e:
      #   pass
      return "yes"
    elif message.content.lower() in ["n","no"]:
      # try:
      #   await message.delete()
      # except Exception as e:
      #   pass
      return "no"
    else:
      # try:
      #   await message.delete()
      # except Exception as e:
      #   pass

      return "retry"

async def getx(mem1,client,ctx):

  def check(m):
    return m.author == ctx.author and m.channel.id == ctx.channel.id
  try:
      message = await client.wait_for('message',timeout=120,check=check)

  except Exception as e :
      
      return "timeout"
  
  if message.content in ["x","X"]:
    # try:
    #   await message.delete()
    # except:
    #   pass
    return "X"
  elif str(message.content) in ["o","O","0"]:
    # try:
    #   await message.delete()
    # except:
    #   pass
    return "O"
  else:
    # try:
    #   await message.delete()
    # except:
    #   pass
    return "retry"


async def getmove(cur_player,ctx,client,values,player_choice,l):
  
  def check(m):
        return m.author == player_choice[cur_player] and m.channel.id == ctx.channel.id 
  try:
      message = await client.wait_for('message',timeout=150,check=check)

  except Exception as e :
      
      return "timeout"
  # l.append(message)
  
  # if len(l)==4:
  #   try:
  #     await message.channel.delete_messages(l)
  #   except:
  #     pass
  #   del l[:4]
  if str(message.content).lower() in ["quit","forfeit","exit"]:
    return "quit"
  if str(message.content) in "123456789":
    if values[int(message.content) - 1] != ' ':
      return "filled"
    else:
      return message.content
  else:
    return "wronginput"


async def single_game(cur_player,ctx,msg,client,player_choice,l):
    # Represents the Tic Tac Toe
    values = [' ' for x in range(9)]

    # Stores the positions occupied by X and O
    player_pos = {'X': [], 'O': []}
 
    # Game Loop for a single game of Tic Tac Toe
    while True:
        embed = await print_tic_tac_toe(values,msg)

        # Try exception block for MOVE input
        
        embed.add_field(name="\u202b",value=f"Player {player_choice[cur_player].mention}'s, turn. Which box? \nBoxes are numbered from 1 to 9 \nYou can type exit/quit/forfeit to exit the game at any moment")
        await msg.edit(content = "\u202b",embed=embed)
        move = await getmove(cur_player,ctx,client,values,player_choice,l)

        if move =="quit":
          if cur_player=="X":
            win = "O"
          else:
            win = "X"
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.add_field(name=f"{player_choice[cur_player].name} Forfeited!!",value=f"Hence, {player_choice[win].name} has Won!!")
          embednew.set_footer(text=f"Game Over!!")
          await msg.edit(embed=embednew)
          # try:
          #   await msg.channel.delete_messages(l)
          # except:
          #   pass
          return
        if move =="timeout":
          if cur_player=="X":
                win = "O"
          else:
                win = "X"
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.add_field(name=f"{player_choice[cur_player].name} didn't reply in Time",value=f"Hence, {player_choice[win].name} has Won!!")
          embednew.set_footer(text=f"Game Over!!")
          await msg.edit(embed=embednew)
          # try:
          #   await msg.channel.delete_messages(l)
          # except:
          #   pass
          return 

        if move == "wronginput"or move =="filled":
          c=True
          while c is True:
            if move =="wronginput":
              await ctx.send("Wrong Input!!! Try Again Enter a no. between 1 and 9",delete_after=2)
            elif move =="filled":
              await ctx.send("Place already filled. Try again!!",delete_after=2)
            elif move =="timeout":
              if cur_player=="X":
                win = "O"
              else:
                win = "X"
              embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
              embednew.add_field(name=f"{player_choice[cur_player].name} didn't reply in Time",value=f"Hence, {player_choice[win].name} has Won!!")
              embednew.set_footer(text=f"Game Over!!")
              await msg.edit(embed=embednew)
              # try:
              #   await msg.channel.delete_messages(l)
              # except:
              #   pass
              return 
            elif move =="quit":
              if cur_player=="X":
                win = "O"
              else:
                win = "X"
              embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
              embednew.add_field(name=f"{player_choice[cur_player].name} Forfeited!!",value=f"Hence, {player_choice[win].name} has Won!!")
              embednew.set_footer(text=f"Game Over!!")
              await msg.edit(embed=embednew)
              # try:
              #   await msg.channel.delete_messages(l)
              # except:
              #   pass
              return
            else:
              c=False
              break
            move = await getmove(cur_player,ctx,client,values,player_choice,l)
              
            

        # Check if the box is not occupied already
        # if values[move - 1] != ' ':
        #     print("Place already filled. Try again!!")
        #     continue

        # Update game information

        # Updating grid status
        values[int(move) - 1] = cur_player

        # Updating player positions
        player_pos[cur_player].append(int(move))

        # Function call for checking win
        if check_win(player_pos, cur_player):
            embed = await print_tic_tac_toe(values,msg)
            embed.add_field(name="\u202b",value=f"Player {player_choice[cur_player].mention} has won the game!!")
            embed.set_footer(text=f"Game Over!!")
            await msg.edit(embed=embed)
            # try:
            #   await msg.channel.delete_messages(l)
            # except:
            #   pass
            return cur_player

        # Function call for checking draw game
        if check_draw(player_pos):
            embed = await print_tic_tac_toe(values,msg)
            embed.add_field(name="\u202b",value=f"Game Drawn!!")
            embed.set_footer(text="Game Over!!")
            await msg.edit(embed=embed)
            # try:
            #   await msg.channel.delete_messages(l)
            # except:
            #   pass
            return 'D'

        # Switch player moves
        if cur_player == 'X':
            cur_player = 'O'
        else:
            cur_player = 'X'

#---------------HANGMAN--------------------------------------

HANGMAN_PICS = ['''
 +---+
     |
     |
     |
    ===''', '''
 +---+
 O   |
     |
     |
    ===''', '''
 +---+
 O   |
 |   |
     |
    ===''', '''
 +---+
 O   |
/|   |
     |
    ===''', '''
 +---+
 O   |
/|\  |
     |
    ===''', '''
 +---+
 O   |
/|\  |
/    |
    ===''', '''
 +---+
 O   |
/|\  |
/ \  |
    ===''']
def getRandomWord():
    words = ['able', 'about', 'account', 'acid', 'across', 'act', 'addition', 'adjustment', 'advertisement', 'after', 'again', 'against', 'agreement', 'air', 'all', 'almost', 'among', 'amount', 'amusement', 'and', 'angle', 'angry', 'animal', 'answer', 'ant', 'any', 'apparatus', 'apple', 'approval', 'arch', 'argument', 'arm', 'army', 'art', 'as', 'at', 'attack', 'attempt', 'attention', 'attraction', 'authority', 'automatic', 'awake', 'baby', 'back', 'bad', 'bag', 'balance', 'ball', 'band', 'base', 'basin', 'basket', 'bath', 'be', 'beautiful', 'because', 'bed', 'bee', 'before', 'behaviour', 'belief', 'bell', 'bent', 'berry', 'between', 'bird', 'birth', 'bit', 'bite', 'bitter', 'black', 'blade', 'blood', 'blow', 'blue', 'board', 'boat', 'body', 'boiling', 'bone', 'book', 'boot', 'bottle', 'box', 'boy', 'brain', 'brake', 'branch', 'brass', 'bread', 'breath', 'brick', 'bridge', 'bright', 'broken', 'brother', 'brown', 'brush', 'bucket', 'building', 'bulb', 'burn', 'burst', 'business', 'but', 'butter', 'button', 'by', 'cake', 'camera', 'canvas', 'card', 'care', 'carriage', 'cart', 'cat', 'cause', 'certain', 'chain', 'chalk', 'chance', 'change', 'cheap', 'cheese', 'chemical', 'chest', 'chief', 'chin', 'church', 'circle', 'clean', 'clear', 'clock', 'cloth', 'cloud', 'coal', 'coat', 'cold', 'collar', 'colour', 'comb', 'come', 'comfort', 'committee', 'common', 'company', 'comparison', 'competition', 'complete', 'complex', 'condition', 'connection', 'conscious', 'control', 'cook', 'copper', 'copy', 'cord', 'cork', 'cotton', 'cough', 'country', 'cover', 'cow', 'crack', 'credit', 'crime', 'cruel', 'crush', 'cry', 'cup', 'cup', 'current', 'curtain', 'curve', 'cushion', 'damage', 'danger', 'dark', 'daughter', 'day', 'dead', 'dear', 'death', 'debt', 'decision', 'deep', 'degree', 'delicate', 'dependent', 'design', 'desire', 'destruction', 'detail', 'development', 'different', 'digestion', 'direction', 'dirty', 'discovery', 'discussion', 'disease', 'disgust', 'distance', 'distribution', 'division', 'do', 'dog', 'door', 'doubt', 'down', 'drain', 'drawer', 'dress', 'drink', 'driving', 'drop', 'dry', 'dust', 'ear', 'early', 'earth', 'east', 'edge', 'education', 'effect', 'egg', 'elastic', 'electric', 'end', 'engine', 'enough', 'equal', 'error', 'even', 'event', 'ever', 'every', 'example', 'exchange', 'existence', 'expansion', 'experience', 'expert', 'eye', 'face', 'fact', 'fall', 'false', 'family', 'far', 'farm', 'fat', 'father', 'fear', 'feather', 'feeble', 'feeling', 'female', 'fertile', 'fiction', 'field', 'fight', 'finger', 'fire', 'first', 'fish', 'fixed', 'flag', 'flame', 'flat', 'flight', 'floor', 'flower', 'fly', 'fold', 'food', 'foolish', 'foot', 'for', 'force', 'fork', 'form', 'forward', 'fowl', 'frame', 'free', 'frequent', 'friend', 'from', 'front', 'fruit', 'full', 'future', 'garden', 'general', 'get', 'girl', 'give', 'glass', 'glove', 'go', 'goat', 'gold', 'good', 'government', 'grain', 'grass', 'great', 'green', 'grey', 'grip', 'group', 'growth', 'guide', 'gun', 'hair', 'hammer', 'hand', 'hanging', 'happy', 'harbour', 'hard', 'harmony', 'hat', 'hate', 'have', 'he', 'head', 'healthy', 'hear', 'hearing', 'heart', 'heat', 'help', 'high', 'history', 'hole', 'hollow', 'hook', 'hope', 'horn', 'horse', 'hospital', 'hour', 'house', 'how', 'humour', 'I', 'ice', 'idea', 'if', 'ill', 'important', 'impulse', 'in', 'increase', 'industry', 'ink', 'insect', 'instrument', 'insurance', 'interest', 'invention', 'iron', 'island', 'jelly', 'jewel', 'join', 'journey', 'judge', 'jump', 'keep', 'kettle', 'key', 'kick', 'kind', 'kiss', 'knee', 'knife', 'knot', 'knowledge', 'land', 'language', 'last', 'late', 'laugh', 'law', 'lead', 'leaf', 'learning', 'leather', 'left', 'leg', 'let', 'letter', 'level', 'library', 'lift', 'light', 'like', 'limit', 'line', 'linen', 'lip', 'liquid', 'list', 'little', 'living', 'lock', 'long', 'look', 'loose', 'loss', 'loud', 'love', 'low', 'machine', 'make', 'male', 'man', 'manager', 'map', 'mark', 'market', 'married', 'mass', 'match', 'material', 'may', 'meal', 'measure', 'meat', 'medical', 'meeting', 'memory', 'metal', 'middle', 'military', 'milk', 'mind', 'mine', 'minute', 'mist', 'mixed', 'money', 'monkey', 'month', 'moon', 'morning', 'mother', 'motion', 'mountain', 'mouth', 'move', 'much', 'muscle', 'music', 'nail', 'name', 'narrow', 'nation', 'natural', 'near', 'necessary', 'neck', 'need', 'needle', 'nerve', 'net', 'new', 'news', 'night', 'no', 'noise', 'normal', 'north', 'nose', 'not', 'note', 'now', 'number', 'nut', 'observation', 'of', 'off', 'offer', 'office', 'oil', 'old', 'on', 'only', 'open', 'operation', 'opinion', 'opposite', 'or', 'orange', 'order', 'organization', 'ornament', 'other', 'out', 'oven', 'over', 'owner', 'page', 'pain', 'paint', 'paper', 'parallel', 'parcel', 'part', 'past', 'paste', 'payment', 'peace', 'pen', 'pencil', 'person', 'physical', 'picture', 'pig', 'pin', 'pipe', 'place', 'plane', 'plant', 'plate', 'play', 'please', 'pleasure', 'plough', 'pocket', 'point', 'poison', 'polish', 'political', 'poor', 'porter', 'position', 'possible', 'pot', 'potato', 'powder', 'power', 'present', 'price', 'print', 'prison', 'private', 'probable', 'process', 'produce', 'profit', 'property', 'prose', 'protest', 'public', 'pull', 'pump', 'punishment', 'purpose', 'push', 'put', 'quality', 'question', 'quick', 'quiet', 'quite', 'rail', 'rain', 'range', 'rat', 'rate', 'ray', 'reaction', 'reading', 'ready', 'reason', 'receipt', 'record', 'red', 'regret', 'regular', 'relation', 'religion', 'representative', 'request', 'respect', 'responsible', 'rest', 'reward', 'rhythm', 'rice', 'right', 'ring', 'river', 'road', 'rod', 'roll', 'roof', 'room', 'root', 'rough', 'round', 'rub', 'rule', 'run', 'sad', 'safe', 'sail', 'salt', 'same', 'sand', 'say', 'scale', 'school', 'science', 'scissors', 'screw', 'sea', 'seat', 'second', 'secret', 'secretary', 'see', 'seed', 'seem', 'selection', 'self', 'send', 'sense', 'separate', 'serious', 'servant', 'sex', 'shade', 'shake', 'shame', 'sharp', 'sheep', 'shelf', 'ship', 'shirt', 'shock', 'shoe', 'short', 'shut', 'side', 'sign', 'silk', 'silver', 'simple', 'sister', 'size', 'skin', '', 'skirt', 'sky', 'sleep', 'slip', 'slope', 'slow', 'small', 'smash', 'smell', 'smile', 'smoke', 'smooth', 'snake', 'sneeze', 'snow', 'so', 'soap', 'society', 'sock', 'soft', 'solid', 'some', '', 'son', 'song', 'sort', 'sound', 'soup', 'south', 'space', 'spade', 'special', 'sponge', 'spoon', 'spring', 'square', 'stage', 'stamp', 'star', 'start', 'statement', 'station', 'steam', 'steel', 'stem', 'step', 'stick', 'sticky', 'stiff', 'still', 'stitch', 'stocking', 'stomach', 'stone', 'stop', 'store', 'story', 'straight', 'strange', 'street', 'stretch', 'strong', 'structure', 'substance', 'such', 'sudden', 'sugar', 'suggestion', 'summer', 'sun', 'support', 'surprise', 'sweet', 'swim', 'system', 'table', 'tail', 'take', 'talk', 'tall', 'taste', 'tax', 'teaching', 'tendency', 'test', 'than', 'that', 'the', 'then', 'theory', 'there', 'thick', 'thin', 'thing', 'this', 'thought', 'thread', 'throat', 'through', 'through', 'thumb', 'thunder', 'ticket', 'tight', 'till', 'time', 'tin', 'tired', 'to', 'toe', 'together', 'tomorrow', 'tongue', 'tooth', 'top', 'touch', 'town', 'trade', 'train', 'transport', 'tray', 'tree', 'trick', 'trouble', 'trousers', 'true', 'turn', 'twist', 'umbrella', 'under', 'unit', 'up', 'use', 'value', 'verse', 'very', 'vessel', 'view', 'violent', 'voice', 'waiting', 'walk', 'wall', 'war', 'warm', 'wash', 'waste', 'watch', 'water', 'wave', 'wax', 'way', 'weather', 'week', 'weight', 'well', 'west', 'wet', 'wheel', 'when', 'where', 'while', 'whip', 'whistle', 'white', 'who', 'why', 'wide', 'will', 'wind', 'window', 'wine', 'wing', 'winter', 'wire', 'wise', 'with', 'woman', 'wood', 'wool', 'word', 'work', 'worm', 'wound', 'writing', 'wrong', 'year', 'yellow', 'yes', 'yesterday', 'you', 'young', 'Bernhard', 'Breytenbach', 'Android']


    word = random.choice(words)
    return word


async def displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord,msg,ctx):
    a = ''
    # x = missedLetters.replace(",","")
    # x = missedLetters.replace(" ","")
    for letter in missedLetters:
      a = a+ letter
    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):  # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    
    a2 = ''
    for letter in blanks:  # show the secret word with spaces in between each letter
        if letter =="_":
          a2 = a2 +"\\"+letter+' '
        else:
          a2 = a2+letter+' '
    # content=f'''{HANGMAN_PICS[len(missedLetters)]}
    # Missed Letters: {a}
    # {a2}'''
    
    embednew = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embednew.add_field(name="\u202b",value=f'''
    ```
    {HANGMAN_PICS[len(missedLetters)]}
    ```
    ''',inline=False)
    embednew.add_field(name="\u202b",value=f'''Letters Missed: {missedLetters}''',inline=False)
    embednew.add_field(name=f"\u202b",value=f'''
    {a2}

    ''',inline=False)
    embednew.add_field(name="HOW TO PLAY?",value='''You Have 6 attempts to guess the correct word.
    You can type exit/quit/forfeit to exit the game at any moment''',inline=False)
    embednew.set_footer(text=f"Currently Playing : {ctx.author.name}")
    await msg.edit(embed=embednew)
    return 

async def getGuess(alreadyGuessed,client,ctx,l):
    while True:
      def check(m):
        return m.author == ctx.author and m.channel.id == ctx.channel.id 
      try:
        message = await client.wait_for('message',timeout=300,check=check)
      except Exception as e :
        return "timeout"
      msgcontent = message.content.lower()
      # l.append(message)
      
      # if len(l)==4:
      #   try:
      #     await message.channel.delete_messages(l)
      #   except:
      #     pass
      #   del l[:4]
      if msgcontent=="quit" or msgcontent=="forfeit":
        return "quit"
      if len(msgcontent) != 1:
        await ctx.channel.send('Please enter a single letter.',delete_after=2)
        return
      elif msgcontent in alreadyGuessed:
        await ctx.channel.send('You have already guessed that letter. Choose another letter again.',delete_after=2)
        return
        #     print('You have already guessed that letter. Choose again.')
      elif msgcontent not in 'abcdefghijklmnopqrstuvwxyz':
          await ctx.send('Please enter a LETTER.',delete_after=2)
          return
      else:
          return msgcontent


# def playAgain():
#     return input("\nDo you want to play again? ").lower().startswith('y')

class Games(commands.Cog):
  def __init__(self,client):
    self.client = client 

  @commands.command(aliases=["HANGMAN","Hangman"],brief = ">hangman",description = "Starts a game of hangman")
  async def hangman(self,ctx):
    l=[]
   # await msg.edit(content="You Have 6 attempts to guess the correct word. All The Best!!")
    # time.sleep(1)
    missedLetters = ''
    correctLetters = ''
    secretWord = getRandomWord()
    gameIsDone = False

    
    embed = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embed.add_field(name="HOW TO PLAY?",value='''You Have 6 attempts to guess the correct word. Send your guess in the channel down below.
    You can type quit/forfeit to exit the game at any moment
    
    The Game has a Timeout Error, if you don't send any response for 5 minutes the game will be over.''',inline=False)
    embed.set_footer(text=f"Currently Playing : {ctx.author.name}")
    msg= await ctx.send(embed=embed)
    await asyncio.sleep(3.6)
    while True:
        await displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord,msg,ctx)

        guess = await getGuess(missedLetters + correctLetters,self.client,ctx,l)
        if guess is None:
          continue
        if guess == "quit":
          embednew = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.add_field(name=f"{ctx.author.name} Forfeited!!",value=f'''The correct word was **{secretWord}**!!''')
          embednew.set_footer(text=f"Game Over")
          await msg.edit(embed=embednew)
          # try:
          #   await ctx.channel.delete_messages(l)
          # except:
          #   pass
          return 
        if guess == "timeout":
          embednew = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.add_field(name=f"Timed Out!!",value=f'''{ctx.author.mention} I waited for 5 minutes for your response but didn't get any.
          The correct word was **{secretWord}**!!''')
          embednew.set_footer(text=f"Game Over")
          await msg.edit(embed=embednew)
          # try:
          #   await ctx.channel.delete_messages(l)
          # except:
          #   pass
          return 
        if guess in secretWord:
            correctLetters = correctLetters + guess
        
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                embednew = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
                embednew.add_field(name=f"{ctx.author.name} Won!!",value=f'''You guessed the word **{secretWord}** correctly!!''')
                embednew.set_footer(text=f"Game Over")
                await msg.edit(embed=embednew)
                # print('\nYes! The secret word is "' +
                #       secretWord + '"! You have won!')
                gameIsDone = True
        else:
            # if len(missedLetters)!=0:
            missedLetters = missedLetters + guess
            # else:
            #   missedLetters = missedLetters + guess
            
            # x = missedLetters.replace(",","")
            # x = missedLetters.replace(" ","")
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                await displayBoard(HANGMAN_PICS, missedLetters,
                            correctLetters, secretWord,msg,ctx)
                embednew = discord.Embed(title="<:hangman:836587894192996382> HANGMAN",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
                embednew.add_field(name=f"{ctx.author.name} lost!!",value=f'''You have ran out of guesses!\nAfter {str(len(missedLetters))} missed guesses and                       {str(len(correctLetters))} correct guesses, the word was **{secretWord}** ''')
                embednew.set_footer(text=f"Game Over")
                await msg.edit(embed=embednew)
                # print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' +
                #       str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                gameIsDone = True

        if gameIsDone:
            # try:
            #   await ctx.channel.delete_messages(l)
            # except:
            #   pass 
            return 

#-------------------TICTACTOE-------------------------
  @commands.command(aliases = ["ttt","TTT","Ttt"],description="Starts a game of tic tac toe")

  async def tictactoe(self,ctx,member2: discord.Member):
    mem1 = ctx.author
    if member2 is not None:
      mem2 = member2
      embed = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"{mem2.mention} will you like to play TIC-TAC-TOE with {ctx.author.mention}? Reply with y/yes or n/no to confirm",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
      embed.set_footer(text=f"Game in Progress!!")
      msg = await ctx.send(f"{mem2.mention}",embed=embed)
      check = await checkplayer2(mem2,ctx,self.client)

      if check =="no":
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"{mem2.mention} declined the request to play with you {ctx.author.mention}",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.set_footer(text=f"Request Declined")
          await msg.edit(content="\u202b",embed=embednew)
          return 
      elif check =="timeout":
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"Request timed Out!!.\n {mem2.mention} didn't reply in time",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.set_footer(text=f"Request Timed Out")
          await msg.edit(embed=embednew)
          return         
      elif check == "retry":
        while check=="retry":
          # await ctx.send("type y/yes or n/no")
          check = await checkplayer2(mem2,ctx,self.client)
        if check =="timeout":
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"Request timed Out!!.\n {mem2.mention} didn't reply in time",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.set_footer(text=f"Request Timed Out")
          await msg.edit(embed=embednew)
          return 
        elif check =="no":
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"{mem2.mention} declined the request to play with you {ctx.author.mention}",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.set_footer(text=f"Request Declined")
          await msg.edit(content="\u202b",embed=embednew)
          return   
        else:
          pass
      if check =="yes":
            # Stores the player who chooses X and O
        l=[]
        cur_player = mem1

        # Stores the choice of players
        player_choice = {'X': "", 'O': ""}

        # Stores the options
        options = ['X', 'O']
        embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"What do you want to choose? {mem1.mention}\n X or O \nType in the channel down below.",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
        embednew.set_footer(text=f"Game in Progress!!")
        await msg.edit(content = f"{mem1.mention}",embed=embednew)
        # print("Turn to choose for", cur_player)
        # print("Enter 1 for X")
        # print("Enter 2 for O")
        # print("Enter 3 to Quit")
        # Conditions for player choice
        choice = await getx(mem1,self.client,ctx)
        
        if choice =="timeout":
          embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"Request timed Out!!.\n {mem1.mention} didn't reply in time",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embednew.set_footer(text=f"Request Timed Out")
          await msg.edit(content="\u202b",embed=embednew)
          return
        elif choice == "retry":        
          while choice=="retry":
            # await ctx.send("Wrong input!. Try again",delete_after =2)
            choice = await getx(mem1,self.client,ctx)
            
          if choice =="timeout":
            embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE",description=f"Request timed Out!!.\n {mem1.mention} didn't reply in time",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
            embednew.set_footer(text=f"Request Timed Out")
            await msg.edit(content="\u202b",embed=embednew)
            return 
          else:
            pass
        if choice == "X":
            player_choice['X'] = cur_player
            if cur_player == mem1:
                player_choice['O'] = mem2
            else:
                player_choice['O'] = mem1

        elif choice == "O":
            player_choice['O'] = cur_player
            if cur_player == mem1:
                player_choice['X'] = mem2
            else:
                player_choice['X'] = mem1
        await single_game(choice,ctx,msg,self.client,player_choice,l)
        return
  @commands.command(aliases=['GUESS','Guess'],description = "Guess a no. b/w 1 and 10")
  async def guess(self,ctx):
    embed=discord.Embed(title="Guess The No.",description="I have chosen a no. between 1-->10 . You have 3 chances to guess the no. Let's Begin",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embed.set_footer(text=f"Currently Playing : {ctx.author.name}",icon_url=ctx.author.avatar.url)
    message =await ctx.send(embed=embed)
    await asyncio.sleep(2)
    number = random.randint(1,10)
    guess_count = 0
    embed = discord.Embed(title="Guess The No.",description=f"Enter Your Guess in the channel below!\n\n You have {3-guess_count} chances left",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embed.set_footer(text=f"Currently Playing : {ctx.author.name}",icon_url=ctx.author.avatar.url)
    await message.edit(embed=embed)

    while guess_count < 3:

      def check(m):
        return m.author == ctx.author and m.channel==ctx.channel
      try:
        msg = await self.client.wait_for('message', timeout=60,check=check)
        guess_count += 1
        if not msg.content.isdigit():
          
          embed = discord.Embed(title="Guess The No.",description=f"Enter an integer \n\n **You have {3-guess_count} chances left**",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Currently Playing : {ctx.author.name}",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed)
          # guess_count += 1
          continue
        guess = int(msg.content)
        if guess < number:
          embed = discord.Embed(title="Guess The No.",description=f"Your guess is smaller than my no.!\nTry Again\n\n **You have {3-guess_count} chances left**",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Currently Playing : {ctx.author.name}",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed)
        elif guess > number:
          embed = discord.Embed(title="Guess The No.",description=f"Your guess is bigger than my no.!\nTry Again\n\n **You have {3-guess_count} chances left**",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Currently Playing : {ctx.author.name}",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed)
        elif guess == number:
          embed = discord.Embed(title="Guess The No.",description=f"You Won!! \n You guessed the no. `{number}` correctly",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Game Over! {ctx.author.name} Won!",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed)          
          return
        # guess_count += 1
        if guess_count == 3 and guess != number:
          embed = discord.Embed(title="Guess The No.",description=f"You Lost!! \n The correct no. was `{number}`",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Game Over! {ctx.author.name} Lost!",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed)  
          return
      except asyncio.TimeoutError:
          embed = discord.Embed(title="Game Timed Out!",description=f"The Game Ended . {ctx.author.name}#{ctx.author.discriminator} didn't reply in time",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
          embed.set_footer(text=f"Game Timed Out",icon_url=ctx.author.avatar.url)
          await message.edit(embed=embed) 
          return 

#------TIC TAC TOE BUTTONS----------------------
  @commands.command(aliases=["ticbuttons","tttbuttons","ticbut","tttbut"],description= '''
The experience of playing TicTacToe is now even better. You can now play the game by clicking on buttons just like you play on a real game app!!.
To play type `>ticbuttons <member2>` and start playing, once the 2nd member accepts to play with you, by clicking on the buttons to send your response''')
  async def tictactoebuttons(self,ctx: commands.Context, member2 : discord.Member):
      # view = discord.ui.View()  # this is the view object that holds all the components
      # for x in range(5):
      #     for y in range(4):
      #         # print(TicTacToe(x, y, ctx))
      #         view.add_item(TicTacToe(x, y, ctx))
      # # button = discord.ui.Button(label="SUPPORT SERVER", style=discord.ButtonStyle.link,
      # #                            url="https://discord.gg/tTr6DvyRCH", emoji="<:support:849646432138559488>")
      # #
      # # view.add_item(button)  # this adds the button onto the view

      mem1 = ctx.author
      if member2 is not None:
          mem2 = member2
          embed = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE-Buttons",
                                description=f"{mem2.mention} will you like to play TIC-TAC-TOE-Buttons with {ctx.author.mention}? Reply with y/yes or n/no to confirm",
                                colour=discord.Colour.purple(), timestamp=datetime.utcnow())
          embed.set_footer(text=f"Game in Progress!!")
          msg = await ctx.send(f"{mem2.mention}",embed=embed)
          check = await checkplayerticbutton(mem2, ctx, self.client)

          if check == "no":
              embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE-Buttons",
                                      description=f"{mem2.mention} declined the request to play with you {ctx.author.mention}",
                                      colour=discord.Colour.purple(), timestamp=datetime.utcnow())
              embednew.set_footer(text=f"Request Declined")
              await msg.edit(embed=embednew)
              return
          elif check == "timeout":
              embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE-Buttons",
                                      description=f"Request timed Out!!.\n {mem2.mention} didn't reply in time",
                                      colour=discord.Colour.purple(), timestamp=datetime.utcnow())
              embednew.set_footer(text=f"Request Timed Out")
              await msg.edit(embed=embednew)
              return
          elif check == "retry":
              while check == "retry":
                  
                  # await ctx.send("type y/yes or n/no",delete_after=2)
                  check = await checkplayerticbutton(mem2, ctx, self.client)
              if check == "timeout":
                  embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE-Buttons",
                                          description=f"Request timed Out!!.\n {mem2.mention} didn't reply in time",
                                          colour=discord.Colour.purple(), timestamp=datetime.utcnow())
                  embednew.set_footer(text=f"Request Timed Out")
                  await msg.edit(embed=embednew)
                  return
              elif check == "no":
                  embednew = discord.Embed(title="<:ttt:837353336662392883> TIC-TAC-TOE-Buttons",
                                          description=f"{mem2.mention} declined the request to play with you {ctx.author.mention}",
                                          colour=discord.Colour.purple(), timestamp=datetime.utcnow())
                  embednew.set_footer(text=f"Request Declined")
                  await msg.edit(embed=embednew)
                  return
              else:
                  pass
          if check == "yes":
              # await msg.delete()
              await msg.edit(content = f"{ctx.author.mention}'s turn",view = TicTacToe(ctx,mem2) ,embed = None)
              pass

async def setup(client):
  await client.add_cog(Games(client))