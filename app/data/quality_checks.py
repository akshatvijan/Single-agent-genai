
def check_data(df):
    print("Dataset shape:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum().sort_values(ascending=False).head(15))

    print("\nDuplicated rows:", df.duplicated().sum())

    print("Unique user IDs:", df["UserID"].nunique())

    print("Duplicate user IDs:", df["UserID"].duplicated().sum())

    print("\nColumn names:")
    print(df.columns)

    print("\nData types:")
    print(df.dtypes)
