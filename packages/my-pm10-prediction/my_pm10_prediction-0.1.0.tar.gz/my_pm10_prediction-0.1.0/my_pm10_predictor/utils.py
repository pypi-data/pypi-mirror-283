def drop_unwanted_columns(df, columns_to_drop):
    for column in columns_to_drop:
        if column in df.columns:
            df.drop(column, axis=1, inplace=True)
    return df
