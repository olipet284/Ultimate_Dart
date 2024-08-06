from dart import DARTS
from utils import int_input, ask_Y_n, dartboard_heatmap
from kunst import home_menu, home_menu2

game = DARTS()
valid_games = {'1', '2', '3', '4', '501', 'HS'}
num_round = 0
while True:
	num_round += 1
	if num_round > 1:
		print(home_menu2)
	else:
		print(home_menu)
	
	game_type = str(input('Hvad vil du gerne spille:\n'))
	while game_type not in valid_games:
		print('Dette er desværre ingen af valgmulighederne, prøv igen.\n')
		game_type = str(input('Hvad vil du gerne spille:\n'))

	if game_type == '1':
		start_score = int_input(
		    '\nHvor mange point skal der være til at starte med? (Eks. 301, 501)\n'
		)
		double_in = ask_Y_n('\nDouble-in  (Y/n): ')
		double_out = ask_Y_n('\nDouble-out (Y/n): ')
		game.score_down(start_score, double_in, double_out)
	elif game_type == '2':
		target_score = int_input('\nHvor mange point skal man score for at vinde?\n')
		game.first_to(target_score)
	elif game_type == '3':
		game.around_the_world()
	elif game_type == '4':
		game.killer()
	elif game_type == '501':
		game.score_down()
	elif game_type == 'HS':
		game.highscore()
	elif game_type == 'HM':
		cont = True
		while cont:
			for p in range(game.n_players):
				print(f'Tast {p+1:2} for {game.names[p]}')
			show_me_player = int_input('\nHvem vil du gerne se Heatmap for?\n')
			dartboard_heatmap(game.shot_history[show_me_player - 1],game.names[show_me_player - 1])
			cont = ask_Y_n('\nVil du se endnu en? (Y/n) ')
	valid_games.add('HM')

