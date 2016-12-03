
class Player:
    VERSION = "bela"

    def betRequest(self, game_state):

        try:

            fishes = self.get_my_hand(game_state)
            pairs_in_hand = self.check_hand_for_pairs(fishes["hole_cards"])
            both_figures = self.check_hand_for_figures(fishes["hole_cards"])

            if pairs_in_hand or both_figures:
                return 10000
            else:
                return 50

        except:
            fishes = self.get_my_hand(game_state)
            pairs_in_hand = self.check_hand_for_pairs(fishes["hole_cards"])
            both_figures = self.check_hand_for_figures(fishes["hole_cards"])

            if pairs_in_hand or both_figures:
                return 10000
            else:
                return 0

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
