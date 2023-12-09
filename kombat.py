import json
import sys

# diccionario con los movimientos y patadas
MOVES_DIC = {
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

class Fighter:
  def __init__(self, name, moves_punches, energy=6):
    self.name = name
    self.moves_punches = moves_punches
    self.energy = energy

  def attack(self):
    moves = list()
    is_special_action = False

    # obtiene la primera tupla
    move, punch = self.moves_punches.pop(0)

    # Al iniciar se valida la combinación de ataques (special_action) y se obtien el daño (damage)
    damage, special_action = 0, ''
    taladoken, remuyuken = '', ''

    if move and punch:
      # para los Taladoken se tiene una combinación de 3 movimientos más un golpe P
      taladoken = move[-3:] + punch
      damage, special_action = MOVES_DIC.get(taladoken, (0, ''))

      # para los Remuyuken tienen una combinación de 2 movimientos más un golpe K
      if not (special_action and damage):
        remuyuken = move[-2:] + punch
        damage, special_action = MOVES_DIC.get(remuyuken, (0, ''))

      if special_action and damage:
        punch = ''
        is_special_action = True
        spaces = min(len(taladoken), len(remuyuken)) if remuyuken else len(taladoken)
        move = move.replace(move[-(spaces - 1):], '')

    damage, _ = MOVES_DIC.get(punch, (damage, ''))
    moves.extend(list(move))

    # print(
    #   f'damage: {damage}, is special: {is_special_action}, action: {special_action}, extra moves: {moves}'
    # )

    # se detalla narrativa
    narrativa = ''

    if moves:
      narrativa = 'se mueve ágilmente'

    if not is_special_action:
      if moves and not punch:
        narrativa = 'hace algunos movimientos exóticos sin ningún daño... ({} se ríe)'
      if not moves and punch:
        narrativa = 'se queda quieto'
      if punch:
        _, action = MOVES_DIC.get(punch, ())
        narrativa += (f' y le pega su {action}' if narrativa else f'le pega su {action}')

    if is_special_action:
        narrativa += (f' y {special_action}' if narrativa else special_action)

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
      if (opponent.moves_punches):
        tmp = attacker
        attacker = opponent
        opponent = tmp

      # si ya no quedan movimientos, se termina el combate
      # el ganador será el que tienen más energía
      if (not attacker.moves_punches):
        print('\nNo hubo Fatality pero hay ganador!')
        print(f'{attacker.name} gana la pelea con {attacker.energy} de energía.')
        print(f'El probre {opponent.name} quedó con algo de energía: {opponent.energy}\n')
        break

def init(data_file):
  with open(data_file, 'r') as file:
    data = json.load(file)

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

if __name__ == '__main__':
  # verificar que se pasa como argumento el archivo json
  if len(sys.argv) != 2:
    print('USO: python kombat.py {kombat_data}.json\n')
    print('donde {kombat_data}: archivo json que contiene los jugadores y sus movimientos\n')
  else:
    # inicializa enviando los datos
    init(sys.argv[1])
