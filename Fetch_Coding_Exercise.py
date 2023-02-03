import pandas as pd
import sys

def main():
    
    file_name = 'transactions.csv'
    
    # read argument and check
    n = len(sys.argv)
    if n != 2: 
        raise ValueError("Invalid Input")
    input_cost = sys.argv[1]
    if ((not input_cost.isnumeric()) or int(input_cost) <= 0):
        raise ValueError("Invalid Input")
    input_cost = -int(input_cost)
       
    # read the csv file
    data = pd.read_csv(file_name)
    data = data.sort_values(by=['timestamp']).copy()
    print(data)
    
    '''
    apply cost to the payer
    internal_mode: 1 if the cost is from the csv file
                   0 if the cost is from user input
    '''
    def apply_cost(cost_points, payer, internal_mode=1):
        if (internal_mode):
            selected_data = data[(data['payer'] == payer) & (data['points'] > 0)]
        else:
            selected_data = data[(data['points'] > 0)]
        for index, row in selected_data.iterrows():
            left_points = row.points + cost_points
            if left_points < 0:
                cost_points = left_points
                data.drop(index, inplace=True)
            else:
                data.at[index, 'points'] = left_points
                cost_points = 0
                if (internal_mode): data.drop(cost_index, inplace=True)
                break
        return cost_points
    
    # get the set of payers
    payers = set(data['payer'].tolist())

    # extract all the cost in the file
    cost = data[data['points'] < 0]

    # for each cost from the file, deduct from the corresponding payer
    for cost_index, cost_row in cost.iterrows():
        payer, cost_points = cost_row.payer, cost_row.points
        apply_cost(cost_points, payer)

    # deduct the cost from argument
    remaining_points = apply_cost(input_cost, '', 0)
    if remaining_points != 0:
        raise ValueError("Error: Cost is invalid. There is not enough points in payer. ")

    # sum remaining points for each payer
    result = {key: data[(data['payer'] == key)]['points'].sum() for key in payers}
    # print(data)
    print(result)
    
if __name__ == '__main__':
    main()