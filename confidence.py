def confidence_interval(correction, auth, neg):
    nega = float(neg)
    correc = float(correction)


    if auth:
        score_a = 1
    else:
        score_a = 0
        
    if nega < 20:
        score_n = 2
    elif nega >=20 and nega < 30:
        score_n = 1
    elif nega >= 30:
        score_n = 0
        
    if correc <= 5:
        score_c = 2
    elif correc > 5 and correc <= 10:
        score_c = 1
    elif correc > 10:
        score_c = 0

    # if cac == True:
    #     score_cac = 0
    # else:
    #     score_cac = 1
        
    # confidence = ((score_a + score_n + score_c) / 30) * 10
    confidence = round(((score_a + score_n + score_c) / 5) * 100)

    return confidence    
    # if confidence > 6:
    #     return "Based on logistics the job invite no be scam"
    # if confidence >= 4 and confidence <= 6:
    #     return "The job invite shows elements of scam but not too sure"
    # if confidence < 4:
    #     return "This is likely a scam"
