this is a difficult one.
see the total idea at: jupyternotebooks/earnings-calendar.ipynb

there is an update implemented in the backend, which calls new earning dates into the table "public.earning_dates"

also, we are running monthly a job to check the effect of earnings on that stock. this is saved in the quarterly_financials_effect table.

remarks:
- i think the earnings date might differ, it's maybe the day befoire
- we do not yet know when results are published to yahoo finance, so some kind of constant querying is required

the effect info we have looks like this:
AAPL	0.09	0.13	[-0.026229666053962788, 0.22740269587868328, 0.09210423296987436]	{"Total Other Income Expense Net": 0.23, "win": -0.5, "Total Operating Expenses": -0.96, "Research Development": -0.97}

## order of steps

1. query "earning_dates" table for the earnings today or tomorrow
2. if there are, for each stock 
3. query yahoo finance for quarterly financials, same way like we do it in the backend to cretae "quarterly_financials" table
4. if the date of that query is today or tomorrow, decide on a trading position, otherwise wait half an hour (?)
5. if we have an update, calculate the pct change to the previous daz similar to "earnings.py" in backend, load the matching effect from the "quarterly_financials_effect" table and compare if sell or buy order

this might be another bot/cronjob
6. after trade execution, wait half an hour and check if we exceeded the medium change amount already. calculate this manually and take mean(abs())
