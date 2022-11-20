import sqlite3
from faker import Faker
import datetime
con = sqlite3.connect("penn.db")
cur = con.cursor()
fake = Faker()


data_bets = []
data_accounts = []
data_promos = []


### generate lists of data entries with some fake data
cur.execute("DELETE FROM bets")
cur.execute("DELETE FROM accounts")
cur.execute("DELETE FROM promos")

for i in range(1,1000):
    data_bets.append(
        (
            i, ### id of bet placed
            fake.date_between(datetime.date(2022, 1, 1), datetime.date(2022, 12, 31)), ### time bet was placed
            fake.random_number(digits=3), ### account_id
            fake.random_number(digits=1), ### promotion_id
            fake.random_number(digits=2) ### amount
        )
    )

    data_accounts.append(
        (
            i, ### account_id
            fake.random_element(elements=('CA', 'US', 'GB')), ### country code
            fake.random_element(elements=('Android', 'iOS')), ### platform
            fake.date_between(datetime.date(2021, 1, 1), datetime.date(2021, 12, 31)) ### account creation date
        )
    )

    data_promos.append(
        (
            fake.random_number(digits=3), ### account_id
            fake.random_number(digits=1), ### promotion_id
            fake.random_element(elements=('Back To Back Special', 'Get $100 In Free Bets')), ### promo campaign name
            fake.random_element(elements=('free_bet', 'bonus')), ### type of promo
            fake.date_between(datetime.date(2022, 1, 1), datetime.date(2022, 4, 30)), ### timestamp when promo is awarded
            fake.random_element(elements=(fake.date_between(datetime.date(2022, 4, 1), datetime.date(2022, 9, 30)), "")), ### timestamp when promo is redeemed (empty means not redeemed yet)
            fake.random_element(elements=(datetime.date(2022, 9, 1), datetime.date(2022, 10, 1), datetime.date(2022, 11, 1), datetime.date(2022, 12, 1))) ### timestamp when promo is set to expire
        )
    )

print(data_bets[0])
print(data_accounts[0])
print(data_promos[0])

### insert fake data lists into tables
cur.executemany("INSERT INTO bets VALUES(?, ?, ?, ?, ?)", data_bets)
cur.executemany("INSERT INTO accounts VALUES(?, ?, ?, ?)", data_accounts)
cur.executemany("INSERT INTO promos VALUES(?, ?, ?, ?, ?, ?, ?)", data_promos)

con.commit()