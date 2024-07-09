from halerium_utilities.collab import CollabBoard
from halerium_utilities.board import BoardNavigator
from halerium_utilities.prompt.agents import call_agent


def execute_botcard(collab_board: CollabBoard, card_id: str):
    #get card from id
    gen = call_agent(collab_board.to_dict(), card_id, parse_data=True)
    result = ""
    for data in gen:
        if data.event == "chunk":
            result += data.data["chunk"]

    collab_board.update_card({'id': card_id, 'type_specific': {'prompt_output': result}})
    collab_board.push()
    return result


def analyze_snippet(board_path: str):
    collab_board = CollabBoard(board_path, pull_on_init=True)
    navigator = BoardNavigator(collab_board)
    execution_order = navigator.get_execution_order(
        navigator.cards, keep_only_executable=True)

    ids_and_answers = {}
    for card_id in execution_order:
        if is_execute_and_show(navigator, card_id):  # card in a red frame
            answer = execute_botcard(collab_board, card_id)
            ids_and_answers[card_id] = answer
        elif is_execute_only(navigator, card_id):  # card in a yellow frame
            execute_botcard(collab_board, card_id)
        else:
            pass

    return ids_and_answers


def is_in_colored_frame(navigator, card_id, color_name):
    containing_frames = navigator.get_containing_frame_ids(card_id)
    for frame_id in containing_frames:
        frame_color = getattr(navigator.cards[frame_id].type_specific, "color", None)
        if frame_color == color_name:
            return True

    return False


COLORS = {
    "yellow": "note-color-8",  # is_execute_and_show
    "blue": "note-color-4",  # is_execute_only
    "red": "note-color-6",  # don't care
}


def is_execute_and_show(navigator, card_id):
    return is_in_colored_frame(navigator, card_id, COLORS["yellow"])


def is_execute_only(navigator, card_id):
    return is_in_colored_frame(navigator, card_id, COLORS["blue"])
