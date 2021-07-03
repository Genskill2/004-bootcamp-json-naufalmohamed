# Add the functions in this file
import json
import math


def load_journal(fname):
    f = open(fname)
    data = json.load(f)
    f.close()
    return data


def compute_phi(fname, event):
    data = load_journal(fname)
    n_1_plus = 0
    n_plus_1 = 0
    n_1_1 = 0
    n_0_0 = 0
    n_1_0 = 0
    n_0_1 = 0
    for entry in data:
        if event in entry["events"]:
            n_1_plus += 1
        if entry["squirrel"] == True:
            n_plus_1 += 1
        if event in entry["events"] and entry["squirrel"] == True:
            n_1_1 += 1
        if event not in entry["events"] and entry["squirrel"] == False:
            n_0_0 += 1
        if event in entry["events"] and entry["squirrel"] == False:
            n_1_0 += 1
        if event not in entry["events"] and entry["squirrel"] == True:
            n_0_1 += 1

    n_0_plus = 91 - n_1_plus
    n_plus_0 = 91 - n_plus_1
    corr = ((n_1_1*n_0_0)-(n_1_0*n_0_1))/math.sqrt(n_1_plus*n_0_plus*n_plus_1*n_plus_0)
    return corr


def compute_correlations(fname):
    data = load_journal(fname)

    unique_events = []
    for entry in data:
        for event in entry["events"]:
            if event not in unique_events:
                unique_events.append(event)

    event_dict = {}
    for i in unique_events:
        corr = compute_phi("journal.json", i)
        event_dict[i] = float(0)
        event_dict[i] += corr

    return event_dict


def diagnose(fname):
    event_dict = compute_correlations(fname)

    corr_list = []
    for element in event_dict.values():
        corr_list.append(element)

    diag_positive = []
    diag_negative = []
    corr_list.sort()
    for element in event_dict:
        if event_dict[element] == corr_list[-1]:
            diag_positive = element
        if event_dict[element] == corr_list[0]:
            diag_negative = element

    return diag_positive, diag_negative

