```SQL
create table bets
(
id int,
bet_timestamp text,
account_id int,
promotion_id int,
amount int
);
```

```SQL
create table accounts
(
id int,
country text,
platform text,
install_time text
);
```

```SQL
create table promos
(
account_id int,
id int,
campaign_name text,
award_type text,
award_timestamp text,
redeemed_timestamp text,
expire_timestamp text
);
```

NOTE: using text datatype for timestamp because of SQLite3 limitations


Fill tables with fake data using Python and Faker
`fill_data.py`


Q1

```SQL
select accounts.id, 
    accounts.country, 
    sum(bets.amount) as "total_bet_amount"
from accounts
left join bets
    on accounts.id = bets.account_id
where accounts.country = "CA"
group by accounts.id, accounts.country
order by total_bet_amount desc
;
```

EXAMPLE RESULTS:  These results are truncated to display the last 10 results as well to show blank values is IDs with no bets

id|country|total_bet_amount
---|---|---
134|CA|394
857|CA|250
410|CA|249
934|CA|218
479|CA|211
736|CA|206
855|CA|200
936|CA|194
884|CA|191
786|CA|184
...|...|...
3|CA|
4|CA|
7|CA|
14|CA|
15|CA|
27|CA|
33|CA|
37|CA|
51|CA|
55|CA|


Q2

NOTE: I assumed March was inclusive but that can be modified by changing the boundaires on the BETWEEN clause

```SQL
select promos.campaign_name, 
    count(distinct bets.id) as "total_bet_count", 
    sum(bets.amount) as "total_bet_amount"
from bets
left join promos
    on bets.promotion_id = promos.id and bets.account_id = promos.account_id
where promos.campaign_name = "Back To Back Special"
    and bets.bet_timestamp between "2022-01-01" and "2022-03-31" --- change here if march excluded
group by promos.campaign_name;
```

EXAMPLE RESULTS:

campaign_name|total_bet_count|total_bet_amount
---|---|---
Back To Back Special|12|575


Q3

```SQL
select accounts.platform,
    promos.campaign_name,
    count(promos.award_timestamp) as total_promos_offered,
    count(nullif(promos.redeemed_timestamp, "")) as total_promos_redeemed, --- counts all non null
    round((cast(count(nullif(promos.redeemed_timestamp, "")) as real) / cast(count(promos.award_timestamp) as real)), 2) as redeemed
from promos
join accounts
    on promos.account_id = accounts.id
where accounts.platform = "iOS"
group by accounts.platform, promos.campaign_name
;
```

EXAMPLE RESULTS:

platform|campaign_name|total_promos_offered|total_promos_redeemed|redeemed_rate
---|---|---|---|---
iOS|Back To Back Special|243|132|0.54
iOS|Get $100 In Free Bets|244|113|0.46
