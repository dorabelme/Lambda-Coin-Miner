
def handle_items(player, item):
    player.take_treasure(item)
    # If boots or jacket have been picked up and are not already being worn, wear them
    if ("boots" in item and not player.footwear) or ("jacket" in item and not player.bodywear):
        player.wear_item(item)


def move_to_location(player, path):
    for m in path:
        player.wise_explorer(m[0], m[1])
        print(f"Moving {m[0]} to room {m[1]}")
        # cooldown = response["cooldown"]
        # time.sleep(cooldown)
        # if "errors" in response:
        #     print(response["errors"])
