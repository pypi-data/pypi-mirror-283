import json
from halerium_utilities.collab import CollabBoard
from halerium_utilities.prompt.agents import call_agent
from .template_analyzer_utils import format_json_to_graph, is_execute_and_show, is_execute_only


def snippet_sequence(board_path: str):
    board = CollabBoard(board_path, pull_on_init = True)
    board_json = board.to_json()
    board_dict = json.loads(board_json)
    
    g = format_json_to_graph(board_dict)

    #topological sort
    ids, names = g.topologicalSort()
    return ids, names

def execute_botcard(card_id:str, board_path:str):
    board = CollabBoard(board_path, pull_on_init=True)
    board_json = board.to_json()
    board_dict = json.loads(board_json)
    #get card from id
    gen = call_agent(board_dict, card_id, parse_data=True)
    result = ""
    for data in gen:
        if data.event == "chunk":
            result += data.data["chunk"]

    board.update_card({'id':card_id, 'type_specific':{'prompt_output':result}})
    board.push()
    return result

def analyze_snippet(board_path:str):
    ids, types = snippet_sequence(board_path)
    ids_and_answers = {}
    for card_id, type in zip(ids, types):
        if type == 'bot':
            if is_execute_and_show(card_id, board_path): #card in a red frame
                answer = execute_botcard(card_id, board_path)
                ids_and_answers[card_id] = answer
            elif is_execute_only(card_id, board_path): #card in a yellow frame
                execute_botcard(card_id, board_path)
            else:
                pass
        else:
            pass
    return ids_and_answers




if __name__ == "__main__":
    answers = analyze_snippet("testboard.board")
    print(answers)
