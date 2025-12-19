# Loading the dataset using pandas
import pandas as pd
df = pd.read_csv("C:/Users/pinma/Downloads/customer_shopping_behavior.csv")
print(df.head())

print(df.info())
# Checking if missing data or null values are present in the dataset
print(df.isnull().sum())
# Imputing missing values in Review Rating column with the median rating of the product category
df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(lambda x:x.fillna(x.median()))

# Renaming columns according to snake casing for better readability and documentation
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={"purchase_amount_(usd)":"purchase_amount"})
print(df.columns)

#  Create age groups 
labels = ['Young','Mid-age','Senior','Elder']
df["Age_group"] = pd.qcut(df['age'],q=4,labels=labels)

print(df[['age','Age_group']].head(10))

# create new column prchase_frequency_days
frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
    }

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))

print(df['discount_applied'] == df['promo_code_used'])

# Dropping promo code used column
df = df.drop('promo_code_used', axis=1)
print(df['purchase_frequency_days'])


from sqlalchemy import create_engine
import pandas as pd
# MySQL connection
# Database credentials
username = 'root'
password = '263350'
host = 'localhost'
port = '3306'  # Default MySQL port
database = 'consumer_behaviour'

# Create engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")


table_name = 'customer'
df.to_sql(table_name, engine, if_exists='replace', index=False)
print("Data successfully loaded into MySQL!")
