import game_module as gm

states = {}

states['game'] = gm.initialize_game()

game_ref = states['game']

access_keys = {}
access_keys['word_key'] = 'word'
access_keys['hint_key'] = 'hint'
access_keys['guessed_key'] = 'guessed_letters'
access_keys['mistakes_key'] = 'mistakes'

gm.run_game_loop(game_ref, access_keys)