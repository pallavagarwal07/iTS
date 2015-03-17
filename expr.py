from tabulate import tabulate
import re
import sys

inp = sys.stdin.read()
def handleOutput(line, scope):
    sep = re.findall(r'(?s)printf\s*\(\"(.*)\"(,.+)*\)', line)
    formatString = sep[0][0]
    if sep[0][1] is '':
        printString = formatString
    formatVars = sep[0][1][1:].split(',')
    for i in range(0, len(formatVars)):
        formatVars[i] = calculate(formatVars[i].strip(), scope)
    formatString = re.sub(r'%(lld|ld|d)', '%d', formatString)
    formatString = re.sub(r'%(Lf|lf|f)', '%f', formatString)
    if sep[0][1] is not '':
        printString = formatString % tuple(formatVars)


    print ("I am printing :\n"+printString)





    

