def getDecision(dfrow):
    if dfrow['volume'] <= 2993849984.0:
        return 1
    else:  # if dfrow['volume'] > 2993849984.0
        if dfrow['volume'] <= 6066684928.0:
            if dfrow['adj_close'] <= 6586.92:
                return 0
            else:  # if dfrow['adj_close'] > 6586.92
                return 0
        else:  # if dfrow['volume'] > 6066684928.0
            if dfrow['high'] <= 5581.51:
                return 1
            else:  # if dfrow['high'] > 5581.51
                if dfrow['volume'] <= 22139246592.0:
                    if dfrow['low'] <= 8612.76:
                        if dfrow['open'] <= 6323.35:
                            return 1
                        else:  # if dfrow['open'] > 6323.35
                            return 0
                    else:  # if dfrow['low'] > 8612.76
                        if dfrow['volume'] <= 8330524928.0:
                            return 1
                        else:  # if dfrow['volume'] > 8330524928.0
                            return 0
                else:  # if dfrow['volume'] > 22139246592.0
                    if dfrow['high'] <= 19577.66:
                        if dfrow['low'] <= 6593.44:
                            return 0
                        else:  # if dfrow['low'] > 6593.44
                            return 1
                    else:  # if dfrow['high'] > 19577.66
                        if dfrow['close'] <= 43682.7:
                            if dfrow['volume'] <= 36882411520.0:
                                return 0
                            else:  # if dfrow['volume'] > 36882411520.0
                                if dfrow['high'] <= 29816.53:
                                    return 1
                                else:  # if dfrow['high'] > 29816.53
                                    return 0
                        else:  # if dfrow['close'] > 43682.7
                            if dfrow['adj_close'] <= 60688.04:
                                return 1
                            else:  # if dfrow['adj_close'] > 60688.04
                                return 1
