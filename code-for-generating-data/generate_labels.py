import pandas as pd

data = pd.read_csv('sensors.csv')
labels = list()
for i in data.values:
    if i[0] > 85 and i[2]>90:
        label = 1
        labels.append(label)
    elif i[2] < 10 and i[0]<20:
        label =1
        labels.append(label)

    elif i[0] > 100 or i[2] > 100 :
        label=1
        labels.append(label)
    elif 87 < i[0] < 92 :
        label = 0
        labels.append(label)
    else:
        label = 0
        labels.append(label)

data['labels'] = labels




data.to_csv('data_frame.csv',index=False)
