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

My built in de-duper isn’t the best. It only removes dups per chuck I process. It also removes any words less than 3char. Its better then nothing but if you really want to get the job done use the following sort foo.

user@host$ LC_ALL=C sort –parallel=8 -f -u -S 30G -T /passwords/tmp/ -o SortedAllPasswords.wl allPasswords.wl

    LC_ALL=C is to make sure the sorting order is based on the byte values. More info here: http://unix.stackexchange.com/a/87763


    –parallel to add parallel support typically just the amount of CPU cores you have.
    -f to ignore-case. Again hashcat is better at toggling the case.
    -u unique. To remove duplicates
    -S buffer-size. SIZE may be followed by the following multiplicative suffixes: % 1% of memory, b 1, K 1024 (default), and so on for M, G, T
    -T Temporary-directory. My default temp directory is small so I have to relocate it.
    -o output file name
    Last item is the input file name
