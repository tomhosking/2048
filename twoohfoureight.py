import math, random, copy
n=6


class Board:
	moves = {
		'r': (0,1),
		'l': (0,-1),
		'd': (1,0),
		'u': (-1,0)
	}
	max_tile = 0
	def __init__(self, n):
		self.n = n
		self.board = [[0 for j in range(n)] for i in range(n) ]
		self.add_new_tile()

	def add_new_tile(self):
		locs = []
		for x in range(self.n):
			for y in range(self.n):
				if self.board[x][y] == 0:
					locs.append((x,y))
		pick = locs[math.floor(random.random()*len(locs))]
		self.board[pick[0]][pick[1]] = (1 + round( random.random()))*2

		return self.board

	def do_move(self, move):
		if not move in self.moves:
			raise "Invalid move!"

		delta = self.moves[move]
		is_valid_move = False
		# remove spaces
		for x in range((0 if delta[0] >=0 else self.n-1), (self.n if delta[0] >= 0 else -1), (1 if delta[0] >= 0 else -1)):
			for y in range((0 if delta[1] >= 0 else self.n-1), (self.n if delta[1] >= 0 else -1), (1 if delta[1] >= 0 else -1)):
				# print(x,y)
				if self.board[x][y] !=0 \
					and (x+delta[0]) >= 0 and (x+delta[0]) < self.n \
					and (y+delta[1]) >= 0 and (y+delta[1]) < self.n \
					and self.board[x+delta[0]][y+delta[1]] == 0:
					self.board[x+delta[0]][y+delta[1]] = self.board[x][y]
					self.board[x][y] = 0
					is_valid_move = True

		newboard = copy.deepcopy(self.board)
		# collapse same values
		for x in range((0 if delta[0] <0 else self.n-1), (self.n if delta[0] < 0 else -1), (1 if delta[0] < 0 else -1)):
			for y in range((0 if delta[1] < 0 else self.n-1), (self.n if delta[1] < 0 else -1), (1 if delta[1] < 0 else -1)):
				if self.board[x][y] !=0 \
					and (x+delta[0]) >= 0 and (x+delta[0]) < self.n \
					and (y+delta[1]) >= 0 and (y+delta[1]) < self.n \
					and self.board[x][y] !=False and self.board[x+delta[0]][y+delta[1]] != False \
					and self.board[x+delta[0]][y+delta[1]] == self.board[x][y]:
					newboard[x+delta[0]][y+delta[1]] = 2 * self.board[x+delta[0]][y+delta[1]]
					newboard[x][y]=0
					self.board[x][y] = False
					self.board[x+delta[0]][y+delta[1]] = False
					is_valid_move = True
					self.max_tile = max(newboard[x+delta[0]][y+delta[1]], self.max_tile)
		self.board = newboard

		# then remove blanks again
		for x in range((0 if delta[0] >=0 else self.n-1), (self.n if delta[0] >= 0 else -1), (1 if delta[0] >= 0 else -1)):
			for y in range((0 if delta[1] >= 0 else self.n-1), (self.n if delta[1] >= 0 else -1), (1 if delta[1] >= 0 else -1)):
				# print(x,y)
				if self.board[x][y] !=0 \
					and (x+delta[0]) >= 0 and (x+delta[0]) < self.n \
					and (y+delta[1]) >= 0 and (y+delta[1]) < self.n \
					and self.board[x+delta[0]][y+delta[1]] == 0:
					self.board[x+delta[0]][y+delta[1]] = self.board[x][y]
					self.board[x][y] = 0
					is_valid_move = True
		if is_valid_move:
			self.add_new_tile()
		return is_valid_move
	def get_board_value(self):
		value = 0
		for x in range(self.n):
			for y in range(self.n):
				value += self.board[x][y]
		return value
	def remaining_moves_exist(self):
		for move, delta in self.moves.items():
			for x in range((0 if delta[0] <0 else self.n-1), (self.n if delta[0] < 0 else -1), (1 if delta[0] < 0 else -1)):
				for y in range((0 if delta[1] < 0 else self.n-1), (self.n if delta[1] < 0 else -1), (1 if delta[1] < 0 else -1)):
					if (x+delta[0]) >= 0 and (x+delta[0]) < self.n \
						and (y+delta[1]) >= 0 and (y+delta[1]) < self.n \
						and (self.board[x+delta[0]][y+delta[1]] == self.board[x][y] or self.board[x][y] == 0):
							return True
		return False
	def __str__(self):
		strboard = ""
		for x in range(self.n):
			for y in range(self.n):
				if self.board == 0:
					strboard += " "
				else:
					strboard += str(self.board[x][y])
				strboard += " "

			strboard += "\n"
		return strboard

if __name__ == "__main__":
	board = Board(n)
	print(board)

	game_over = False
	while(not game_over):
		move = input()
		if not move in board.moves:
			print("Not a valid move!")
		else:
			if not board.do_move(move):
				print("That's not allowed here")
				if not board.remaining_moves_exist():
					print("You lose!")
					game_over = True
			print(board)
		if board.max_tile == 2048:
			print("Congrats, you made 2048!")
			game_over = True
	print("You scored ", board.get_board_value())
