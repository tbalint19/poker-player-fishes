
class Player:
    VERSION = "bela"

    def betRequest(self, game_state):
        all_data = game_state
        for player in all_data["players"]:
            if player["name"] == "Fishes":
                fishes = player

        if fishes["hole_cards"][0]["rank"] == fishes["hole_cards"][1]["rank"]:
            return_value = 10000
        else:
            return_value = 0

        return return_value

    def showdown(self, game_state):
        pass
