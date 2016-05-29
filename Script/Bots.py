import sys
from random import randint, uniform


def best_response(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):

    
    step = len(history)
    
    if step == 0:
        return 0
    
    #Initialization
    for i in range(1, step+1):
        if query in history[step-i]:
            adv_slots = history[step-i][query]["adv_slots"]
            adv_bids = history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0


    #print ("adv_bids")
    #print(adv_bids)

    sort_bids=sorted(adv_bids[query].values(), reverse=True)

    #print ("sort_bids")
    #print(sort_bids)

    sort_slots=sorted(slot_ctrs[query].keys(), key=slot_ctrs[query].__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.values():
        last_slot=-1
    else:
        last_slot = list(adv_slots.values()).index(name)

    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        
        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
        elif i >= len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
            
        else: #If I take the slot as before or a worse one (but not the last)
            if len(sort_bids)==1:
                tmp_pay = sort_bids[0]
            else:
                if tp == "fpa":
                    tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the next advertiser
                elif tp == "gsp":
                    tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[query][sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    #ultima slot
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value, sort_bids[len(sort_slots)])
    
    #prima slot
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2
    
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[query][sort_slots[preferred_slot]])/slot_ctrs[query][sort_slots[preferred_slot-1]] * (adv_value - payment))


def best_response_competitive(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    
    step = len(history)
    
    if step == 0:
        return 0

    #Initialization
    for i in range(1, step+1):
        if query in history[step-i]:
            adv_slots = history[step-i][query]["adv_slots"]
            adv_bids = history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0

    sort_bids = sorted(adv_bids[query].values(), reverse=True)

    sort_slots = sorted(slot_ctrs[query].keys(), key=slot_ctrs[query].__getitem__, reverse=True)

    if name not in adv_slots.values():
        last_slot = -1
    else:
        last_slot = list(adv_slots.values()).index(name)

    utility = -1
    preferred_slot = -1
    payment = 0

    for i in range(len(sort_slots)):

        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned

        elif i >= len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0

        else: #If I take the slot as before or a worse one (but not the last)
            if len(sort_bids)==1:
                tmp_pay = sort_bids[0]
            else:
                if tp == "fpa":
                    tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the next advertiser
                elif tp == "gsp":
                    tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser

    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[query][sort_slots[i]]*(adv_value-tmp_pay)

        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay

    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    #ultima slot
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return max(adv_value, sort_bids[len(sort_slots)])

    #prima slot
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return max(adv_value, payment)

    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return max(payment+1, sort_bids[preferred_slot]-1)

def best_response_altruistic(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    
    step = len(history)

    if step == 0:
        return randint(0, adv_value)

    #Initialization
    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots = history[step-i][query]["adv_slots"]
            adv_bids = history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return randint(0, adv_value)

    sort_bids = sorted(adv_bids[query].values(), reverse=True)

    sort_slots = sorted(slot_ctrs[query].keys(), key=slot_ctrs[query].__getitem__, reverse=True)

    if name not in adv_slots.values():
        last_slot =- 1
    else:
        last_slot = list(adv_slots.values()).index(name)

    utility = -1
    preferred_slot = -1
    payment = 0

    for i in range(len(sort_slots)):

        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned

        elif i >= len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0

        else: #If I take the slot as before or a worse one (but not the last)
            if len(sort_bids) == 1:
                tmp_pay = sort_bids[0]
            else:
                if tp == "fpa":
                    tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the next advertiser
                elif tp == "gsp":
                    tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser

    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[query][sort_slots[i]]*(adv_value-tmp_pay)

        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay

    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    #ultima slot
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value, sort_bids[len(sort_slots)])

    #prima slot
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return min(adv_value, payment)

    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    if sort_bids[preferred_slot]-1 < 0:
        return 0
    return min(payment+1, sort_bids[preferred_slot]-1)


def competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    
    step = len(history)
    
    if step == 0:
        return adv_value
    

    for i in range(1,step+1):
        if query in history[step-i]:
            adv_bids = history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0

    sort_bids = sorted(adv_bids[query].values(), reverse=True)
    
    return sort_bids[0] + uniform(0, 1)


def budget_saving(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    
    step = len(history)
    
    if step == 0:
        return randint(0, adv_value)
    
    for i in range(1, step+1):
        if query in history[step-i]:
            adv_slots = history[step-i][query]["adv_slots"]
            adv_bids = history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return randint(0, adv_value)
    
    min_value = sys.float_info.max
    min_name = None
    for bid in adv_bids[query]:
        if not bid in list(adv_slots.values()) and adv_bids[query][bid] < min_value:
            min_value = adv_bids[query][bid]
            min_name = bid

    return min(min_value, adv_value)


def random(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):

    all_bids = []
    for i in range(len(history)):
        if query in history[i]:
            for b in history[i][query]["adv_bids"].values():
                all_bids += list(b.values())

    if len(all_bids) == 0:
        return randint(0, adv_value)

    maxbidEVER= max(all_bids)

    return uniform(0, maxbidEVER+1)


def competitor_budget(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):

    if current_budget >= budget/2:
        return competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)
    else:
        return best_response(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)


def preferential_competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    if adv_value > threshold:
        return competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)
    else:
        return budget_saving(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)


def best_competitor_budget(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):

    if current_budget >= budget/2:
        return best_response_competitive(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)
    else:
        return best_response(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)


def best_preferential_competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp):
    if adv_value > threshold:
        return best_response_competitive(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)
    else:
        return budget_saving(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query, tp)















