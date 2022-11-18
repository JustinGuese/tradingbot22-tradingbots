import json

import numpy as np
from eiten import Eiten


class ArgsObj:
    history_to_use = None
    data_granularity_minutes = None
    is_test = None
    future_bars = None
    apply_noise_filtering = None
    only_long = None
    market_index = None
    eigen_portfolio_number = None
    stocks_file_path = None
    
    def __init__(self, history_to_use=90, data_granularity_minutes=3600, is_test=1, future_bars=30, 
    apply_noise_filtering=1, only_long=0, market_index='QQQ', eigen_portfolio_number=3, 
    stocks_file_path='stocks/stocks.txt') -> None:
        self.history_to_use = history_to_use
        self.data_granularity_minutes = data_granularity_minutes
        self.is_test = is_test
        self.future_bars = future_bars
        self.apply_noise_filtering = apply_noise_filtering
        self.only_long = only_long
        self.market_index = market_index
        self.eigen_portfolio_number = eigen_portfolio_number
        self.stocks_file_path = stocks_file_path
    
args = ArgsObj(
    history_to_use=90, data_granularity_minutes=3600, is_test=1, future_bars=30, 
    apply_noise_filtering=1, only_long=1, market_index='QQQ', eigen_portfolio_number=3, 
    stocks_file_path='stocks/stocks.txt'
)

eiten = Eiten(args)

# start backtest sim and so on
historical_price_info, future_prices, symbol_names, predicted_return_vectors, returns_matrix, returns_matrix_percentages = eiten.load_data()
historical_price_market, future_prices_market = eiten.dataEngine.get_market_index_price()

# Calculate covariance matrix
covariance_matrix = np.cov(returns_matrix)

# Use random matrix theory to filter out the noisy eigen values
if eiten.args.apply_noise_filtering:
    print(
        "\n** Applying random matrix theory to filter out noise in the covariance matrix...\n")
    covariance_matrix = eiten.strategyManager.random_matrix_theory_based_cov(
        returns_matrix)

# Get weights for the portfolio
eigen_portfolio_weights_dictionary = eiten.strategyManager.calculate_eigen_portfolio(
    symbol_names, covariance_matrix, eiten.args.eigen_portfolio_number)
mvp_portfolio_weights_dictionary = eiten.strategyManager.calculate_minimum_variance_portfolio(
    symbol_names, covariance_matrix)
msr_portfolio_weights_dictionary = eiten.strategyManager.calculate_maximum_sharpe_portfolio(
    symbol_names, covariance_matrix, predicted_return_vectors)
ga_portfolio_weights_dictionary = eiten.strategyManager.calculate_genetic_algo_portfolio(
    symbol_names, returns_matrix_percentages)

# Print weights
print("\n*% Printing portfolio weights...")
eiten.print_and_plot_portfolio_weights(
    eigen_portfolio_weights_dictionary, 'Eigen Portfolio', plot_num=1)
eiten.print_and_plot_portfolio_weights(
    mvp_portfolio_weights_dictionary, 'Minimum Variance Portfolio (MVP)', plot_num=2)
eiten.print_and_plot_portfolio_weights(
    msr_portfolio_weights_dictionary, 'Maximum Sharpe Portfolio (MSR)', plot_num=3)
eiten.print_and_plot_portfolio_weights(
    ga_portfolio_weights_dictionary, 'Genetic Algo (GA)', plot_num=4)
# eiten.draw_plot("output/weights.png")

WEIGHTS = dict(
    eigen = eigen_portfolio_weights_dictionary,
    minvar = mvp_portfolio_weights_dictionary,
    sharpe = msr_portfolio_weights_dictionary,
    gen = ga_portfolio_weights_dictionary
)

# Back test
results = dict()
print("\n*& Backtesting the portfolios...")
results["backtest"] = dict()
results["backtest"]["eigen"] = eiten.backTester.back_test(symbol_names, eigen_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            historical_price_market,
                            eiten.args.only_long,
                            market_chart=True,
                            strategy_name='Eigen Portfolio')
