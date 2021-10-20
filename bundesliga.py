import win32com.client  # первым делом импортируем из предустановленной заранее библеотеки pywin32 нужный модуль
import os  # импортируем модуль из встроенной библеотеки для легкого обозначения пути к фалу на любом копмьютере
import string

# Для удобства уточню, что изначально использовал немецкую бундеслигу, и все строил на ней, но опустил некоторые правила, до котрых
# не доходит в обычных матчах, чтоб можно было использовать францию как страну с условно такими же правилами.
# Какое имеено правило я опустил, написано в прикрепленном файле по бундеслиге.


def get_input(filename): 
    excel = win32com.client.Dispatch("Excel.Application") 
    filepath = os.getcwd()
    wb = excel.Workbooks.Open(os.path.join(filepath, filename))
    sheet = wb.ActiveSheet
    values = [r[0].value for r in sheet.Range("A1:A225")]
    list_input = []
    for elem in values:
        list_input.append(elem.split(','))
    return list_input


def get_teams(list_input):
    teams = []
    for n in list_input:
        if list_input.index(n) > 1:
            for r in n:
                if r.startswith((tuple(string.ascii_uppercase))) and len(r) > 2:
                    if r not in teams:
                        teams.append(r)
    return teams


def get_rating(teams, list_input): # заметил, что питон начинает багать при большом количестве параллельных
    rating = []      # циклов в одной ф-ции, поэтому старался делать максимально вохможное разбиение
    for j in teams:
        team_rate = []
        games_played = 0
        win = 0
        draw = 0
        goal_scored = 0
        rate = 0
        goal_diff = 0
        for l in list_input:
            if j in l:
                if l.index(j) == 3:
                    games_played += 1
                    goal_scored += int(l[5])
                    goal_diff += int(l[5]) - int(l[6])
                    if l[7] == 'H':
                        win += 1
                        rate += 3
                if l[7] == 'D':
                    draw += 1
                    rate += 1
                if l.index(j) == 4:
                    games_played += 1
                    goal_scored += int(l[6])
                    goal_diff += int(l[6]) - int(l[5])
                    if l[7] == 'A':
                        win += 1
                        rate += 3
                lose = games_played - (win + draw)
                team_rate = [rate, goal_diff, goal_scored, j, games_played, win, draw, lose]
        rating.append(team_rate)
        rating.sort()
        rating.reverse()
    return rating


def get_samescored_teams(rating):
    samescored_teams = []
    for elem in rating:
        samescored_teams_local = [elem[3]]
        for elem_2 in rating:
            if elem[0] == elem_2[0] and elem_2[3] not in samescored_teams_local:
                samescored_teams_local.append(elem_2[3])
                samescored_teams_local.sort()
        if len(samescored_teams_local) != 1:
            samescored_teams.append(samescored_teams_local)
    for teams_list in samescored_teams:
        if samescored_teams.count(teams_list) > 1:
            samescored_teams.remove(teams_list)
    return samescored_teams


def get_local_rating(samescored_teams, list_input):  # пришлось долго возиться, чтоб додуматься, что
    local_rating = []       # для 3 и более команд с одинаковыми очками легче всего просто провести свой мини-турнир
    for j in samescored_teams:
        list_input_modified = []
        for elem in j:
            for elem_2 in list_input:
                if len(set(j) & set(elem_2)) >= 2 and elem_2 not in list_input_modified:
                    list_input_modified.append(elem_2)
            if len(list_input_modified) >= 1:
                team_rate = []
                goal_scored = 0
                rate = 0
                goal_diff = 0
                for l in list_input_modified:
                    if elem in l:
                        if l.index(elem) == 3:
                            goal_scored += int(l[5])
                            goal_diff += int(l[5]) - int(l[6])
                            if l[7] == 'H':
                                rate += 3
                        if l[7] == 'D':
                            rate += 1
                        if l.index(elem) == 4:
                            goal_scored += int(l[6])
                            goal_diff += int(l[6]) - int(l[5])
                            if l[7] == 'A':
                                rate += 3
                        team_rate = [rate, goal_diff, goal_scored, elem]
                local_rating.append(team_rate)
                local_rating.sort()
                local_rating.reverse()
    return local_rating


