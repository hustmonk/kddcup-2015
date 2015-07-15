set -e
command="1"

function valid() {
    echo "valid"
    dt=`date +"%s"`
    >logs/$dt
    nohup python learn.py ../shell/train1.txt ../shell/train2.txt valid.txt 1 >logs/$dt &
    #nohup python learn.py ../shell/train1.txt.transfer ../shell/train2.txt.transfer valid.txt 1 >logs/$dt &
    tail -f logs/$dt
}
function sub() {
    echo "sub"
    python learn.py ../shell/train.txt ../shell/test.txt sub.csv 0
    #python learn01.py train.txt test.txt sub.csv 0
    #python sub01.py
}

if [ $command == "1" ];then
    valid
elif [ $command == "2" ];then
    sub
elif [ $command == "3" ];then
    valid
    sub
fi