results["backtest"]["minvar"] = eiten.backTester.back_test(symbol_names,
                            mvp_portfolio_weights_dictionary,
                            eiten.data_dictionary, historical_price_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Minimum Variance Portfolio (MVP)')
results["backtest"]["sharpe"] = eiten.backTester.back_test(symbol_names, msr_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            historical_price_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Maximum Sharpe Portfolio (MSR)')
results["backtest"]["gen"] = eiten.backTester.back_test(symbol_names,
                            ga_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            historical_price_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Genetic Algo (GA)')
# eiten.draw_plot("output/backtest.png")

print("\n#^ Future testing the portfolios...")
# Future test
results["future"] = dict()
results["future"]["eigen"] = eiten.backTester.future_test(symbol_names,
                            eigen_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            future_prices_market,
                            eiten.args.only_long,
                            market_chart=True,
                            strategy_name='Eigen Portfolio')
results["future"]["minvar"] = eiten.backTester.future_test(symbol_names,
                            mvp_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            future_prices_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Minimum Variance Portfolio (MVP)')
results["future"]["sharpe"] = eiten.backTester.future_test(symbol_names,
                            msr_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            future_prices_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Maximum Sharpe Portfolio (MSR)')
results["future"]["gen"] = eiten.backTester.future_test(symbol_names,
                            ga_portfolio_weights_dictionary,
                            eiten.data_dictionary,
                            future_prices_market,
                            eiten.args.only_long,
                            market_chart=False,
                            strategy_name='Genetic Algo (GA)')
# eiten.draw_plot("output/future_tests.png")

# Simulation
print("\n+$ Simulating future prices using monte carlo...")
results["sim"] = dict()
results["sim"]["eigen"] = eiten.simulator.simulate_portfolio(symbol_names,
                                    eigen_portfolio_weights_dictionary,
                                    eiten.data_dictionary,
                                    future_prices_market,
                                    eiten.args.is_test,
                                    market_chart=True,
                                    strategy_name='Eigen Portfolio')
results["sim"]["minvar"] = eiten.simulator.simulate_portfolio(symbol_names,
                                    eigen_portfolio_weights_dictionary,
                                    eiten.data_dictionary,
                                    future_prices_market,
                                    eiten.args.is_test,
                                    market_chart=False,
                                    strategy_name='Minimum Variance Portfolio (MVP)')
results["sim"]["sharpe"] = eiten.simulator.simulate_portfolio(symbol_names,
                                    eigen_portfolio_weights_dictionary,
                                    eiten.data_dictionary,
                                    future_prices_market,
                                    eiten.args.is_test,
                                    market_chart=False,
                                    strategy_name='Maximum Sharpe Portfolio (MSR)')
results["sim"]["gen"] = eiten.simulator.simulate_portfolio(symbol_names,
                                    ga_portfolio_weights_dictionary,
                                    eiten.data_dictionary,
                                    future_prices_market,
                                    eiten.args.is_test,
                                    market_chart=False,
                                    strategy_name='Genetic Algo (GA)')
# eiten.draw_plot("output/monte_carlo.png")


## next interpret results
# with open('output/results.json', 'w') as fp:
#     json.dump(results, fp, indent=4)

# somehow the weights contain negative values even though the only_long flag is set to True
# fix this manually
todelete = []

for weight in WEIGHTS:
    for ticker in WEIGHTS[weight]:
        if WEIGHTS[weight][ticker] <= 0:
            todelete.append([weight,ticker])
# and run again to kick out zero weights
for [weight,ticker] in todelete:
    del WEIGHTS[weight][ticker]

from pprint import pprint

winners = dict()
for testtype in results.keys():
    highestWin = -99999
    best = None
    for strategy in results[testtype].keys():
        if results[testtype][strategy][-1] > highestWin:
            highestWin = results[testtype][strategy][-1]
            best = strategy
    winners[testtype] = dict(name = best, win = highestWin, weights = WEIGHTS[best])

with open('../persistent/winners.json', 'w') as fp:
    json.dump(winners, fp, indent=4)
pprint(winners)