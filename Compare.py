from pygbx import *
import difflib
from tkinter import *
import re

WIDTH = 500
HEIGHT = 100


def findMatches(baseReplay, replay):
    """Returns timestamps during which both replays are identical
    baseReplay : link to the base replay. Timestamps are corresponding to his inputs
    replay : link to the other replay for comparison"""
    baseInputs = toInputs(baseReplay)
    inputs = toInputs(replay)
    timeStamps = set()
    for (start, end) in matchIndexes(baseInputs, inputs):
        timeStamps.add((baseInputs[start][0], baseInputs[end][0]))
    return timeStamps


def matchIndexes(_list1, _list2):
    """Returns a generator of indexes corresponding to similar parts for _list1 and _list2
    _list1 : main list, indexes are corresponding to its structure
    _list2 : other list to compare"""
    list1 = [(_list1[i + 1][0] - _list1[i][0], _list1[i][1:], _list1[i + 1][1:]) for i in range(len(_list1) - 1)]
    list2 = [(_list2[i + 1][0] - _list2[i][0], _list2[i][1:], _list2[i + 1][1:]) for i in range(len(_list2) - 1)]
    while True:
        mbs = difflib.SequenceMatcher(None, list1, list2).get_matching_blocks()
        if len(mbs) == 1:
            break
        for i, j, n in mbs[::-1]:
            if n > 0:
                yield i, i + n
            del list1[i: i + n]
            del list2[j: j + n]


def toInputs(link):
    """Returns inputList of a replay, for further analysis
    link : link to the file of the replay"""
    g = Gbx(link)
    ghost = g.get_class_by_id(GbxType.CTN_GHOST)
    inputList = []
    isTAS = False
    for i in ghost.control_entries:
        if i.event_name in ('Steer', 'SteerRight', 'SteerLeft', 'Accelerate', 'Brake', 'Respawn'):
            if isTAS:
                inputList.append((i.time - 65535, i.event_name, i.enabled, i.flags))
            else:
                inputList.append((i.time, i.event_name, i.enabled, i.flags))
        elif i.event_name == '_FakeIsRaceRunning':
            isTAS = i.time != 0
    return inputList


def getNickname(link):
    """Returns the readable nickname from a replay
    link: link to the replay you want to extract name"""
    g = Gbx(link)
    ghost = g.get_classes_by_ids([GbxType.REPLAY_RECORD_OLD, GbxType.REPLAY_RECORD])[0]
    nick = re.sub(r'\$[0-9A-Fa-f]{3}', '', ghost.nickname)
    nicke = re.sub(r'\$.', '', nick)
    return nicke


def getMapName(link):
    """Returns the map name of a replay
    link : link to the replay you want to extract map name"""
    g = Gbx(link)
    record = g.get_classes_by_ids([GbxType.REPLAY_RECORD_OLD, GbxType.REPLAY_RECORD])[0]
    return record.track.get_classes_by_ids([GbxType.CHALLENGE, GbxType.CHALLENGE_OLD])[0].map_name


def getFinishTime(link):
    """Returns the finish time of a replay
    link : link to the replay you want to extract finish time"""
    g = Gbx(link)
    ghost = g.get_class_by_id(GbxType.CTN_GHOST)
    return ghost.race_time


def drawIndexes(dataset, replay):
    """Draws the comparison between inputs
    dataset : list of replay links to compare against
    replay : link to the replay you want to introduce into the dataset"""
    root = Tk()
    canvas = Canvas(root, width=WIDTH, height=HEIGHT * 2)
    canvas.create_text(WIDTH * 0.5, 5 / 3 * HEIGHT, fill='black', text=getMapName(replay))
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='black')
    canvas.create_text(WIDTH / (2 * len(dataset) + 2), 4 / 3 * HEIGHT, fill='black', text=getNickname(replay))
    colors = ["red", "green", "blue", "yellow"]
    for idx, rep in enumerate(dataset):
        canvas.create_text(WIDTH * (1.5 + idx) / (len(dataset) + 1), 4 / 3 * HEIGHT, fill=colors[idx],
                           text=getNickname(rep))
        timeStamps = findMatches(replay, rep)
        for (i, j) in timeStamps:
            scale = WIDTH / getFinishTime(replay)
            canvas.create_rectangle(i * scale, 0, max(j * scale, i * scale + 10), HEIGHT, fill=colors[idx])
    canvas.pack()
    mainloop()


trabadia = "C:\\Users\\User\\Documents\\TmForever\\Tracks\\Replays\\FromWeb\\A01 Race-trabadia-23.83.Gbx"
tasbadia = "C:\\Users\\User\\Documents\\TmForever\\Tracks\\Replays\\CreatedGhosts\\A01-Race 23.75 trabadia.Replay.Gbx"

delete_club = "C:\\Users\\User\\Downloads\\C12-Obstacle_DELETE_CLUB002872.Replay.Gbx"
mehh = "C:\\Users\\User\\Documents\\TmForever\\Tracks\\Replays\\FromWeb\\C12 Obstacle-Mehh-29.75.Gbx"
solution = "C:\\Users\\User\\Documents\\TmForever\\Tracks\\Replays\\FromWeb\\C12 Obstacle-Solution-29.33.Gbx"

delete_club_c4 = "C:\\Users\\User\\Downloads\\StarSnowC4_DELETE_CLUB003113.Replay.Gbx"
frev = "C:\\Users\\User\\Downloads\\StarSnowC4_«__»_frev.____(00'33''31).Replay.Gbx"
roa = "C:\\Users\\User\\Downloads\\StarSnowC4_[CMC]Roa(00'32''56).Replay.Gbx"

drawIndexes([mehh, solution], delete_club)
# drawIndexes([trabadia], tasbadia)
