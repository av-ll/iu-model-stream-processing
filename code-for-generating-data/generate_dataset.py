import random
import pandas as pd

temperature = [random.uniform(25,61) for i in range(18000) ]

for i in range(1500):
    i = random.uniform(61,90)
    temperature.append(i)

for i in range(400):
    i = random.uniform(10,25)
    temperature.append(i)

for i in range(100):
    i = random.uniform(90,130)
    temperature.append(i)

random.Random(1).shuffle(temperature)

humidity = temperature.copy()

for index,i in enumerate(humidity):
    if 60 < i < 90:
        i = random.uniform(0.2,0.4)
        humidity[index] = i
    elif 40< i < 61 :
        i = random.uniform(0.4,0.6)
        humidity[index] = i
    elif i < 40:
        i = random.uniform(0.4,0.6)
        humidity[index] = i
    elif 100 > i > 90:
        i = random.uniform(0,0.2)
        humidity[index] = i
    elif i > 100:
        i = random.uniform(0,0.05)
        humidity[index] = i

volume  = temperature.copy()

for index,i in enumerate(volume):
    if 60 < i < 80:
        i = random.uniform(70,90)
        volume[index] = i
    if 80 < i < 90:
        i = random.uniform(90,120)
        volume[index] = i
    elif 40< i < 61 :
        i = random.uniform(40,70)
        volume[index] = i
    elif i < 40:
        i = random.uniform(10,40)
        volume[index] = i
    elif i > 90:
        i = random.uniform(120,130)
        volume[index] = i

volume = pd.DataFrame(volume,columns=['volume(db)'])

humidity = pd.DataFrame(humidity,columns = ['humidity'])

temperature = pd.DataFrame(temperature,columns = ['temperature'])

dataframe = pd.concat([temperature,humidity,volume],axis=1)

dataframe.to_csv('sensors.csv',index=False)
