from openpyxl import load_workbook # type: ignore
import pandas as pd # type: ignore




outPayName="Внешний" # user with name of output mony
file_path = 'test-data.csv'  # Replace with your actual file path

def detUniqueUsers(data):
    unique_who = data['Who'].unique()
    unique_whom = data['To whom'].unique()

    # Convert to a list if needed and print the result
    un_names = list(set(unique_who.tolist() + unique_whom.tolist()))
    un_users = un_names.copy()
    un_users.remove(outPayName)
    print(un_names)
    print(un_users)
    return un_names, un_users

def calcPaymentMatrix(data: pd.DataFrame, unique_names: list) -> pd.DataFrame:
    print(unique_names)
    payment_matrix = pd.DataFrame(0, index=unique_names, columns=unique_names)
    for who in unique_names:
        for whom in unique_names:
            user_to = data[(data['Who'] == who) & (data['To whom'] == whom)]
            total_paid = user_to['Cost'].sum()
            payment_matrix.at[who, whom] = total_paid
    return payment_matrix




data = pd.read_csv(file_path,encoding='utf-8')

print(data.head())


# Convert to a list if needed and print the result
unique_names, unique_user = detUniqueUsers(data)
payment_matrix = calcPaymentMatrix(data, unique_names)


print("Payment Matrix:")
print(payment_matrix)
