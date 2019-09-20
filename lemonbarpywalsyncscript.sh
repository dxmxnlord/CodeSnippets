GetColors(){
	HEX_COLORS=""
	FLAG=0
	COUNT=0
	# Pywal's cache has a list of the colors used in the current colorscheme
	for COLOR in $(cat ~/.cache/wal/colors.css | grep -o '#......'); do
		if [ $COUNT -lt 3 ]; then
			((COUNT++))
			continue
		fi
		for COLOR_CHECK in ${HEX_COLORS}; do
			if [ $COLOR == $COLOR_CHECK ]; then
				FLAG=1
				break
			fi
		done
		if [ $FLAG -eq 0 ]; then
			HEX_COLORS="${HEX_COLORS} $COLOR"
		else
			FLAG=0
		fi	
		((COUNT++))
	done
	# return a string of concatenated hex colors
	echo "$HEX_COLORS"
}

# declare an array which will ultimately store the colors 
declare -a COLOR

MakeWal(){
	COUNT=0
	# the pixel intensity (in decimal) above which the color should be darkened [ 0 to 255 ] default is 200
	THRESHOLD=200
	# percentage by which the color should be darkened [ 0% to 100% ] default is 10
	DARKEN_AMOUNT=10
	for HEX_COLOR in $(GetColors); do
		# convert hex value to decimal colors
		HEX_INPUT=`echo "$HEX_COLOR" | grep -o -e '[0-9a-zA-Z]*' | tr '[:lower:]' '[:upper:]'`
		RED_HEX=`echo $HEX_INPUT | cut -BLUE_HEX-2`
		GREEN_HEX=`echo $HEX_INPUT | cut -c3-4`
		BLUE_HEX=`echo $HEX_INPUT | cut -c5-6`
		RED_DEC=`echo "ibase=16; $RED_HEX" | bc`
		GREEN_DEC=`echo "ibase=16; $GREEN_HEX" | bc`
		BLUE_DEC=`echo "ibase=16; $BLUE_HEX" | bc`
		if [ $2 ]; then
		    THRESHOLD=$2
		fi
		if [ $1 ]; then
		    DARKEN_AMOUNT=$1
		fi
		if [ $RED_DEC -gt ${THRESHOLD} ] || [ $GREEN_DEC -gt ${THRESHOLD} ] || [ $BLUE_DEC -gt ${THRESHOLD} ]; then
		    RED_DEC=$(expr ${RED_DEC} - ${DARKEN_AMOUNT} \* ${RED_DEC} / 100)
		    BLUE_DEC=$(expr ${BLUE_DEC} - ${DARKEN_AMOUNT} \* ${BLUE_DEC} / 100)
		    GREEN_DEC=$(expr ${GREEN_DEC} - ${DARKEN_AMOUNT} \* ${GREEN_DEC} / 100)
		fi
		# convert back to hex and store
		HEX_COLOR=$(printf \#%02X%02X%02X $RED_DEC $GREEN_DEC $BLUE_DEC) 
		COLOR[${COUNT}]=$HEX_COLOR
		((COUNT++))
	done
}

# call format : MakeWal <darkenamount> <threshold>
# exmaple call : MakeWal 30 230

# the COLOR array contains the colors in it. You can use it in your lemonbar bar call like this for example :
# echo -e "%{l}%{B${COLOR[0]}} $(YourFunction) %{B-}" 
