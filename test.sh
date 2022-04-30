# ./test.sh запускать в виртуальной среде
trap printout SIGINT
export DUMP_FILE=out.log
printout() {
    echo ""
    echo "Finished with count=$i"
    exit
}
> out.log
END=250
for ((i=1;i<=END;i++)); do
    python -m unittest tests/test_api.py
    echo TEST / $i
done