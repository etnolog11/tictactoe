from tkinter import *
import random

field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#TODO restrtructure code make the global values obsolete

step = 0
typeofplay = False
game_in_progress = False
cross = False


def parameter_for_best_move():
    return not ((step) % 2 == 0 and not cross)


def transpose(field):
    transposed_field = [0] * 9
    transpose_dictionary = {0: 2, 1: 5, 2: 8, 3: 1, 4: 4, 5: 7, 6: 0, 7: 3, 8: 6}
    for i in range(0, 9):
        transposed_field[transpose_dictionary[i]] = field[i]
    return transposed_field


def check_horizontal_diagonal(field):
    full_diagonal = field[0] == field[4] == field[8]
    cross_win = (full_diagonal and field[4] == 1)
    cross_lose = (full_diagonal and field[4] == 2)
    for i in range(0, 3):
        full_horizontal = field[i * 3] == field[i * 3 + 1] == field[i * 3 + 2]
        cross_win = cross_win or (full_horizontal and field[i * 3] == 1)
        cross_lose = cross_lose or (full_horizontal and field[i * 3] == 2)

    return [cross_win, cross_lose]

#TODO connect win lose and tie condition to position_eval() function instead of check() function

def position_eval(field):
    circles = 0
    crosses = 0
    blank = 0
    for square in field:
        match square:
            case 2:
                circles += 1
            case 1:
                crosses += 1
            case 0:
                blank += 1
            case _:
                raise RuntimeError("The field was improperly constructed")
    cross_win = False
    cross_lose = False
    this_transposition_check = check_horizontal_diagonal(field)
    cross_win = cross_win or this_transposition_check[0]
    cross_lose = cross_lose or this_transposition_check[1]
    this_transposition_check = check_horizontal_diagonal(transpose(field))
    cross_win = cross_win or this_transposition_check[0]
    cross_lose = cross_lose or this_transposition_check[1]
    free_spots = 9
    for i in range(0, 9):
        if (field[i] != 0):
            free_spots -= 1

    if cross_win and cross_lose:
        raise RuntimeError("invalid field state")

    if not (cross_win or cross_lose):
        if free_spots > 0:
            return 0
        else:
            return 2
    elif cross_win:
        return 3
    elif cross_lose:
        return 1
    else:
        raise ValueError("Winning state malfunction")


def best_move(field_loc, cross):
    #minmax algorithm implementation
    #TODO try alpha beta prunning
    #TODO try not calculating the symmetrical variants at least the most symmetrical ones
    global field, step
    local_field = field_loc.copy()
    #print(local_field)
    fill = 0
    match cross:  # whose time to play 1 for crosses
        case False:
            fill = 1
        case True:
            fill = 2
        case _:
            raise RuntimeError("invalid current player")

    # if endgame return result
    evaluation = position_eval(local_field)
    if evaluation != 0:
        return evaluation

    # generate valid moves
    valid_move_indexes = []
    for i in range(0, 9):
        if local_field[i] == 0:
            valid_move_indexes.append(i)
    # find the best valid move recursively
    moves_score = {}
    for i in range(0, len(valid_move_indexes)):
        new_local_field = local_field.copy()
        new_local_field[valid_move_indexes[i]] = fill
        moves_score.update([(valid_move_indexes[i], best_move(new_local_field, not cross))])

    # optimize for the needed player
    if cross:
        final_choice_position = min(moves_score, key=moves_score.get)
        final_choice_score = moves_score[final_choice_position]
    else:
        final_choice_position = max(moves_score, key=moves_score.get)
        final_choice_score = moves_score[final_choice_position]

    if local_field == field:
        field[final_choice_position] = fill
        step += 1
        draw()
        return final_choice_score
    return final_choice_score


