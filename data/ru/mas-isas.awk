#!/usr/bin/gawk -f
BEGIN {
    FS  = 0;
    OFS = "\t";
}
/^\t/ {
    gsub(/(^\t| \{.*|')/, "");
    gsub(/ - /, OFS);
    gsub(/ /, "_");
    print $0;
}
