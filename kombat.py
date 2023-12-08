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

    moves_dic = {
      'DSDP': (3, 'Taladoken'),
      'ASAP': (2, 'Taladoken'),
      'SAK': (3, 'Remuyuken'),
      'SDK': (2, 'Remuyuken'),

      'P': (1, 'Puño'),
      'K': (1, 'Patada'),

      'W': (0, 'Arriba'),
      'S': (0, 'Izquierda'),
      'A': (0, 'Abajo'),
      'D': (0, 'Derecha'),
    }

    # Al iniciar se valida la combinación de ataques (special_action)
    # para los Taladoken se tiene una combinación de 3 movimientos más un golpe P
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
        moves.extend(list(move))
      else:
        moves.extend(list(move.replace(move[-2:], '')))  # ??? validar

    else:
      moves.extend(list(move.replace(move[-3:], '')))  # ??? validar

    # se agrega el punch a los movimientos extra solo si no se ha utilizado en un movimiento especial
    if (not is_special_action and len(punch) > 0):
      moves.append(punch)

    # print(
    #     f'damage: {damage}, action: {special_action}, extra moves: {moves}')

    damages = damage
    actions = list()

    for m in moves:
      damage, action = moves_dic.get(m, (0, 'se queda quieto'))

      damages += damage
      actions.append(action)

    return damages, ', '.join(actions) + ', ' + special_action

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

      # narra lo acontecido --> por mejorar
      print(f'{attacker.name} {action}')

      # fatality
      if opponent.energy <= 0:
        print(
          f'\nFATALITY!: {attacker.name} gana la pelea y aún le queda(n) {attacker.energy} de energía\n'
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
        print(f'\nNo hubo Fatality pero hay ganador! {attacker.name} gana la pelea con {attacker.energy} de energía.')
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
