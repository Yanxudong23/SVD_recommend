#!/bin/bash
source  ../conf/conf.sh
echo "时间窗口:"$daylenth
#echo "end day is  $end_day"
today=`date +%Y%m%d`
yesterday=`date -d "-1days" +%Y%m%d`
ts=`date -d  "-${daylenth_cf}days"   +%s`
#news_daylenth=10
news_start_day=`date -d "-${news_daylenth_cf}days" +%Y%m%d`
echo "timestamp is $ts"
input=""
inputbase="test/clk_ttime/"
#数据导入hdfs
#./mv_date_hdfs.sh 
#删除标志文件
/bin/rm ../dump/*

#nohup ./news_rank.sh  $daylenth_rank  $user_items  $item_ctr  >news_rank.log 2>&1 &

i=1
while [ $i -le ${daylenth_cf} ]
do
    tm=`date -d "-${i}days" +%Y%m%d`
    let i++
    hadoop fs -ls  ${inputbase}${tm}/_SUCCESS
    if [ $? -eq 0 ] ;then
        input="$input ${inputbase}${tm}"
    fi
done
start_day=`date -d "-${daylenth_cf}days" +%Y%m%d%H`
today_clk=clk_data/$today
yes_clk=clk_data/$yesterday

#用户点击未曝光历史
exposeinput="/user/exposedata/${day}"

echo "exposeinput finished"

input="$input $exposeinput"

echo "$input"

#用户-新闻-时间表

STREAMING_PATH="/data/hadoop-streaming-2.4.1.jar"
#hadoop fs -rmr $news_usr_table_hdfs
#if [ 1 -eq 2 ] ;then
echo "input is $input"
echo "ouput is $iut_table"
hadoop jar $STREAMING_PATH  \
    -D mapred.map.tasks=200 \
    -D mapred.reduce.tasks=200 \
    -D mapreduce.job.queuename=media \
    -D mapred.job.name="news_users_table" \
    -input $input \
    -file  ./map_iut.py  \
    -file  ./reduce_iut.py  \
    -output $iut_table \
    -mapper "python map_iut.py  " \
    -reducer "python reduce_iut.py 400"

hadoop fs -ls $iut_table/_SUCCESS
if [ $? -eq 0 ]; then
    echo "IUtable success"
else
    echo "IUtable faild"
    exit 1
fi

#所有的新闻列表

#hadoop fs -cat $iut_table/*  |python ./itemdict.py  dump.txt

#用户-新闻-评级表

echo "input is $iut_table"
echo "output is $iur_table"
hadoop jar $STREAMING_PATH  \
	-D mapred.map.tasks=200 \
	-D mapred.reduce.tasks=200 \
	-D mapreduce.job.queuename=media \
	-D mapred.job.name="item_user_rank_table" \
	-input $iut_table \
	-file  ./map_iur.py \
	-file  ./reduce_iur.py  \
	-output $iur_table \
	-mapper "python map_iur.py "  \
	-reducer "python reduce_iur.py " 
	
hadoop fs -ls $iur_table/_SUCCESS
if [ $? -eq 0 ]; then
	echo "IUtable success"
else
	echo "IUtable faild"
	exit 1
fi


#用户-点击历史

echo "input is $iur_table"
echo "output is $test_table"
hadoop jar $STREAMING_PATH  \
	-D mapred.map.tasks=200 \
	-D mapred.reduce.tasks=200 \
	-D mapreduce.job.queuename=media \
	-D mapred.job.name="test_table" \
	-input $iur_table \
	-file  ./map_test.py \
	-file  ./reduce_test.py  \
	-output $test_table \
	-mapper "python map_test.py"  \
	-reducer "python reduce_test.py  50" 
	
hadoop fs -ls $test_table/_SUCCESS
if [ $? -eq 0 ]; then
	echo "IUtable success"
else
	echo "IUtable faild"
	exit 1
fi

#用户-未点击新闻

#hadoop fs -cat  $test_table/*  |python ./testdata.py   >  ./test.txt


#training-testing
hadoop fs -cat  $test_table/*  |python  -u ./train_test.py  20 

if [ $? -eq 0 ]; then
	echo "training-testing success"
else
	echo "training-testing faild"
	exit 1
fi


hadoop fs -rmr  item_cf/iut_table/$day
hadoop fs -rmr  item_cf/iur_table/$day
hadoop fs -rmr  exposedata/$day
#hadoop fs -rmr  item_cf/test_table/$day

