from openpyxl import load_workbook # type: ignore
import pandas as pd # type: ignore

import sys





def detUniqueUsers(data, uselessUser:str):
    unique_who = data['Who'].unique()
    unique_whom = data['To whom'].unique()

    # Convert to a list if needed and print the result
    un_names = list(set(unique_who.tolist() + unique_whom.tolist()))
    un_users = un_names.copy()
    un_users.remove(uselessUser)
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


def preparePaymentTable(data: pd.DataFrame, users: list) -> pd.DataFrame:
    df = pd.DataFrame(columns=['to', 'from', 'sum'])
    for u in users:
        for us in users:
            if u == us:
                continue
            new_row = {"to": u,  "from": us, "sum": 0}
            df = df.append(new_row, ignore_index=True)
    # Create the DataFrame

    return df

def getUsedListFromTransaction(transaction: pd.DataFrame, all_users: list):
    if (transaction["Who use it"] == "ALL"):
        return all_users
    name_list = transaction["Who use it"].split(',')
    print(name_list)
    return name_list
    

def calculatePaymentProcess(payment_matrix: pd.DataFrame, transaction: pd.DataFrame, users: list) -> pd.DataFrame:
    payments = preparePaymentTable(payment_matrix, users)
    
    for idx, t in transaction.iterrows():
        used_list = getUsedListFromTransaction(t, users)
        sum = t["Cost"] / len(used_list)
        for user in used_list:
            if t["To whom"] not in users:
                payments.loc[(payments['to'] == t.loc["Who"]) & (payments['from'] == user), 'sum'] += sum
            else:
                payments.loc[(payments['to'] == t.loc["Who"]) & (payments['from'] == user), 'sum'] -= sum
            
    
    return payments



def main():
    args = sys.argv[1:]  # Skip the first argument (script name)
    print(args)
    if len(args) < 2:
        print('Need args data table and useless output user [table.csv, OUT]')
        return -1
    outPayName=args[1] # user with name of output mony
    file_path = args[0]  # Replace with your actual file path
    data = pd.read_csv(file_path,encoding='utf-8')

    print(data)

    # Convert to a list if needed and print the result
    unique_names, unique_user = detUniqueUsers(data, outPayName)    
    payment_matrix = calcPaymentMatrix(data, unique_names)

    print("Payment Matrix:")
    print(payment_matrix)

    print("report Matrix:")
    report = calculatePaymentProcess(payment_matrix, data, unique_user)
    print(report)




if __name__ == "__main__":
    main()


