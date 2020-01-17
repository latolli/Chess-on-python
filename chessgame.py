import pyglet

library = {
	"pieces": [],
	"moves": [],
	"moving": 0,
	"start_x": 0,
	"start_y": 0,
	"turn": 0,
	"game_on": 0,
	"w_castling_west": True,
	"w_castling_east": True,
	"b_castling_west": True,
	"b_castling_east": True,
	"do_w_castling_west": False,
	"do_w_castling_east": False,
	"do_b_castling_west": False,
	"do_b_castling_east": False
}
"""
Library called "library" includes all global variables that I will be using throghout this code. Most important
ones are "pieces" and "moves". "pieces" is a list of 8 lists that all have 8 items inside. So it forms a 8x8 area
that contains 64 tiles. It also has all the pieces and their location obviously changes when you move the pieces.
"moves" is also a list that forms a same exact 8x8 area, but it doesn't have any pieces in it. It only has tiles
called "empty" or "move_option". So when you click any piece, "moves" list will put "move_option" to every tile that
this piece can be moved to. If you move the piece or click anywhere else, it removes those "move_options".
"""
pyglet.resource.path = ["images"]
window = pyglet.window.Window(400, 446, "Chess")
background = pyglet.resource.image("chessbg.png")
menubg = pyglet.resource.image("menubg.png")

wpawn = pyglet.resource.image("wpawn.png")
wrook_w = pyglet.resource.image("wrookie.png")
wrook_e = pyglet.resource.image("wrookie.png")
wknight = pyglet.resource.image("wknight.png")
wbishop = pyglet.resource.image("wbishop.png")
wqueen = pyglet.resource.image("wqueen.png")
wking = pyglet.resource.image("wking.png")
bpawn = pyglet.resource.image("bpawn.png")
brook_w = pyglet.resource.image("brookie.png")
brook_e = pyglet.resource.image("brookie.png")
bknight = pyglet.resource.image("bknight.png")
bbishop = pyglet.resource.image("bbishop.png")
bqueen = pyglet.resource.image("bqueen.png")
bking = pyglet.resource.image("bking.png")
move_option = pyglet.resource.image("move_option.png")
white_win = pyglet.resource.image("whitewin.png")
black_win = pyglet.resource.image("blackwin.png")
"""
Here I load all the pictures I will need to make the graphical user interface. Every "w" before word means we are 
handling some white team event or piece and "b" means the same for black team.
"""

def starting_formation():
	#Creates new list that have all the pieces in starting location. Also resets all needed library elements.
	library["turn"] = 0
	library["moves"] = []
	library["pieces"] = []
	
	for y in range(8):
		library["moves"].append([])
		for x in range(8):
			library["moves"][y].append("empty")
	for y in range(8):
		library["pieces"].append([])
		for x in range(8):
			if y == 1:
				library["pieces"][y].append(wpawn)
			elif y == 6:
				library["pieces"][y].append(bpawn)
			elif y == 0 and x == 0:
				library["pieces"][y].append(wrook_w)
			elif y == 0 and x == 7:
				library["pieces"][y].append(wrook_e)
			elif y == 7 and x == 0:
				library["pieces"][y].append(brook_w)
			elif y == 7 and x == 7:
				library["pieces"][y].append(brook_e)
			elif y == 0 and x in (1, 6):
				library["pieces"][y].append(wknight)
			elif y == 7 and x in (1, 6):
				library["pieces"][y].append(bknight)
			elif y == 0 and x in (2, 5):
				library["pieces"][y].append(wbishop)
			elif y == 7 and x in (2, 5):
				library["pieces"][y].append(bbishop)
			elif y == 0 and x == 3:
				library["pieces"][y].append(wqueen)
			elif y == 7 and x == 3:
				library["pieces"][y].append(bqueen)
			elif y == 0 and x == 4:
				library["pieces"][y].append(wking)
			elif y == 7 and x == 4:
				library["pieces"][y].append(bking)
			else:
				library["pieces"][y].append("empty")


