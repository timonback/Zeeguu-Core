#!/bin/bash

echo -n DB Password: 
read -s password
echo $password

while true; do
    
    clear
	mysql -u zeeguu_test -p$password -e "select * from zeeguu_test.exercise as e, zeeguu_test.exercise_outcome as o where e.outcome_id = o.id LIMIT 10"
	sleep 1

done