def ai_decision():  # must draw after itself
    global field, cross, step
    aifield = field.copy()
    playerfield = field.copy()
    i = 0
    if cross:
        aishouldplace = 2
    else:
        aishouldplace = 1
    a = 0
    if cross:
        for elem in playerfield:
            if elem == 2:
                playerfield[i] = 0
            i += 1
        i = 0
        for elem in aifield:
            if elem == 1:
                aifield[i] = 0
            elif elem == 2:
                aifield[i] = 1
            i += 1


    else:
        for elem in playerfield:
            if elem == 1:
                playerfield[i] = 0
            elif elem == 2:
                playerfield[i] = 1
            i += 1
        i = 0
        for elem in aifield:
            if elem == 2:
                aifield[i] = 0
            i += 1
        i = 0
    if aifield[0] + aifield[1] == 2 and playerfield[2] != 1:
        a = 2
    elif aifield[0] + aifield[2] == 2 and playerfield[1] != 1:
        a = 1
    elif aifield[1] + aifield[2] == 2 and playerfield[0] != 1:
        a = 0
    elif aifield[3] + aifield[4] == 2 and playerfield[5] != 1:
        a = 5
    elif aifield[3] + aifield[5] == 2 and playerfield[4] != 1:
        a = 4
    elif aifield[5] + aifield[4] == 2 and playerfield[3] != 1:
        a = 3
    elif aifield[6] + aifield[7] == 2 and playerfield[8] != 1:
        a = 8
    elif aifield[6] + aifield[8] == 2 and playerfield[7] != 1:
        a = 7
    elif aifield[8] + aifield[7] == 2 and playerfield[6] != 1:
        a = 6
    elif aifield[0] + aifield[3] == 2 and playerfield[6] != 1:
        a = 6
    elif aifield[0] + aifield[6] == 2 and playerfield[3] != 1:
        a = 3
    elif aifield[3] + aifield[6] == 2 and playerfield[0] != 1:
        a = 0
    elif aifield[1] + aifield[4] == 2 and playerfield[7] != 1:
        a = 7
    elif aifield[1] + aifield[7] == 2 and playerfield[4] != 1:
        a = 4
    elif aifield[7] + aifield[4] == 2 and playerfield[1] != 1:
        a = 1
    elif aifield[2] + aifield[5] == 2 and playerfield[8] != 1:
        a = 8
    elif aifield[2] + aifield[8] == 2 and playerfield[5] != 1:
        a = 5
    elif aifield[8] + aifield[5] == 2 and playerfield[2] != 1:
        a = 2
    elif aifield[0] + aifield[4] == 2 and playerfield[8] != 1:
        a = 8
    elif aifield[0] + aifield[8] == 2 and playerfield[4] != 1:
        a = 4
    elif aifield[4] + aifield[8] == 2 and playerfield[0] != 1:
        a = 0
    elif aifield[2] + aifield[4] == 2 and playerfield[6] != 1:
        a = 6
    elif aifield[2] + aifield[6] == 2 and playerfield[4] != 1:
        a = 4
    elif aifield[6] + aifield[4] == 2 and playerfield[2] != 1:
        a = 2
    elif playerfield[0] + playerfield[1] == 2 and aifield[2] != 1:
        a = 2
    elif playerfield[0] + playerfield[2] == 2 and aifield[1] != 1:
        a = 1
    elif playerfield[1] + playerfield[2] == 2 and aifield[0] != 1:
        a = 0
    elif playerfield[3] + playerfield[4] == 2 and aifield[5] != 1:
        a = 5
    elif playerfield[3] + playerfield[5] == 2 and aifield[4] != 1:
        a = 4
    elif playerfield[5] + playerfield[4] == 2 and aifield[3] != 1:
        a = 3
    elif playerfield[6] + playerfield[7] == 2 and aifield[8] != 1:
        a = 8
    elif playerfield[6] + playerfield[8] == 2 and aifield[7] != 1:
        a = 7
    elif playerfield[8] + playerfield[7] == 2 and aifield[6] != 1:
        a = 6
    elif playerfield[0] + playerfield[3] == 2 and aifield[6] != 1:
        a = 6
    elif playerfield[0] + playerfield[6] == 2 and aifield[3] != 1:
        a = 3
    elif playerfield[3] + playerfield[6] == 2 and aifield[0] != 1:
        a = 0
    elif playerfield[1] + playerfield[4] == 2 and aifield[7] != 1:
        a = 7
    elif playerfield[1] + playerfield[7] == 2 and aifield[4] != 1:
        a = 4
    elif playerfield[7] + playerfield[4] == 2 and aifield[1] != 1:
        a = 1
    elif playerfield[2] + playerfield[5] == 2 and aifield[8] != 1:
        a = 8
    elif playerfield[2] + playerfield[8] == 2 and aifield[5] != 1:
        a = 5
    elif playerfield[8] + playerfield[5] == 2 and aifield[2] != 1:
        a = 2
    elif playerfield[0] + playerfield[4] == 2 and aifield[8] != 1:
        a = 8
    elif playerfield[0] + playerfield[8] == 2 and aifield[4] != 1:
        a = 4
    elif playerfield[4] + playerfield[8] == 2 and aifield[0] != 1:
        a = 0
    elif playerfield[2] + playerfield[4] == 2 and aifield[6] != 1:
        a = 6
    elif playerfield[2] + playerfield[6] == 2 and aifield[4] != 1:
        a = 4
    elif playerfield[6] + playerfield[4] == 2 and aifield[2] != 1:
        a = 2
    else:
        while 1:
            a = random.randint(0, 8)
            if field[a] == 0:
                break
    field[a] = aishouldplace
    step += 1
    draw()

