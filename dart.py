import pyfiglet
import random
import kunst
from pyfiglet import figlet_format
from utils import int_input, ask_Y_n, in_range, is_double
from copy import deepcopy


class DARTS():

	def __init__(self):
		print()
		print(kunst.ultimate_dart_banner)
		print()
		self.n_players = None
		self.names = None
		return None

	def random_order(self):
		names = {}
		shot_history = {}
		index = random.sample(range(self.n_players), self.n_players)
		
		for p, new_p in zip(range(self.n_players), index):
			names[p] = self.names[new_p]
			shot_history[p] = self.shot_history[new_p]
		self.names = names
		self.shot_history = shot_history


	def update_players(self, get_names=True):
		if self.n_players != None:
			if not ask_Y_n('\nVil du ændre antal spillere og navne? (Y/n): '):
				return None

		self.n_players = int_input('Hvor mange spillere er der?\n')

		if get_names:
			get_names = ask_Y_n('\nVil du angive spillernavne? (Y/n): ')

		if get_names:
			names = {}
			for i in range(self.n_players):
				while True:
					names[i] = str(input(f'\nNavn på spiller nr. {i + 1}:\n'))
					if len(names[i]) > 0:
						break
					print('"" is not a name silly, try again.')
		else:
			names = {i: f'Spiller {i+1}' for i in range(self.n_players)}
		self.names = names

		self.shot_history = {i: [] for i in range(self.n_players)}
		
		if get_names and ask_Y_n('\nVil du spille med tilfældige rækkefølge? (Y/n): '):
			self.random_order()


	def scored(self, dar, player, sht_num, try_num=1):
		scr = None
		if len(dar) == 0:
			dar = 'empty'
		if dar in ['fuck', 'FUCK']:
			return False, False
		elif dar == '0':
			scr = 0
		elif dar == '25':
			scr = 25
		elif dar in ['be', 'BE', 'Be', 'bE']:
			scr = 50
		elif dar[0] in ['d', 'D'] and in_range(dar[1:]):
			scr = 2 * int(dar[1:])
		elif dar[0] in ['t', 'T'] and in_range(dar[1:]):
			scr = 3 * int(dar[1:])
		elif in_range(dar):
			scr = int(dar)
		else:
			if try_num % 3 == 0:
				print('*' * 10 + '  Format  ' + '*' * 10)
				print('1,   2, ...,  20 - I tilfælde af single')
				print('D1, D2, ..., D20 - I tilfælde af double')
				print('T1, T2, ..., T20 - I tilfælde af triple')
				print('25               - I tilfælde af Bull')
				print('BE               - I tilfælde af Bull\'s Eye')
				print('0                - I tilfælde af Miss')
				print('*' * 30)
			print('\nVærdien blev desværre ikke genkendt')
			dar = str(input(f'{sht_num+1}. Dart: '))
			scr, dar = self.scored(dar, player, sht_num, try_num + 1)
		if scr != None:
			self.shot_history[player].append(dar)
		return scr, dar


	def victory(self, player):
		ascii_win = pyfiglet.figlet_format('Tillykke')
		ascii_name = pyfiglet.figlet_format(self.names[player])
		
		print()
		print(ascii_win)
		print(ascii_name)
		print()

	# -----------------------
	# ------   GAMES   ------
	# -----------------------

	def score_down(self, start_score=501, double_in=False, double_out=True):
		self.update_players()
		scores = {p: start_score for p in range(self.n_players)}

		winner_found = False
		p = 0
		while True:
			bust = False
			print()
			print('-' * 20)
			print(f'\nSpiller {p+1}: {self.names[p]}')
			print(f'Mangler {scores[p]} point\n')

			tot_scr = 0

			# -------------
			# 1. Skud
			# -------------

			scr1, dar1 = self.scored(str(input(f'1. Dart: ')), p, 0)
			if scr1 == dar1:
				p -= 1
				if p < 0:
					p = self.n_players - 1
				last_three = self.shot_history[p][-3:]
				for i, dar in enumerate(last_three):
					scores[p] += self.scored(dar, p, i + 1)[0]
				if len(self.shot_history[p]) == 6:
					self.shot_history[p] = []
				else:
					self.shot_history[p] = self.shot_history[p][:-6]
				print(f'DU HAR LAVET EN FEJL. ANGIV VENLIGST FOR SPILLER {p + 1}: {self.names[p]} igen')
				continue
			tot_scr += scr1
			
			if tot_scr > scores[p]:
				print('BUST')
				p = (p + 1) % self.n_players
				continue
			elif scores[p] == tot_scr:
				if double_out:
					if is_double(dar1):
						self.victory(p)
						break
					print('BUST, skal være double out')
					p = (p + 1) % self.n_players
					continue
				else:
					self.victory(p)
					break
			elif (scores[p] == start_score) and double_in:
				if not is_double(dar1):
					tot_scr = 0
					scr1 = 0
			elif double_out and (scores[p] - tot_scr == 1):
				print('BUST')
				p = (p + 1) % self.n_players
				continue

			print(f'Mangler nu {scores[p] - tot_scr}')

			# -------------
			# 2. Skud
			# -------------

			scr2, dar2 = self.scored(str(input(f'2. Dart: ')), p, 1)
			if scr2 == dar2: 
				self.shot_history[p] = self.shot_history[p][:-1]
				print(f'DU HAR LAVET EN FEJL. ANGIV VENLIGST FOR SPILLER {p + 1}: {self.names[p]} igen')
				continue
			tot_scr += scr2
			
			if tot_scr > scores[p]:
				print('BUST')
				p = (p + 1) % self.n_players
				continue
			elif scores[p] == tot_scr:
				if double_out:
					if is_double(dar2):
						self.victory(p)
						break
					print('BUST, skal være double out')
					p = (p + 1) % self.n_players
					continue
				else:
					self.victory(p)
					break
			elif (scores[p] == start_score) and double_in:
				if not is_double(dar2):
					tot_scr = 0
					scr2 = 0
			elif double_out and (scores[p] - tot_scr == 1):
				print('BUST')
				p = (p + 1) % self.n_players
				continue
			
			print(f'Mangler nu {scores[p] - tot_scr}')

			# -------------
			# 3. Skud
			# -------------
			
			scr3, dar3 = self.scored(str(input(f'3. Dart: ')), p, 2)
			if scr3 == dar3: 
				self.shot_history[p] = self.shot_history[p][:-2]
				print(f'DU HAR LAVET EN FEJL. ANGIV VENLIGST FOR SPILLER {p + 1}: {self.names[p]} igen')
				continue
			tot_scr += scr3
			
			if tot_scr > scores[p]:
				print('BUST')
				p = (p + 1) % self.n_players
				continue
			elif scores[p] == tot_scr:
				if double_out:
					if is_double(dar3):
						self.victory(p)
						break
					print('BUST, skal være double out')
					p = (p + 1) % self.n_players
					continue
				else:
					self.victory(p)
					break
			elif (scores[p] == start_score) and double_in:
				if not is_double(dar3):
					tot_scr = 0
					scr3 = 0
			elif double_out and (scores[p] - tot_scr == 1):
				print('BUST')
				p = (p + 1) % self.n_players
				continue
				
			scores[p] -= tot_scr
			print(f'Samlet score: {tot_scr:3}\n')
			print(f'Mangler nu:   {scores[p]:3}\n')

			p = (p + 1) % self.n_players


	def first_to(self, target_score=100):
		self.update_players()
		scores = {p: 0 for p in range(self.n_players)}

		p = -1
		memory = []
		iterat = 0
		mistake_made = False
		while True:
			if mistake_made:
				if len(memory) == 1:
					self.shot_history, scores, p = memory[0]
				else:
					self.shot_history, scores, p = memory[-2]
				if p == -1:
					p = 0
			else:
				p = (p + 1) % self.n_players
			
			shot_hist_copy = deepcopy(self.shot_history)
			scores_copy = deepcopy(scores)
			p_copy = deepcopy(p)
			memory.append((shot_hist_copy, scores_copy, p_copy))
			
			#if not mistake_made:
				
			
			mistake_made = False

			print()
			print('-' * 20)
			print(f'\nSpiller {p+1} - {self.names[p]}')
			print(f'Samlet score: {scores[p]}\n')

			##############################
			##         SHOOTING         ##
			##############################



			scr1, dar1 = self.scored(str(input(f'1. Dart: ')), p, 0)
			if scr1 == dar1:
				mistake_made = True
				continue
			tot_scr = scr1
			if target_score <= tot_scr + scores[p]:
				break
			

			scr2, dar2 = self.scored(str(input(f'2. Dart: ')), p, 1)
			if scr2 == dar2:
				mistake_made = True
				continue
			tot_scr += scr2
			if target_score <= tot_scr + scores[p]:
				break
			

			scr3, dar3 = self.scored(str(input(f'3. Dart: ')), p, 2)
			if scr3 == dar3:
				mistake_made = True
				continue
			tot_scr += scr3
			if target_score <= tot_scr + scores[p]:
				break

			iterat += 1

			scores[p] += tot_scr
			print(f'Scoret denne runde: {tot_scr:3}')
			print(f'Samlet score: {scores[p]}\n')

		self.victory(p)


	def around_the_world(self):
		self.update_players()
		order = [(str(i + 1), f'D{str(i+1)}', f'T{str(i+1)}', f'd{str(i+1)}', f't{str(i+1)}')
		         for i in range(20)] + [('BE', 'be', 'Be', 'bE', '25')]
		target = {p: 0 for p in range(self.n_players)}

		def is_target(dar):
			if dar in order[target[p]]:
				if dar[0] in ['T', 't']:
					return 3
				elif dar[0] in ['D', 'd']:
					return 2
				return 1
			if dar in ['25', 'BE', 'be', 'Be', 'bE'] and (target[p] > 19):
				return 10
			return 0

		def print_target(p):
			print(f'\nDu skal ramme {order[target[p]][0]}')

		p = -1
		memory = []
		iterat = 0
		mistake_made = False
		while True:
			if mistake_made:
				if iterat == 0:
					self.shot_history, target, p = memory[-1]
					p = 0
				else:
					self.shot_history, target, p = memory[-2]
			
			shot_hist_copy = deepcopy(self.shot_history)
			target_copy = deepcopy(target)
			p_copy = deepcopy(p)
			memory.append((shot_hist_copy, target_copy, p_copy))
			
			if not mistake_made:
				p = (p + 1) % self.n_players
			
			mistake_made = False

			print()
			print('-' * 20)
			print(f'\nSpiller {p+1}: {self.names[p]}')
			print_target(p)

			##############################
			##         SHOOTING         ##
			##############################


			scr1, dar1 = self.scored(str(input(f'1. Dart: ')), p, 0)

			if scr1 == dar1:
				mistake_made = True
				continue
			atw_scr = is_target(dar1)
			is_hit = atw_scr > 0

			if target[p] == 20 and is_hit:
				break
			target[p] += atw_scr
			if target[p] > 19:
				target[p] = 20
			if is_hit:
				print_target(p)

			scr2, dar2 = self.scored(str(input(f'2. Dart: ')), p, 1)

			if scr2 == dar2:
				mistake_made = True
				continue
			atw_scr = is_target(dar2)
			is_hit = atw_scr > 0

			if target[p] == 20 and is_hit:
				break
			target[p] += atw_scr
			if target[p] > 19:
				target[p] = 20
			if is_hit:
				print_target(p)

			scr3, dar3 = self.scored(str(input(f'3. Dart: ')), p, 2)

			if scr3 == dar3:
				mistake_made = True
				continue
			atw_scr = is_target(dar3)
			is_hit = atw_scr > 0

			if target[p] == 20 and is_hit:
				break
			target[p] += atw_scr
			if target[p] > 19:
				target[p] = 20
			if is_hit:
				print_target(p)

			iterat += 1
			


		self.victory(p)


	def killer(self):
		self.update_players()
		num_lives = int_input('\nHvor mange liv har hver spiller?\n')
		num_winners = int_input('\nHvor mange vindere er der?\n')

		kills = {p: 0 for p in range(self.n_players)}
		lives = {p: 0 for p in range(self.n_players)}

		all_homes = [(str(i + 1), f'D{str(i+1)}', f'T{str(i+1)}', f'd{str(i+1)}', f't{str(i+1)}')
		             for i in range(20)] + [('BE','be','bE','Be', '25')]
		home = {p: None for p in range(self.n_players)}

		def whose_home(dar):
			for p in range(self.n_players):
				if dar in home[p]:
					return p
			print('ERROR IN CODE')
			return None

		def cur_homes():
			cur_list = []
			for p in range(self.n_players):
				if lives[p] >= 0 and home[p] != None:
					for field in home[p]:
						cur_list.append(field)
			return cur_list

		def is_target(dar):
			if dar in cur_homes():
				if dar == '25':
					return 2
				elif dar in ['BE', 'be', 'Be', 'bE']:
					return 3
				elif dar[0] in ['T', 't']:
					return 3
				elif dar[0] in ['D', 'd']:
					return 2
				return 1
			return 0

		def create_table():
			alive = []
			print()
			row = ''
			for p in range(self.n_players):
				if lives[p] >= 0:
					alive.append(p)
				else:
					continue
				row += ' | '

				row += ' ' * (len(self.names[p]) // 2 - 1)
				if home[p] != None:
					row += f'{home[p][0]:2}'
				else:
					row += f'--'
				if len(self.names[p]) // 2 == len(self.names[p]) / 2:
					row += ' ' * (len(self.names[p]) // 2 - 1)
				else:
					row += ' ' * (len(self.names[p]) // 2)
			row += ' | '
			print(row)

			for p in alive:
				print(f' | ', end='')
				if len(self.names[p]) == 1:
					print(f'{self.names[p]} ', end='')
				else:
					print(f'{self.names[p]}', end='')
			print(f' | ')

			print('-' * len(row))

			for live in range(num_lives):
				for p in alive:
					print(f' | ', end='')
					print(' ' * (len(self.names[p]) // 2), end='')
					if lives[p] >= live + 1:
						print('X', end='')
					else:
						print(' ', end='')
					if len(self.names[p]) == 1:
						print(f' ', end='')
					elif len(self.names[p]) // 2 == len(self.names[p]) / 2:
						print(' ' * (len(self.names[p]) // 2 - 1), end='')
					else:
						print(' ' * (len(self.names[p]) // 2), end='')
				print(f' | ')
			print()

		################
		# FØRSTE RUNDE #
		################
		p = 0
		while True:
			mistake_made = False
			print(f'\nSpiller {p+1} - {self.names[p]}')
			shot = 0
			while True:
				scr, dar = self.scored(str(input(f'\n{shot+1}. Dart: ')), p, shot)
				if scr == dar:
					mistake_made = True
					if p > 0:
						p -= 1
					break
				shot += 1
				if scr == 0:
					continue
				if dar in cur_homes():
					print('Optaget, prøv igen.')
					continue
				elif dar == '25' or (dar in ['BE', 'be', 'Be', 'bE']):
					home[p] = all_homes[-1]
					break
				if dar[0] in ['D', 'T', 'd', 't']:
					dar = dar[1:]
				home[p] = all_homes[int(dar) - 1]
				break
			if mistake_made:
				continue
			p += 1
			create_table()
			if p == self.n_players:
				break

		p = -1
		iterat = 0
		memory = []
		mistake_made = False
		winner_found = False
		while True:
			iterat += 1
			p = (p+1) % self.n_players
			
			if mistake_made:
				if iterat == 2:
					self.shot_history, lives, kills, p = memory[-1]
					continue
				else:
					self.shot_history, lives, kills, p = memory[-2]
				print('Hov, der er vist sket en fejl.')
				print()
				create_table()
				print()

			mistake_made = False
			if not lives[p] >= 0:
				continue
			
			shot_hist_copy = deepcopy(self.shot_history)
			lives_copy = deepcopy(lives)
			kills_copy = deepcopy(kills)
			p_copy = deepcopy(p)
			memory.append((shot_hist_copy, lives_copy, kills_copy, p_copy))
			

			

			print(f'\nSpiller {p+1} - {self.names[p]}')

			for shot in range(3):
				scr, dar = self.scored(str(input(f'{shot+1}. Dart: ')), p, shot)
				if scr == dar:
					mistake_made = True
					break
				scr = is_target(dar)
				is_hit = (scr > 0)
				if dar not in cur_homes():
					continue

				got_hit = whose_home(dar)

				if p == got_hit:
					if lives[p] == num_lives:
						lives[p] -= scr
					else:
						lives[p] += scr
						if lives[p] >= num_lives:
							lives[p] = num_lives
				elif lives[p] == num_lives:
					lives[got_hit] -= scr
					if lives[got_hit] < 0:
						kills[p] += 1
						print()
						print(kunst.skull)
						print()
						print(figlet_format(self.names[p]))
						print()
						print(figlet_format('killed'))
						print()
						print(figlet_format(self.names[got_hit]))
						print()
						if sum(list(kills.values())) == self.n_players - num_winners:
							winner_found = True
							break
				print()
				create_table()
				print()
			if winner_found:
				break

		ascii_win = pyfiglet.figlet_format('Tillykke')
		print()
		print(ascii_win)
		for p in range(self.n_players):
			if lives[p] >= 0:
				ascii_name = pyfiglet.figlet_format(self.names[p])
				print(ascii_name)
		print()

		###############
		# ANTAL KILLS #
		###############
		kills_by_p = [(kills[p], self.names[p]) for p in range(self.n_players)]
		for kill, name in sorted(kills_by_p):
			print(f'{name:10} har fået {kill:2} kills')


	def highscore(self):
		prev_hs = int_input('Tidligere Highscore\n')
		self.update_players(get_names=False)
		scores = {p: 0 for p in range(self.n_players)}

		tot_scr = 0
		p = -1
		memory = []
		mistake_made = False
		while True:
			if mistake_made:
				if p == 0:
					self.shot_history, scores, tot_scr, p = memory[-1]
					continue
				self.shot_history, scores, tot_scr, p = memory[-2]
				print('Hov, der er vist sket en fejl.')
			else:
				p += 1
				shot_hist_copy = deepcopy(self.shot_history)
				scores_copy = deepcopy(scores)
				tot_scr_copy = deepcopy(tot_scr)
				p_copy = deepcopy(p)
				memory.append((shot_hist_copy, scores_copy, tot_scr_copy, p_copy))
				
				
				
			mistake_made = False

			print()
			print('-' * 20)
			print(f'\nSpiller {p+1}')

			##############################
			##         SHOOTING         ##
			##############################

			scr1, dar1 = self.scored(str(input(f'1. Dart: ')), p, 0)
			if scr1 == dar1:
				mistake_made = True
				continue	
			scores[p] += scr1
			scr2, dar2 = self.scored(str(input(f'2. Dart: ')), p, 1)
			if scr2 == dar2:
				mistake_made = True
				continue	
			scores[p] += scr2
			scr3, dar3 = self.scored(str(input(f'3. Dart: ')), p, 2)
			if scr3 == dar3:
				mistake_made = True
				continue
			scores[p] += scr3
			tot_scr += scores[p]

			print(f'Spiller {p+1} scorede: {scores[p]}')
			print(f'I alt har i scoret: {tot_scr}')
			if p + 1 == self.n_players:
				break

		if tot_scr > prev_hs:
			ascii_new_hs = pyfiglet.figlet_format('NEW HIGHSCORE')
			ascii_tot_scr = pyfiglet.figlet_format(f'{tot_scr}')
			print()
			print(ascii_new_hs)
			print()
			print(ascii_tot_scr)
			print()
		else:
			print()
			print(kunst.skull)
			print()

		for p in range(self.n_players):
			print(f'Spiller {p+1:2} - {scores[p]:3}')