def show_moves(x, y, piece):
	#Shows all the tiles that selected piece can be moved to.
	if piece == bpawn:
		show_soldier_moves(x, y, piece)
		show_moves_southeast(x, y, piece)
		show_moves_southwest(x, y, piece)
	elif piece == wpawn:
		show_soldier_moves(x, y, piece)
		show_moves_northeast(x, y, piece)
		show_moves_northwest(x, y, piece)
	elif piece in (brook_e, wrook_e):
		show_moves_north(x, y, piece)
		show_moves_south(x, y, piece)
		show_moves_west(x, y, piece)
		show_moves_east(x, y, piece)
	elif piece in (brook_w, wrook_w):
		show_moves_north(x, y, piece)
		show_moves_south(x, y, piece)
		show_moves_west(x, y, piece)
		show_moves_east(x, y, piece)
	elif piece in (bbishop, wbishop):
		show_moves_northeast(x, y, piece)
		show_moves_northwest(x, y, piece)
		show_moves_southwest(x, y, piece)
		show_moves_southeast(x, y, piece)
	elif piece in (bqueen, wqueen):
		show_moves_north(x, y, piece)
		show_moves_south(x, y, piece)
		show_moves_west(x, y, piece)
		show_moves_east(x, y, piece)
		show_moves_northeast(x, y, piece)
		show_moves_northwest(x, y, piece)
		show_moves_southwest(x, y, piece)
		show_moves_southeast(x, y, piece)
	elif piece in (bking, wking):
		show_moves_north(x, y, piece)
		show_moves_south(x, y, piece)
		show_moves_west(x, y, piece)
		show_moves_east(x, y, piece)
		show_moves_northeast(x, y, piece)
		show_moves_northwest(x, y, piece)
		show_moves_southwest(x, y, piece)
		show_moves_southeast(x, y, piece)
		show_castling()
	elif piece in (bknight, wknight):
		show_horse_moves(x, y, piece)


def move_piece(x_start, y_start, x_target, y_target, piece):
	#Moves the selected piece to target location
	library["pieces"][y_start][x_start] = "empty"
	library["moving"] = 0
	library["turn"] += 1
	if library["pieces"][y_target][x_target] == bking:
		library["pieces"][y_target][x_target] = piece
		library["game_on"] = 2
	elif library["pieces"][y_target][x_target] == wking:
		library["pieces"][y_target][x_target] = piece
		library["game_on"] = 3
	elif library["do_w_castling_east"]:
		library["pieces"][0][6] = wking
		library["pieces"][0][5] = wrook_e
		library["pieces"][0][7] = "empty"
	elif library["do_w_castling_west"]:
		library["pieces"][0][1] = wking
		library["pieces"][0][2] = wrook_w
		library["pieces"][0][0] = "empty"
	elif library["do_b_castling_east"]:
		library["pieces"][7][6] = bking
		library["pieces"][7][5] = brook_e
		library["pieces"][7][7] = "empty"
	elif library["do_b_castling_west"]:
		library["pieces"][7][1] = bking
		library["pieces"][7][2] = brook_e
		library["pieces"][7][0] = "empty"
	elif piece == wpawn and y_target == 7:
		library["pieces"][y_target][x_target] = wqueen
	elif piece == bpawn and y_target == 0:
		library["pieces"][y_target][x_target] = bqueen
	else:
		library["pieces"][y_target][x_target] = piece

	if piece in (wking, wrook_w):
		library["w_castling_west"] = False
	if piece in (wking, wrook_e):
		library["w_castling_east"] = False
	if piece in (bking, brook_w):
		library["b_castling_west"] = False
	if piece in (bking, brook_e):
		library["b_castling_east"] = False
	
	library["do_w_castling_east"] = False
	library["do_w_castling_west"] = False
	library["do_b_castling_east"] = False
	library["do_b_castling_west"] = False
	for y, row in enumerate(library["moves"]):
		for x, tile in enumerate(row):
			if tile == move_option:
				library["moves"][y][x] = "empty"
			else:
				continue


def show_moves_north(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to north direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y + 1 + i][x] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y + 1 + i][x] = move_option
				break
			else:
				library["moves"][y + 1 + i][x] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y + 1 + i][x] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y + 1 + i][x] = move_option
				break
			else:
				library["moves"][y + 1 + i][x] = move_option
				if piece == bking:
					break