#TODO either make draw function reset the field or draw only the new elements
def draw():
    i = 0
    global typeofplay
    #print("I drew" + str(field))
    for tile in field:
        if tile == 1:
            canvas.create_line(133 * (i % 3), (i // 3) * 133, 133 * (i % 3 + 1), (i // 3 + 1) * 133, fill="#ffffff"
                               , tags='transient')
            canvas.create_line(133 * (i % 3), (i // 3 + 1) * 133, 133 * (i % 3 + 1), (i // 3) * 133, fill="#ffffff"
                               , tags='transient')
        elif tile == 2:
            canvas.create_oval(133 * (i % 3), (i // 3) * 133, 133 * (i % 3 + 1), (i // 3 + 1) * 133, outline="#ffffff"
                               , tags='transient')
        i += 1
    if check(field) != 0:
        global game_in_progress
        a.config(fg="#ffffff")
        frame.place(x=401, y=0)
        frame.config(highlightbackground="#ffffff")
        game_in_progress = False
    if check(field) == 0:
        pass
    elif check(field) == 1:
        a.config(text="Crosses have won")
        a.place(x=200, y=25, anchor=CENTER)

    elif check(field) == 2:
        a.config(text="Circles have won")
        a.place(x=200, y=25, anchor=CENTER)
    elif check(field) == 3:
        a.config(text="It's a tie")
        a.place(x=200, y=25, anchor=CENTER)


def sologameset():
    global typeofplay, game_in_progress, quest, frame_for_quest, antiai, proai
    antiai.place_forget()
    proai.place_forget()
    quest.config(text="")
    frame_for_quest.config(highlightbackground="#000000")
    typeofplay = False
    game_in_progress = True

# TODO make this abomination of three function be one function
def cross_handler():
    global proai, antiai, quest, frame_for_quest, cross, game_in_progress
    proai.place_forget()
    antiai.place_forget()
    quest.place_forget()
    frame_for_quest.place_forget()
    cross = True
    game_in_progress = True


def circles_handler():
    global proai, antiai, quest, frame_for_quest, cross, game_in_progress
    proai.place_forget()
    antiai.place_forget()
    quest.place_forget()
    frame_for_quest.place_forget()
    cross = False
    game_in_progress = True
    # ai_decision()
    best_move(field, parameter_for_best_move())


def cross_or_circle():
    global proai, antiai, quest, typeofplay
    typeofplay = True
    quest.configure(text="What is your figure?")
    proai.configure(text="Crosses", command=cross_handler)
    antiai.configure(text="Circles", command=circles_handler)


def check(a):
    state = 0
    if ((a[0] == 1 and a[1] == 1 and a[2] == 1) or (a[3] == 1 and a[4] == 1 and a[5] == 1) or (
            a[6] == 1 and a[7] == 1 and a[8] == 1)) or \
            ((a[0] == 1 and a[3] == 1 and a[6] == 1) or (a[1] == 1 and a[4] == 1 and a[7] == 1) or (
                    a[2] == 1 and a[5] == 1 and a[8] == 1)) or \
            ((a[0] == 1 and a[4] == 1 and a[8] == 1) or (a[2] == 1 and a[4] == 1 and a[6] == 1)):
        state = 1
    elif ((a[0] == 2 and a[1] == 2 and a[2] == 2) or (a[3] == 2 and a[4] == 2 and a[5] == 2) or (
            a[6] == 2 and a[7] == 2 and a[8] == 2)) or \
            ((a[0] == 2 and a[3] == 2 and a[6] == 2) or (a[1] == 2 and a[4] == 2 and a[7] == 2) or (
                    a[2] == 2 and a[5] == 2 and a[8] == 2)) or \
            ((a[0] == 2 and a[4] == 2 and a[8] == 2) or (a[2] == 2 and a[4] == 2 and a[6] == 2)):
        state = 2
    elif a[0] != 0 and a[1] != 0 and a[2] != 0 and a[3] != 0 and a[4] != 0 and a[5] != 0 and a[6] != 0 and a[7] != 0 and \
            a[8] != 0:
        state = 3
    return state


def logic(num):
    global field, game_in_progress, typeofplay, cross, step
    if field[num] == 0:
        if game_in_progress:
            if not typeofplay:  # game with friend
                if step % 2 == 0:
                    field[num] = 1
                else:
                    field[num] = 2
                draw()
                step += 1
            else: #game with AI
                    if cross:
                        field[num] = 1
                    else:
                        field[num] = 2
                    draw()
                    step += 1
                    if check(field) == 0:
                        best_move(field, parameter_for_best_move())


def restart_game():
    global a, quest, frame, game_in_progress, field, step, quest, frame_for_quest, antiai, proai, canvas, typeofplay, cross
    canvas.delete("transient")
    typeofplay = False
    cross = False
    step = 0
    game_in_progress = False
    field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    frame_for_quest.config(highlightbackground="#ffffff")
    frame_for_quest.place(x=401, y=0)
    quest.place(x=200, y=25, anchor=CENTER)
    quest.config(text="How do you want to play?", fg="#ffffff")
    a.config(fg="#000000")
    frame.config(highlightbackground="#000000")
    frame.place_forget()
    antiai.configure(text="Local", command=sologameset)
    antiai.place(x=400, y=50)
    proai.configure(text="With AI", command=cross_or_circle)
    proai.place(x=600, y=50)


def coords_of_click(event):
    x = 0
    y = 0
    if event.x < 400:
        if event.x > 267:
            x = 2
        elif event.x > 133:
            x = 1
        if event.y > 267:
            y = 2
        elif event.y > 133:
            y = 1
        num = x + y * 3
        logic(num)

#TODO if __name__ == main please
# basic graphic setup
root = Tk()
root.title("TicTacToe")
root.resizable(False, False)
root.geometry("800x400")
root.update()
canvas = Canvas(root, bg="#000000", height=400, width=800)
canvas.pack()
canvas.pack_propagate()
canvas.create_line(400, 0, 400, 400, fill="#ffffff")
canvas.create_line(0, 133, 400, 133, fill="#ffffff")
canvas.create_line(0, 267, 400, 267, fill="#ffffff")
canvas.create_line(133, 0, 133, 400, fill="#ffffff")
canvas.create_line(267, 0, 267, 400, fill="#ffffff")
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - root_width) // 2
y = (screen_height - root_height) // 2
root.geometry(f"{root_width}x{root_height}+{x}+{y}")
# permanent buttons and some things for end of the game
antiai = Button(root, bg="#000000", fg="#ffffff", font=("Courier", 20), bd=1, width=12)
proai = Button(root, text="With AI", bg="#000000", fg="#ffffff", font=("Courier", 20), bd=1, width=12)
frame_for_quest = Frame(canvas, bg="#000000", height=50, width=397, highlightthickness=1)
quest = Label(frame_for_quest, font=("Courier", 20), bg='#000000', fg="#ffffff", anchor=CENTER,
              height=1, width=24)
frame = Frame(canvas, bg="#000000", height=50, width=397, highlightthickness=1)
a = Label(frame, font=("Courier", 20), bg='#000000', fg="#ffffff", anchor=CENTER,
          height=1, width=20)
restart_game()  # basically start of the game
exit = Button(root, text="Exit", bg="#000000", fg="#ffffff", font=("Courier", 20), command=root.destroy, bd=1,
              width=25).place(x=400, y=350)
restart = Button(root, text="Restart", bg="#000000", fg="#ffffff", font=("Courier", 20), bd=1, command=restart_game,
                 width=25).place(x=400, y=299)

canvas.bind("<1>", coords_of_click)
root.mainloop()
