#!/bin/sh


#######################################################################  
#	
# 功能：硬盘占用率达到设定的阙值，
#	就把不在播放列表里的老节目删掉一部分，
#	保证不发生故障，同时最大程度保留老节目.
#	同时，30天内的节目不会被删除，以防止节目更新了一半，
#	播出单还未更新的情况下，系统重启后误删刚更新的节目,
#	30天这个值是可以自定义的。
#		  
# 使用：把该脚本添加到开机启动脚本
#
# 如果是bash, 可以用更简洁的方式判断字符串是否存在于数组中
# if [[ ! ${VIDEO_LIST} =~ ${video} ]];then
#       do somthing
# fi
# By Songlihong 20200710
########################################################################	


VIDEO_DIR=/mnt/video_source
PLAYLIST=/mnt/play_list/channel5.ini
EXT=ts
MOUNT_POINT=/mnt
RESERVE_DAYS="+30"
MAX_DISK_USAGE=65



get_video_list() {
	for f in `grep $1 $2 | awk -F\= '{print $2}'`;do
		echo $3/$f
	done
}

cp -af $PLAYLIST ${PLAYLIST}.BAK
echo ${PLAYLIST}.BAK | xargs -I {} dos2unix {} 2> /dev/null
VIDEO_LIST=`get_video_list $EXT ${PLAYLIST}.BAK $VIDEO_DIR | sort | uniq`
disk_usage_pecent=`df -h | grep $MOUNT_POINT | awk '{print $5}'` 
disk_usage=$((${disk_usage_pecent%%%}+0))

for video in `find $VIDEO_DIR -type f -iname "*.$EXT" -mtime $RESERVE_DAYS`;do
	if [ ${disk_usage} -ge ${MAX_DISK_USAGE} ];then
		match=`echo "${VIDEO_LIST[@]}" | grep -wq "$video" && echo "Y" || echo "N"` 
		if [ x"$match" != x"Y" ];then
			rm -rf $video
			rm -rf ${video}.index
		fi
	else
		break
	fi
	disk_usage_pecent=`df -h | grep $MOUNT_POINT | awk '{print $5}'`
	disk_usage=$((${disk_usage_pecent%%%}+0))
done

rm -rf ${PLAYLIST}.BAK