def show_moves_south(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to south direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y - 1 - i][x] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y - 1 - i][x] = move_option
				break
			else:
				library["moves"][y - 1 - i][x] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y - 1 - i][x] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y - 1 - i][x] = move_option
				break
			else:
				library["moves"][y - 1 - i][x] = move_option
				if piece == bking:
					break

def show_moves_west(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to west direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x - 1 - i < 0:
				break
			elif library["pieces"][y][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y][x - 1 - i] = move_option
				break
			else:
				library["moves"][y][x - 1 - i] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x - 1 - i < 0:
				break
			elif library["pieces"][y][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y][x - 1 - i] = move_option
				break
			else:
				library["moves"][y][x - 1 - i] = move_option
				if piece == bking:
					break

def show_moves_east(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to east direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x + 1 + i > 7:
				break
			elif library["pieces"][y][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y][x + 1 + i] = move_option
				break
			else:
				library["moves"][y][x + 1 + i] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x + 1 + i > 7:
				break
			elif library["pieces"][y][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y][x + 1 + i] = move_option
				break
			else:
				library["moves"][y][x + 1 + i] = move_option
				if piece == bking:
					break

def show_moves_northeast(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to northeast direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x + 1 + i > 7 or y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y + 1 + i][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y + 1 + i][x + 1 + i] = move_option
				break
			else:
				if piece == wpawn:
					break
				else:
					library["moves"][y + 1 + i][x + 1 + i] = move_option
					if piece == wking:
						break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x + 1 + i > 7 or y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y + 1 + i][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y + 1 + i][x + 1 + i] = move_option
				break
			else:
				library["moves"][y + 1 + i][x + 1 + i] = move_option
				if piece == bking:
					break

def show_moves_northwest(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to northwest direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x - 1 - i < 0 or y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y + 1 + i][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y + 1 + i][x - 1 - i] = move_option
				break
			else:
				if piece == wpawn:
					break
				else:
					library["moves"][y + 1 + i][x - 1 - i] = move_option
					if piece == wking:
						break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x - 1 - i < 0 or y + 1 + i > 7:
				break
			elif library["pieces"][y + 1 + i][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y + 1 + i][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y + 1 + i][x - 1 - i] = move_option
				break
			else:
				library["moves"][y + 1 + i][x - 1 - i] = move_option
				if piece == bking:
					break

def show_moves_southwest(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to southwest direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x - 1 - i < 0 or y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y - 1 - i][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y - 1 - i][x - 1 - i] = move_option
				break
			else:
				library["moves"][y - 1 - i][x - 1 - i] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x - 1 - i < 0 or y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x - 1 - i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y - 1 - i][x - 1 - i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y - 1 - i][x - 1 - i] = move_option
				break
			else:
				if piece == bpawn:
					break
				else:
					library["moves"][y - 1 - i][x - 1 - i] = move_option
					if piece == bking:
						break

