# usage: dl.sh router-ip 
router=$1
log=$2
scp root@${router}:/root/logs/${log}.csv /home/smeets/thesis/datasets/