def get_final_rating(rating, local_rating):
    for elem in local_rating:
        for elem_2 in rating:
            if elem[3] == elem_2[3]:
                elem_2.extend(elem)
                if elem_2 in rating:
                    break
                rating.pop(rating.index(elem_2))
                rating.append(elem_2)
    rating_final = []
    for i in rating:
        if len(i) >= 11:
            i.remove(i[3])
        rating_final.append(i)
    return rating_final


def get_sorted_final_rating(rating_final, list_input):  # вынес сортировку в отдельную ф-цию для того, чтобы вписать
    for insides in rating_final:           # условие для итальянской лиги и избежать перегрузки одной ф-ции циклами
        if len(insides) > 8:
            insides[-4], insides[3] = insides[3], insides[-4]
            insides[-3], insides[4] = insides[4], insides[-3]
            insides[-2], insides[5] = insides[5], insides[-2]
            insides[-1], insides[6] = insides[6], insides[-1]
    for insides_2 in rating_final:
        if len(insides_2) > 8 and list_input[1][0] == 'I1':
            insides_2[1], insides_2[3] = insides_2[3], insides_2[1]
            insides_2[2], insides_2[4] = insides_2[4], insides_2[2]
            insides_2[3], insides_2[5] = insides_2[5], insides_2[3]
            insides_2[4], insides_2[5] = insides_2[5], insides_2[4]
    rating_final.sort()
    rating_final.reverse()
    return rating_final


choice = str()
while choice != "exit":
    print("Choose the tournament from Italy, Germany, France, enter the desired country(enter exit to exit): ", end="")
    while True:
        choice = input()
        if choice == "Italy":
            input_list = get_input("I1")
            break
        if choice == "Germany":
            input_list = get_input("D1")
            break
        if choice == "France":
            input_list = get_input("F1")
            break
        if choice == "exit":
            input_list = 0
            break
        else:
            print("Incorrect Data, try again: ", end="")
    if choice != "exit":
        try:
            teams = get_teams(input_list)
            rating = get_rating(teams, input_list)
            samescored_teams = get_samescored_teams(rating)
            local_rating = get_local_rating(samescored_teams, input_list)
            rating_final = (get_final_rating(rating, local_rating))
            sorted_final_rating = get_sorted_final_rating(rating_final, input_list)
        except Exception:
            print("Error reading file")
            break
    else:
        break
    while True:
        print("Enter table for score table, date for list of matches in this date, name of team for list of"
              " matches of this team, back to return to the selection of country: ", end="")
        choice = input()
        if choice == 'table':
            n = 1
            table = ["Pos", "Team name", "Number of games played", "Number of wins", "Number of draws",
                     "Number of losses", "Goal difference", "Points"]
            print("{0:<8}{1:<20}{2:<30}{3:<20}{4:<20}{5:<20}{6:<20}{7:<20}\n".format(*table))
            for i in sorted_final_rating:
                if input_list[1][0] == "D1" or "F1":
                    table = [n, i[-5], i[-4], i[-3],  i[-2],  i[-1],  i[1], i[0]]
                if input_list[1][0] == "I1":
                    if len(i) > 8:
                        a = 4
                    else:
                        a = 1
                    table = [n,  i[-5],  i[-4],  i[-3],  i[-2],  i[-1],  i[a], i[0]]
                print("{0:<8}{1:<20}{2:<30}{3:<20}{4:<20}{5:<20}{6:<20}{7:<20}\n".format(*table))
                n += 1
        if choice == "back":
            break
        if choice != "table" and "back" and "exit":
            table_1 = []
            try:
                for j in input_list:
                    for q in j:
                        if q == choice and j.index(q) < 5:
                            table_1.append(j)
                if len(table_1) < 1:
                    raise ValueError
                output = ["Date", "Home Team", "Away Team", "Full Time Home Team Goals", "Full Time Away Team Goals",
                          "Result"]
                print("{0:<15}{1:<20}{2:<30}{3:<30}{4:<30}{5:<20}\n".format(*output))
                for elem in table_1:
                    output = [elem[1], elem[3], elem[4], elem[5], elem[6], elem[7]]
                    print("{0:<15}{1:<20}{2:<30}{3:<30}{4:<30}{5:<20}\n".format(*output))
            except Exception:
                print("Incorrect Data, try again")
