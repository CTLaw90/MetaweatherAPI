from weatherobj import weatherOBJ
import sys
if len(sys.argv) > 1:
    locations = (sys.argv[1:])
else:
    locations = ['2487610', '2442047', '2366355']

def main():

    y = weatherOBJ(locations)
    y.getData('getAvgMax')

main()