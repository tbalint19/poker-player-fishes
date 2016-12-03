gamestate = {
    "tournament_id":"550d1d68cd7bd10003000003",     # Id of the current tournament

    "game_id":"550da1cb2d909006e90004b1",           # Id of the current sit'n'go game. You can use this to link a
                                                    # sequence of game states together for logging purposes, or to
                                                    # make sure that the same strategy is played for an entire game

    "round":0,                                      # Index of the current round within a sit'n'go

    "bet_index":0,                                  # Index of the betting opportunity within a round

    "small_blind": 10,                              # The small blind in the current round. The big blind is twice the
                                                    #     small blind

    "current_buy_in": 80,                          # The amount of the largest current bet from any one player

    "pot": 400,                                     # The size of the pot (sum of the player bets)

    "minimum_raise": 240,                           # Minimum raise amount. To raise you have to return at least:
                                                    #     current_buy_in - players[in_action][bet] + minimum_raise

    "dealer": 1,                                    # The index of the player on the dealer button in this round
                                                    #     The first player is (dealer+1)%(players.length)

    "orbits": 7,                                    # Number of orbits completed. (The number of times the dealer
                                                    #     button returned to the same player.)

    "in_action": 1,                                 # The index of your player, in the players array

    "players": [                                    # An array of the players. The order stays the same during the
        {                                           #     entire tournament

            "id": 0,                                # Id of the player (same as the index)

            "name": "Albert",                       # Name specified in the tournament config

            "status": "active",                     # Status of the player:
                                                    #   - active: the player can make bets, and win the current pot
                                                    #   - folded: the player folded, and gave up interest in
                                                    #       the current pot. They can return in the next round.
                                                    #   - out: the player lost all chips, and is out of this sit'n'go

            "version": "Default random player",     # Version identifier returned by the player

            "stack": 1010,                          # Amount of chips still available for the player. (Not including
                                                    #     the chips the player bet in this round.)

            "bet": 0                              # The amount of chips the player put into the pot
        },
        {
            "id": 1,                                # Your own player looks similar, with one extension.
            "name": "Fishes",
            "status": "active",
            "version": "Default random player",
            "stack": 1590,
            "bet": 80,
            "hole_cards": [                         # The cards of the player. This is only visible for your own player
                                                    #     except after showdown, when cards revealed are also included.
                {
                    "rank": "A",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                    "suit": "hearts"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                },
                {
                    "rank": "A",
                    "suit": "spades"
                }
            ]
        },
        {
            "id": 2,
            "name": "Chuck",
            "status": "out",
            "version": "Default random player",
            "stack": 0,
            "bet": 0
        }
    ],
    "community_cards": [                            # Finally the array of community cards.
        {
            "rank": "10",
            "suit": "spades"
        },
        {
            "rank": "10",
            "suit": "hearts"
        },
        {
            "rank": "10",
            "suit": "clubs"
        }
    ]
}


class Board:

    def check_one_pair(self):
        ranks = []
        for card in self.cards:
            ranks.append(card[0])

        ranks = set(ranks)
        if len(ranks) == 4:
            return True

        return False

    def check_two_pairs(self):
        ranks = []
        for card in self.cards:
            ranks.append(card[0])

        ranks = set(ranks)
        if len(ranks) == 3:
            return True

        return False

    def check_set(self):
        ranks = []
        for card in self.cards:
            ranks.append(card[0])

        for rank in ranks:
            if ranks.count(rank) == 3:
                return True

        return False

    def check_poker(self):
        ranks = []
        for card in self.cards:
            ranks.append(card[0])

        for rank in ranks:
            if ranks.count(rank) == 4:
                return True

        return False

    def check_top_pair(self, game_state, player_data):
        community_cards = [i['rank'] if i['rank'] != "10" else "T" for i in game_state['community_cards']]
        own_cards = [i['rank'] if i['rank'] != "10" else "T" for i in player_data['hole_cards']]




    def get_hand_rank(self, gamestate, player_data):
        if self.check_poker():
            return "Poker"
        if self.check_set():
            return "Set"
        if self.check_two_pairs():
            return "Two pairs"
        if self.check_top_pair(gamestate, player_data):
            return "Top pair"
        if self.check_one_pair():
            return 'One pair'


    def update_cards(self, game_state, player_data):
        cards = []
        community_cards = [i['rank']  + i['suit'][0] if i['rank'] != "10" else "T" + i['suit'][0] for i in game_state['community_cards']]
        own_cards = [i['rank']  + i['suit'][0] if i['rank'] != "10" else "T" + i['suit'][0] for i in player_data['hole_cards']]
        for card in community_cards:
            cards.append(card)
        for card in own_cards:
            cards.append(card)
        self.cards = cards

    def update_status(self, game_state):
        if(len(game_state['community_cards']) == 0):
            self.status = 'preflop'
        elif (len(game_state['community_cards']) == 3):
            self.status = 'flop'
        elif (len(game_state['community_cards']) == 4):
            self.status = 'turn'
        elif (len(game_state['community_cards']) == 5):
            self.status = 'river'

        self.current_buy_in = int(game_state['current_buy_in'])

        self.small_blind = int(game_state['small_blind'])

    def update_action(self, game_state):
        bets = []
        for player in game_state['players']:
            if player['bet'] > game_state['small_blind'] * 2:
                bets.append(int(player['bet']))
        bets = set(bets)
        if len(bets) == 0:
            self.action = 'no_bet'
        elif len(bets) == 1:
            self.action = 'bet'
        else:
            self.action = 'raise'

    def format_cards(self):
        suits = []
        suit = 'o'
        cards = []
        for card in self.player_data['hole_cards']:
            if card['rank'] == '10':
                rank = 'T'
            else:
                rank = card['rank']
            suits.append(card['suit'])
            cards.append(rank)

        if suits[0] == suits[1]:
            suit = 's'
        self.own_cards = "".join(cards)



