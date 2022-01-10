from weatherobj import weatherOBJ

locations = ['2487610', '2442047', '2366355', 'New York', 'Boston']

def main():

    y = weatherOBJ(locations)
    y.getData('getAvgMax')

main()