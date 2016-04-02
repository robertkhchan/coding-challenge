'''
Created on Mar 31, 2016

@author: Robert Chan
'''
import sys, getopt
from avgdegree_calculator import AverageDegreeCalculator
from hashtags_graph import HashtagsGraph
from tweet_parser import TweetParser

def main(argv):
    '''Entry point to calculate the average degree of a vertex 
       in a Twitter hashtag graph for the last 60 seconds.
    '''
    inputfile = ''
    outputfile = ''
    try:
        opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("average_degree.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("average_degree.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            
    parser = TweetParser()
    graph = HashtagsGraph()
    calculator = AverageDegreeCalculator()

    with open(inputfile, 'r') as ifile, open(outputfile, 'w') as ofile:
        for line in ifile:
            entry = parser.parse(line)
            if (entry):
                graph.update(entry)
                average_degree = calculator.calculate(graph.edge_counts)
                ofile.write(str(average_degree)+"\n")


if __name__ == "__main__":
    main(sys.argv[1:])
