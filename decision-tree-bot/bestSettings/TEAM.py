def getDecision(dfrow):
    if dfrow['volume'] <= 1460400.0:
        if dfrow['high'] <= 329.61:
            if dfrow['low'] <= 191.17:
                if dfrow['volume'] <= 773700.0:
                    if dfrow['open'] <= 51.85:
                        if dfrow['adj_close'] <= 42.75:
                            return 1
                        else:  # if dfrow['adj_close'] > 42.75
                            return 0
                    else:  # if dfrow['open'] > 51.85
                        return 1
                else:  # if dfrow['volume'] > 773700.0
                    return 1
            else:  # if dfrow['low'] > 191.17
                if dfrow['volume'] <= 778600.0:
                    return 1
                else:  # if dfrow['volume'] > 778600.0
                    if dfrow['close'] <= 223.52:
                        if dfrow['open'] <= 212.02:
                            return 1
                        else:  # if dfrow['open'] > 212.02
                            return 0
                    else:  # if dfrow['close'] > 223.52
                        if dfrow['close'] <= 229.09:
                            return 1
                        else:  # if dfrow['close'] > 229.09
                            return 1
        else:  # if dfrow['high'] > 329.61
            return 1
    else:  # if dfrow['volume'] > 1460400.0
        if dfrow['high'] <= 113.78:
            return 1
        else:  # if dfrow['high'] > 113.78
            if dfrow['volume'] <= 2397150.0:
                if dfrow['volume'] <= 2338550.0:
                    return 0
                else:  # if dfrow['volume'] > 2338550.0
                    return 1
            else:  # if dfrow['volume'] > 2397150.0
                if dfrow['volume'] <= 4993350.0:
                    return 0
                else:  # if dfrow['volume'] > 4993350.0
                    return 1