def show_moves_southeast(x, y, piece):
	#Shows all the tiles that the selected piece can be moved to southeast direction.
	if library["turn"] % 2 == 0:
		for i in range(8):
			if x + 1 + i > 7 or y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				break
			elif library["pieces"][y - 1 - i][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				library["moves"][y - 1 - i][x + 1 + i] = move_option
				break
			else:
				library["moves"][y - 1 - i][x + 1 + i] = move_option
				if piece == wking:
					break
	if library["turn"] % 2 == 1:
		for i in range(8):
			if x + 1 + i > 7 or y - 1 - i < 0:
				break
			elif library["pieces"][y - 1 - i][x + 1 + i] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
				break
			elif library["pieces"][y - 1 - i][x + 1 + i] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
				library["moves"][y - 1 - i][x + 1 + i] = move_option
				break
			else:
				if piece == bpawn:
					break
				else:
					library["moves"][y - 1 - i][x + 1 + i] = move_option
					if piece == bking:
						break

def show_soldier_moves(x, y, piece):
	#Shows all the tiles that the selected pawn can be moved to.
	if piece == wpawn:
		if y == 1:
			if library["pieces"][y + 1][x] == "empty":
				library["moves"][y + 1][x] = move_option
				if library["pieces"][y + 2][x] == "empty":
					library["moves"][y + 2][x] = move_option
		else:
			if library["pieces"][y + 1][x] == "empty":
				library["moves"][y + 1][x] = move_option

	if piece == bpawn:
		if y == 6:
			if library["pieces"][y - 1][x] == "empty":
				library["moves"][y - 1][x] = move_option
				if library["pieces"][y - 2][x] == "empty":
					library["moves"][y - 2][x] = move_option
		else:
			if library["pieces"][y - 1][x] == "empty":
				library["moves"][y - 1][x] = move_option

def show_castling():
	#Shows the move option for castling, if king nor rook hasn't been moved yet.
	if library["turn"] % 2 == 0:
		if library["w_castling_east"] and library["pieces"][0][5] == "empty" and library["pieces"][0][6] == "empty":
			library["moves"][0][6] = move_option
			library["do_w_castling_east"] = True
		if library["w_castling_west"] and library["pieces"][0][1] == "empty" and library["pieces"][0][2] == "empty" and library["pieces"][0][3] == "empty":
			library["moves"][0][1] = move_option
			library["do_w_castling_west"] = True
	if library["turn"] % 2 == 1:
		if library["b_castling_east"] and library["pieces"][7][5] == "empty" and library["pieces"][7][6] == "empty":
			library["moves"][7][6] = move_option
			library["do_b_castling_east"] = True
		if library["b_castling_west"] and library["pieces"][7][1] == "empty" and library["pieces"][7][2] == "empty" and library["pieces"][7][3] == "empty":
			library["moves"][7][1] = move_option
			library["do_b_castling_west"] = True

def show_horse_moves(x, y, piece):
	#Shows all the tiles that the selected knight can be moved to.
	if library["turn"] % 2 == 0:
		if y + 2 > 7 or x + 1 > 7:
			pass
		elif library["pieces"][y + 2][x + 1] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y + 2][x + 1] = move_option
		
		if y + 2 > 7 or x - 1 < 0:
			pass
		elif library["pieces"][y + 2][x - 1] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y + 2][x - 1] = move_option
		
		if y + 1 > 7 or x - 2 < 0:
			pass
		elif library["pieces"][y + 1][x - 2] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y + 1][x - 2] = move_option
		if y - 1 < 0 or x - 2 < 0:
			pass
		elif library["pieces"][y - 1][x - 2] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y - 1][x - 2] = move_option
		
		if y + 1 > 7 or x + 2 > 7:
			pass
		elif library["pieces"][y + 1][x + 2] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y + 1][x + 2] = move_option

		if y - 1 < 0 or x + 2 > 7:
			pass
		elif library["pieces"][y - 1][x + 2] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y - 1][x + 2] = move_option

		if y - 2 < 0 or x + 1 > 7:
			pass
		elif library["pieces"][y - 2][x + 1] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y - 2][x + 1] = move_option
		
		if y - 2 < 0 or x - 1 < 0:
			pass
		elif library["pieces"][y - 2][x - 1] in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
			pass
		else:
			library["moves"][y - 2][x - 1] = move_option
	
	if library["turn"] % 2 == 1:
		if y + 2 > 7 or x + 1 > 7:
			pass
		elif library["pieces"][y + 2][x + 1] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y + 2][x + 1] = move_option
		
		if y + 2 > 7 or x - 1 < 0:
			pass
		elif library["pieces"][y + 2][x - 1] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y + 2][x - 1] = move_option
		
		if y + 1 > 7 or x - 2 < 0:
			pass
		elif library["pieces"][y + 1][x - 2] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y + 1][x - 2] = move_option
		if y - 1 < 0 or x - 2 < 0:
			pass
		elif library["pieces"][y - 1][x - 2] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y - 1][x - 2] = move_option
		
		if y + 1 > 7 or x + 2 > 7:
			pass
		elif library["pieces"][y + 1][x + 2] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y + 1][x + 2] = move_option

		if y - 1 < 0 or x + 2 > 7:
			pass
		elif library["pieces"][y - 1][x + 2] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y - 1][x + 2] = move_option

		if y - 2 < 0 or x + 1 > 7:
			pass
		elif library["pieces"][y - 2][x + 1] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y - 2][x + 1] = move_option
		
		if y - 2 < 0 or x - 1 < 0:
			pass
		elif library["pieces"][y - 2][x - 1] in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
			pass
		else:
			library["moves"][y - 2][x - 1] = move_option

