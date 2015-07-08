#! usr/bin/bash

# Seeding Random Generator
RANDOM=$$$(date +%s)


# List of Device id's
declare -a all_Connected_devices=(dev_001 dev_002 dev_003 dev_004 dev_005)
num_Connect_devices=${#all_Connected_devices[@]} 
num_Connect_devices=$((num_Connect_devices-1))
echo $num_Connect_devices

# Initializing counter
counter=0

# infinite while loop
while true
do 
	echo $counter
	echo ${all_Connected_devices[$counter]}
	
	#Generating Health Vitals
	HR=$(shuf -i 60-100 -n 1)
	echo "HeartRate="$HR
	#Blood_oxygen=$(shuf -i 90-99 -n 0.01)
	#echo "Blood oxygen=",$Blood_oxygen

	Blood_oxygen=$(python -S -c "import random; print random.uniform(90,99)")
	echo "Blood oxygen="$Blood_oxygen

	body_temp=$(python -S -c "import random; print random.uniform(95,103)")
	echo "Body temperature="$body_temp

	env_temp=$(python -S -c "import random; print random.uniform(55,85)")
	echo "Environment Temperature="$env_temp

	#Generating position (altitude) of fireman
	position=$(python -S -c "import random; print random.uniform(50,5000)")
	echo "Position="$position

	if [ "$counter" -eq $num_Connect_devices ];
	then 
		echo "Reset counter to zero"
		counter=0
	else
		echo "Increment counter"
		counter=$((counter+1))
	fi

#       if [$counter -eq num_Connect_devices-1]
#	then 
#		echo "Counter has reached max"
#		counter=0
#	else
#		echo "Ïncrement counter"
#	fi

	echo "All values to be passed to API=" $HR, $Blood_oxygen, $body_temp, $env_temp, $position

	#API CAll (Dummy)
	curl --request GET echo.jsontest.com/heartrate/$HR/Blood_O2/$Blood_oxygen

done
