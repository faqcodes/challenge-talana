class Fighter:
  def __init__(self, name, moves_punches, energy=6):
    self.name = name
    self.moves_punches = moves_punches
    self.energy = energy

  def attack(self):
    moves = list()
    is_special_action = True

    # obtiene la primera tupla
    move, punch = self.moves_punches.pop(0)

    ############################
    # TODO: ESTO SE PODRIA MOVER
    ############################
    moves_dic = {
      'DSDP': (3, 'le pega tremendo Taladoken al pobre {}'),
      'ASAP': (2, 'sacude a {} con un Taladoken'),
      'SAK': (3, 'le pega su buen Remuyuken al pobre {}'),
      'SDK': (2, 'hace ver estrellas a {} con un Remuyuken'),

      'P': (1, 'Puñetazo'),
      'K': (1, 'Patada'),

      'W': (0, 'Arriba'),
      'S': (0, 'Izquierda'),
      'A': (0, 'Abajo'),
      'D': (0, 'Derecha'),
    }

    # Al iniciar se valida la combinación de ataques (special_action) y se obtien el daño (damage)
    damage = 0
    special_action = ''

    # para los Taladoken se tiene una combinación de 3 movimientos más un golpe P
    if (len(move) > 0 and len(punch) > 0):
      damage, special_action = moves_dic.get(
        move[-3:] + punch, (0, 'NOT_FOUND'))

      if (special_action == 'NOT_FOUND'):
        # si no hay Taladoken: para los Remuyuken se tiene una combinación de 2 movimientos más un golpe K
        damage, special_action = moves_dic.get(
          move[-2:] + punch, (0, 'NOT_FOUND')
        )

        if (special_action == 'NOT_FOUND'):
          # si no se encuentran movimientos especiales, todos son movimientos ordinarios
          is_special_action = False
          damage, _ = moves_dic.get(punch, (0, ''))
          moves.extend(list(move))
        else:
          moves.extend(list(move.replace(move[-2:], '')))  # ??? validar

      else:
        moves.extend(list(move.replace(move[-3:], '')))  # ??? validar

    # no se encuentran movimientos especiales, todos son movimientos ordinarios
    else:
      is_special_action = False
      damage, _ = moves_dic.get(punch, (0, ''))
      moves.extend(list(move))

    # print(
    #   f'damage: {damage}, is special: {is_special_action}, action: {special_action}, extra moves: {moves}'
    # )

    # se detalla narrativa
    narrativa = ''

    if not is_special_action:
      if len(moves) > 0:
        narrativa = 'se mueve ágilmente'
      if len(moves) > 0 and len(punch) == 0:
        narrativa = 'hace algunos movimientos exóticos sin ningún daño... ({} se ríe)'
      if len(moves) == 0 and len(punch) > 0:
        narrativa = 'se queda quieto'
      if len(punch) > 0:
        _, action = moves_dic.get(punch, ())
        narrativa += (f' y le pega su {action}' if len(narrativa) > 0 else f'le pega su {action}')

    if is_special_action:
        narrativa += (f' y {special_action}' if len(narrativa) > 0 else special_action)

    return damage, narrativa


class Kombat:
  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2

  def define_starting_player(self):
    moves_a = self.player1.moves_punches
    moves_b = self.player2.moves_punches

    # compara el número combinado de movimientos
    if len(moves_a) != len(moves_b):
      return self.player1 if len(moves_a) < len(moves_b) else self.player2

    # si hay empate, obtiene y compara la cantidad de movimientos
    move_a = sum(1 for move, _ in moves_a if move)
    move_b = sum(1 for move, _ in moves_b if move)

    if (move_a != move_b):
      return self.player1 if move_a < move_b else self.player2

    # si hay empate, obtiene y compara la cantidad de golpes
    punches_a = sum(1 for _, punch in moves_a if punch)
    punches_b = sum(1 for _, punch in moves_b if punch)

    if (punches_a != punches_b):
      return self.player1 if punches_a < punches_b else self.player2

    # si hay empate, iniciar con el player 1: hermano mayor B-)
    return self.player1

  def fight(self):
    # se obtiene el atacante y el oponente
    attacker = self.define_starting_player()
    opponent = self.player2 if attacker == self.player1 else self.player1

    print(f'\nTALANA KOMBAT: comienza y {attacker.name} ataca primero\n')

    while True:
      # ataque!: obtiene la acción y el daño que provoca el atacante
      damage, action = attacker.attack()

      # quita energía al oponente
      opponent.energy -= damage

      # fatality
      fatality = 'Fatality! ' if opponent.energy <= 0 else ''

      # narra lo acontecido
      print(f'{fatality}{attacker.name} {action}'.format(opponent.name))

      if opponent.energy <= 0:
        print(
          f'\n{attacker.name} gana la pelea y aún le queda(n) {attacker.energy} de energía\n'
        )
        break

      # switch: cambio de turno de los jugadores
      # si un jugador se queda sin movimientos, el otro continúa hasta terminar... sin piedad
      switch = len(opponent.moves_punches) > 0

      if (switch):
        tmp = attacker
        attacker = opponent
        opponent = tmp

      # si ya no quedan movimientos, se termina el combate
      # el ganador será el que tienen más energía
      if (len(attacker.moves_punches) == 0):
        print('\nNo hubo Fatality pero hay ganador!')
        print(f'{attacker.name} gana la pelea con {attacker.energy} de energía.')
        print(f'El probre {opponent.name} quedó con algo de energía: {opponent.energy}\n')
        break

# data de ejemplos:
data = {
  'player1': {'movimientos': ['D', 'DSD', 'S', 'DSD', 'SD'], 'golpes': ['K', 'P', '', 'K', 'P']},
  'player2': {'movimientos': ['SA', 'SA', 'SA', 'ASA', 'SA'], 'golpes': ['K', '', 'K', 'P', 'P']}
}

# gana Tonyn
# data = {
#   'player1':{'movimientos':['SDD', 'DSD', 'SA', 'DSD'] ,'golpes':['K', 'P', 'K', 'P']},
#   'player2':{'movimientos':['DSD', 'WSAW', 'ASA', '', 'ASA', 'SA'],'golpes':['P', 'K', 'K', 'K', 'P', 'k']}
# }

# gana Arnaldor
# data = {
#   'player1':{'movimientos':['DSD', 'S'] ,'golpes':[ 'P', '']},
#   'player2':{'movimientos':['', 'ASA', 'DA', 'AAA', '', 'SA'],'golpes':['P', '', 'P', 'K', 'K', 'K']}
# }

# data = {
#   'player1':{'movimientos':['', 'ASA', 'DA', 'AAA', '', 'SAA'],'golpes':['P', '', 'P', 'K', 'K', 'K']},
#   'player2':{'movimientos':['DSD', 'S'] ,'golpes':[ 'P', '']}
# }

# obtiene movimientos y golpes (tupla) para cada jugador desde data
player1_moves = [
  (move, punch) for move, punch in zip(data['player1']['movimientos'], data['player1']['golpes'])
]
player2_moves = [
  (move, punch) for move, punch in zip(data['player2']['movimientos'], data['player2']['golpes'])
]

# crear instancias de los jugadores
tony = Fighter('Tonyn', player1_moves)
arnold = Fighter('Arnaldor', player2_moves)

# crea instancia del combate
kombat = Kombat(tony, arnold)
# se iniciar la pelea
kombat.fight()