#mainloop

@window.event
def on_draw():
	turns = "Turns: {}".format(str(library["turn"]))
	turn_counter = pyglet.text.Label(turns,
    font_name="serif",
    font_size=16,
    color=(0, 0, 0, 255),
    x=285, y=408,
    anchor_x="left", anchor_y="bottom")

	if library["game_on"] == 1:
		window.clear()
		background.blit(0, 0)
		for y, row in enumerate(library["pieces"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				else:
					tile.blit((x * 50 + 5), (y * 50 + 5))
		for y, row in enumerate(library["moves"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				elif tile == move_option:
					tile.blit((x * 50 + 15), (y * 50 + 15))
		turn_counter.draw()
	elif library["game_on"] == 2:
		window.clear()
		background.blit(0, 0)
		turn_counter.draw()
		for y, row in enumerate(library["pieces"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				else:
					tile.blit((x * 50 + 5), (y * 50 + 5))
		for y, row in enumerate(library["moves"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				elif tile == move_option:
					tile.blit((x * 50 + 15), (y * 50 + 15))
		white_win.blit(125, 175)
	elif library["game_on"] == 3:
		window.clear()
		background.blit(0, 0)
		turn_counter.draw()
		for y, row in enumerate(library["pieces"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				else:
					tile.blit((x * 50 + 5), (y * 50 + 5))
		for y, row in enumerate(library["moves"]):
			for x, tile in enumerate(row):
				if tile == "empty":
					continue
				elif tile == move_option:
					tile.blit((x * 50 + 15), (y * 50 + 15))
		black_win.blit(125, 175)
	else:
		starting_formation()
		window.clear()
		menubg.blit(0, 0)

@window.event
def on_mouse_press(x, y, button, modifiers):
	x_coordinate = int(x / 50)
	y_coordinate = int(y / 50)
	if library["game_on"] == 1:
		if 9 < x < 71 and 405 < y < 441:
			library["game_on"] = 0
		elif y > 400:
			pass
		else:
			piece = library["pieces"][y_coordinate][x_coordinate]
			target = library["moves"][y_coordinate][x_coordinate]
			if (library["turn"] % 2) == 0:
				if button == pyglet.window.mouse.LEFT:
					if target == move_option:
						move_piece(library["start_x"],library["start_y"] , x_coordinate, y_coordinate, library["moving"])
					elif piece in (bpawn, brook_w, brook_e, bbishop, bknight, bking, bqueen):
						pass
					else:
						for y, row in enumerate(library["moves"]):
							for x, tile in enumerate(row):
								if tile == move_option:
									library["moves"][y][x] = "empty"
								else:
									continue
						library["moving"] = piece
						library["start_x"] = x_coordinate
						library["start_y"] = y_coordinate
						show_moves(x_coordinate, y_coordinate, piece)
			elif (library["turn"] % 2) == 1:
				if button == pyglet.window.mouse.LEFT:
					if target == move_option:
						move_piece(library["start_x"],library["start_y"] , x_coordinate, y_coordinate, library["moving"])
					elif piece in (wpawn, wrook_w, wrook_e, wbishop, wknight, wking, wqueen):
						pass
					else:
						for y, row in enumerate(library["moves"]):
							for x, tile in enumerate(row):
								if tile == move_option:
									library["moves"][y][x] = "empty"
								else:
									continue
						library["moving"] = piece
						library["start_x"] = x_coordinate
						library["start_y"] = y_coordinate
						show_moves(x_coordinate, y_coordinate, piece)
	elif library["game_on"] in (2, 3):
		if 9 < x < 71 and 405 < y < 441:
			library["game_on"] = 0
	else:
		if 151 < x < 245 and 294 < y < 331:
			library["game_on"] = 1


pyglet.app.run()
