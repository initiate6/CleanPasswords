pyClean.py

Cleans large dictionaries removing configured chars via regex.
For more information check out my blog: https://blog.init6.me/?p=63

    --help        Prints this help
    --file        File containing words you want to clean up. 1 word per line
    --threads     Number of processors
    --output      Output filename. Default: input file name plus .out
    --lines       Lines per chuck to read Default [10000]
    --startRegex  Regex to remove at start of line. Default [^[\d|\W]+]
    --endRegex    Regex to remove at end of line.   Default [[\d|\W]+$]
