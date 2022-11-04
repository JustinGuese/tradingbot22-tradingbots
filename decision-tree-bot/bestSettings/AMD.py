def getDecision(dfrow):
    if dfrow['adj_close'] <= 11.54:
        return 0
    else:  # if dfrow['adj_close'] > 11.54
        if dfrow['open'] <= 55.42:
            if dfrow['volume'] <= 82882496.0:
                if dfrow['high'] <= 32.22:
                    if dfrow['high'] <= 28.25:
                        if dfrow['volume'] <= 34596450.0:
                            return 0
                        else:  # if dfrow['volume'] > 34596450.0
                            return 1
                    else:  # if dfrow['high'] > 28.25
                        return 0
                else:  # if dfrow['high'] > 32.22
                    return 1
            else:  # if dfrow['volume'] > 82882496.0
                if dfrow['volume'] <= 121193400.0:
                    return 0
                else:  # if dfrow['volume'] > 121193400.0
                    return 1
        else:  # if dfrow['open'] > 55.42
            if dfrow['low'] <= 79.46:
                if dfrow['open'] <= 63.31:
                    return 1
                else:  # if dfrow['open'] > 63.31
                    return 0
            else:  # if dfrow['low'] > 79.46
                if dfrow['adj_close'] <= 147.19:
                    if dfrow['open'] <= 129.75:
                        if dfrow['volume'] <= 60645800.0:
                            return 1
                        else:  # if dfrow['volume'] > 60645800.0
                            if dfrow['volume'] <= 128297000.0:
                                return 0
                            else:  # if dfrow['volume'] > 128297000.0
                                return 1
                    else:  # if dfrow['open'] > 129.75
                        if dfrow['high'] <= 148.27:
                            return 0
                        else:  # if dfrow['high'] > 148.27
                            return 1
                else:  # if dfrow['adj_close'] > 147.19
                    return 1