class Player:
    VERSION = "bela"
    top_1 = ['AAo', 'KKo', 'AKo', 'AKs', 'QQo', 'JJo', 'TTo', 'AQs', 'AJs', 'AQo', 'KQs', 'ATs', '99o', '88o', '77o']
    top_2 = [
        'AAo', 'KKo', 'AKo', 'AKs', 'QQo', 'JJo', 'TTo', 'AQs', 'AQo', 'AJo', 'KQo', 'KQs', 'KJs', 'QJs',
        'ATs', '99o', '88o', '77o', 'AJs'
    ]
    top_3 = [
        'AAo', 'KKo', 'AKo', 'AKs', 'QQo', 'JJo', 'TTo', 'AQs', 'AQo', 'AJo', 'KQo', 'KQs', 'KJs', 'QJs', 'ATs',
        '99o', '88o', '77o', '66o', '55o', '44o', '33o', '22o', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s',
        'A2s', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'QTs', 'Q9s', 'Q8s', 'JTs', 'J9s', 'T9s', 'ATo', 'A9o', 'A8o',
        'KJo', 'KTo', 'K9o', 'QJo', 'QTo', 'JTo', 'AJs'
    ]

    def __init__(self):
        self.board = Board()

    # Finds player data
    def find_player(self, game_state):
        for player in game_state["players"]:
            if player["name"] == "Fishes":
                self.player_data = player

    # Formats our cards into a desired format, example: 'AKs' - meaning ace, king, offsuite (not the same color)
    def format_own_cards(self):
        suits = []
        suit = 'o'
        cards = []
        for card in self.player_data['hole_cards']:
            if card['rank'] == '10':
                rank = 'T'
            else:
                rank = card['rank']
            suits.append(card['suit'])
            cards.append(rank)

        if suits[0] == suits[1]:
            suit = 's'
        self.own_cards = "".join(cards) + suit

    # Checks if our cards are in top5%
    def check_top1(self):
        altered_cards = self.own_cards[1] + self.own_cards[0] + self.own_cards[2]
        return self.own_cards in self.top_1 or altered_cards in self.top_1

    def check_top2(self):
        altered_cards = self.own_cards[1] + self.own_cards[0] + self.own_cards[2]
        return self.own_cards in self.top_2 or altered_cards in self.top_2

    def check_top3(self):
        altered_cards = self.own_cards[1] + self.own_cards[0] + self.own_cards[2]
        return self.own_cards in self.top_3 or altered_cards in self.top_3

    def reraise(self):
        return self.board.current_buy_in * 3

    def bet(self):
        return self.board.small_blind * 8

    def call(self):
        return self.board.current_buy_in

    def check(self):
        return 0

    def fold(self):
        return 0

    def all_in(self):
        return self.stack

    def betRequest(self, game_state):
        self.find_player(game_state)
        self.format_own_cards()

        self.stack = self.player_data['stack']
        self.board.update_status(game_state)
        self.board.update_action(game_state)
        self.board.update_cards(game_state, self.player_data)
        print("hand_rank")
        hand_rank = self.board.get_hand_rank(game_state, self.player_data)

        if self.board.status == 'preflop':
            if self.check_top1():
                if self.board.action == 'no_bet':
                    return self.bet()
                if self.board.action == 'bet':
                    return self.reraise()
                if self.board.action == 'raise':
                    return self.all_in()

            elif self.check_top2():
                if self.board.action == 'no_bet':
                    return self.bet()
                if self.board.action == 'bet':
                    return self.reraise()
                if self.board.action == 'raise':
                    return self.fold()

            elif self.check_top3():
                if self.board.action == 'no_bet':
                    return self.bet()
                if self.board.action == 'bet':
                    return self.call()
                if self.board.action == 'raise':
                    return self.fold()

            else:
                return 0


        else:
            if hand_rank == "Set":
                if self.board.action == 'no_bet':
                    return self.bet()
                if self.board.action == 'bet':
                    return self.reraise()
                if self.board.action == 'raise':
                    return self.all_in()
            elif hand_rank == "Two pairs" or hand_rank == "Top pair":
                if self.board.action == 'no_bet':
                    return self.bet()
                if self.board.action == 'bet':
                    return self.reraise()
                if self.board.action == 'raise':
                    return self.all_in()
            elif hand_rank == "One pair":
                if self.check_top1():
                    if self.board.action == 'no_bet':
                        return self.bet()
                    if self.board.action == 'bet':
                        return self.reraise()
                    if self.board.action == 'raise':
                        return self.call()
                else:
                    if self.board.action == 'no_bet':
                        return self.bet()
                    if self.board.action == 'bet':
                        return self.fold()
                    if self.board.action == 'raise':
                        return self.fold()
            else:
                if self.board.action == 'no_bet':
                    return self.check()
                if self.board.action == 'bet':
                    return self.fold()
                if self.board.action == 'raise':
                    return self.fold()


    def showdown(self, game_state):
        pass


    def get_my_hand(self, game_state):
        all_data = game_state
        for player in all_data["players"]:
            if player["name"] == "Fishes":
                return player


    def check_hand_for_pairs(self, cards):
        return cards[0]["rank"] == cards[1]["rank"]


    def check_hand_for_figures(self, cards):
        first_good = False
        second_good = False
        try:
            first = int(cards[0]["rank"])
        except:
            first_good = True
        try:
            second = int(cards[1]["rank"])
        except:
            second_good = True
        return first_good and second_good

player = Player()
print(player.betRequest(gamestate))
