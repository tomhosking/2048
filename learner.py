import twoohfoureight, math, random, copy


class Agent:
	moves = [
		'r',
		'l',
		'd',
		'u'
	]
	def __init__(self):
		pass
	def get_action(self, state):
		pass
	def give_reward(self, s, sprime, a, r):
		pass
	def end_episode(self):
		pass

class UpLeftAgent(Agent):
	def get_action(self, state):
		# m = math.floor(random.random()*4)
		# return self.moves[m]
		# make some copies of the board to check whether mvoes are valid
		statecopy_l = copy.deepcopy(state)
		statecopy_u = copy.deepcopy(state)
		statecopy_r = copy.deepcopy(state)
		if statecopy_l.do_move("l"):
			return "l"
		elif statecopy_u.do_move("u"):
			return "u"
		elif statecopy_r.do_move("r"):
			return "r"
		else:
			return "d"

class LearningAgent(Agent):

	actionvalues = {}
	turn=0
	actions_tried = []
	def __init__(self, epsilon, alpha, n):
		self.epsilon = epsilon
		self.alpha = alpha
		self.n = n
	def get_features(self, state):
		searches=[[0,1],[1,0]]
		features=[0 for i in range(len(searches))]
		max_val=0
		max_loc=[0,0]
		for x in range(0, self.n):
			for y in range(0, self.n):
				# print(x,y)
				f=0
				for delta in searches:
					if state[x][y] !=0 \
						and (x+delta[0]) >= 0 and (x+delta[0]) < self.n \
						and (y+delta[1]) >= 0 and (y+delta[1]) < self.n \
						and state[x+delta[0]][y+delta[1]] == state[x][y]:
						features[f] += 1
					if state[x][y] !=0 \
						and (x-delta[0]) >= 0 and (x-delta[0]) < self.n \
						and (y-delta[1]) >= 0 and (y-delta[1]) < self.n \
						and state[x-delta[0]][y-delta[1]] == state[x][y]:
						features[f] += 1
					f+=1
					if state[x][y] > max_val:
						max_val = state[x][y]
						max_loc = [x,y]
		if features[1] > features[0]:
			features[1]=1
			features[0] = 0
		else:
			features[1]= (1 if features[1] == features[0] else 0)
			features[0] = 1
		features.append(max_loc[0])
		features.append(max_loc[1])
		return repr(features)
	def get_action(self, state):
		self.turn += 1
		state = self.get_features(state.board)
		if random.random() < self.epsilon:
			# explore!
			m = math.floor(random.random()*len(self.moves))
			action = self.moves[m]
		else:
			# pick max (or rand if unexplored)
			max_r = 0.
			m = math.floor(random.random()*4)
			best_action = self.moves[m]
			for move in self.moves:
				if (state, move) in self.actionvalues:
					(samples, r) = self.actionvalues[(state, move)]
					if r > max_r:
						max_r = r
						best_action = move
			action= best_action
		self.actions_tried.append((state, action))
		return action
	def give_reward(self, s, sprime, a ,r):
		self.latestReward = r
	def end_episode(self):
		# update actionvalues
		for (state, move) in self.actions_tried:
			new_samples=1
			new_r=self.latestReward
			if (state, move) in self.actionvalues:
				(samples, r) = self.actionvalues[(state, move)]
				new_samples += samples
				max_r = 0
				for m in self.moves:
					if (state,m) in self.actionvalues.keys() and self.actionvalues[(state,m)][1] > max_r:
						max_r = self.actionvalues[(state,m)][1]
				new_r = r + self.alpha * (new_r + max_r*0 - r)
			self.actionvalues[(state,move)] = (new_samples, new_r)
		self.latestReward = 0.
		self.turn = 0
		self.actions_tried = []
		# print(self.actionvalues)
keep_trying = True
game_count=0
n=4
agent = LearningAgent(0.5,0.1,n)
scores=[]
while keep_trying:
	board = twoohfoureight.Board(n)
	game_over = False
	while(not game_over):
		prevstate = copy.deepcopy(board)
		move = agent.get_action(board)
		if not move in board.moves:
			pass# print("Not a valid move!")
		else:
			if not board.do_move(move):
				# print("That's not allowed here")
				if not board.remaining_moves_exist():
					# print("You lose!")
					game_over = True
			# print(board)
		if board.max_tile == 2048:
			print("Congrats, you made 2048!")
			game_over = True
		# agent.give_reward(prevstate, board, move, (board.max_tile if game_over else 0))
		agent.give_reward(prevstate, board, move, (board.max_tile))
	# print("You scored ", board.get_board_value())
	# print(board)
	game_count += 1
	if board.max_tile == 2048:
		keep_trying = False
	agent.end_episode()
	scores.append(board.max_tile)
	if game_count % 500 == 0:
		# print(agent.actionvalues)
		# print(board)
		print(game_count, " ", agent.epsilon)#, " ", scores[-1])
		print(sum(scores[-250:-1])/250, flush=True)
		print(max(scores[-250:-1]))
		agent.epsilon *= 0.997

print("I won!")
