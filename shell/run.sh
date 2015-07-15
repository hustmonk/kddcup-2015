set -e
command="1"

function valid() {
    echo "valid"
    python features.py ../data/train2/log_train.csv ../data/train2/enrollment_train.csv train2.txt &
    python features.py ../data/train1/log_train.csv ../data/train1/enrollment_train.csv train1.txt 
    #python features.py ../data/train1/log_train.csv ../data/enrollment_train.csv.expand  train.txt.expand 
    python learn.py train1.txt train2.txt valid.txt 1
}
function sub() {
    echo "sub"
    nohup python features.py ../data/test/log_test.csv ../data/test/enrollment_test.csv test.txt &
    python features.py ../data/train/log_train.csv ../data/train/enrollment_train.csv train.txt
    python learn.py train.txt test.txt sub.csv 0
    python learn01.py train.txt test.txt sub.csv 0
    python sub01.py
}

if [ $command == "1" ];then
    valid
elif [ $command == "2" ];then
    sub
elif [ $command == "3" ];then
    valid
    sub
fi
