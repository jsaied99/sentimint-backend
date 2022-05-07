# Import SentiMintSVM, do NOT import any other svm files
import SentiMintSVM

# To use the algorithm you must first create an instance of sentimintSVM
svm = SentiMintSVM.sentimintSVM()

# use .predict() to get a score {-100, 0, 100} on a string
# pass a SINGLE STRING. it will return a number
print((svm.predict("Good day")))
