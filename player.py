
class Player:
    VERSION = "bela"

    def betRequest(self, game_state):

        # fishes = self.get_my_hand()
        # pairs_in_hand = self.check_hand_for_pairs(fishes["hole_cards"])
        #
        # if fishes["hole_cards"][0]["rank"] == fishes["hole_cards"][1]["rank"]:
        #     return_value = 10000
        # else:
        #     first_good = False
        #     second_good = False
        #     try:
        #         first = int(fishes["hole_cards"][0]["rank"])
        #     except:
        #         first_good = True
        #     try:
        #         second = int(fishes["hole_cards"][0]["rank"])
        #     except:
        #         second_good = True
        #     if first_good and second_good:
        #         return_value = 10000
        #     else:
        #         return_value = 0

        return 0

    def showdown(self, game_state):
        pass

    # def get_my_hand(self, game_state):
    #     all_data = game_state
    #     for player in all_data["players"]:
    #         if player["name"] == "Fishes":
    #             return player
    #
    # def check_hand_for_pairs(self, cards):
    #     return cards[0]["rank"] == cards[0]["rank"]
