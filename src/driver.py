'''
Created on Mar 31, 2016

@author: robert
'''
import sys, getopt
from src.tweet_parser import TweetParser
from src.hashtags_graph import HashtagsGraph
from src.avgdegree_calculator import AverageDegreeCalculator

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("driver.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("driver.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            
    print("Input file is ", inputfile)
    print("Output file is ", outputfile)
    
    parser = TweetParser()
    graph = HashtagsGraph()
    calculator = AverageDegreeCalculator()

    with open(inputfile, 'r') as ifile, open(outputfile, 'w') as ofile:
        for line in ifile:
            entry = parser.parse(line)
            if (entry):
                graph.update(entry)
                average_degree = calculator.calculate(graph.hashtags_graph)
                ofile.write(str(average_degree)+"\n")


if __name__ == "__main__":
    main(sys.argv[1:])
