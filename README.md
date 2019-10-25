# doClosure
make closure plots for corrected lep pT error using Z and H events

note:
in compare 1D 2D, contain code to make fullSim-model-toy comparision part and unc of unc study
they need to be reorganized to somewhere else

## How to Make ZClosure Plots:
**doAllClosure\_mZ.py** has a function called `doAllClosure` which calls the file **doClosure\_mZ.py**.

Ultimately **doClosure\_mZ.py** produces **sigma\_m2e.txt** (or **sigma\_m2mu.txt**) which is a file that stores 
all the values to be plotted. It contains four columns:

**Example sigma\_2e.txt**:

| Measured sigma(CB,fit) [y] | Meas\_Err of sigma(CB,fit) [yErr] | Predicted sigma(pred) [x1]  | Predicted sigma(pred,corrected) [x2] |
|:--------:|:-----------:|:--------:|:-----------------:|
|  blank line |  blank line   | blank line    | blank line     |
| 1.19499228126 | 0.00855546049762  | 0.6589886754 |  0.81351701441 |
| 1.6185653721 | 0.00980362146727  | 0.926673338737 | 1.15340653145 |
| etc. | etc. | etc. | etc. |

Next, feed this file into makeGraph.py (or makeGraph.sh which just called the .py version).

Note:
 * Make sure that the LUTs (look-up tables) are up-to-date.
 * The LUTs store the lambda values across all eta and relpTErr regions.
