WORK IN PROGRESS

Simple little tool I am making for help in setting up simple LED circuits. There are many calculators on the web, I am making my own for fun. It it also combining different calculations into one.

Currently is supports (though there is no menu yet, just manually running the functions or using the Jupyter notebook layout)
- Create a basic ASCII (I mean basic) layout of a circuit given parameters such as power source voltage, number of LED's, forward voltage of LED's, and current draw of LED's. Currently all LED's have to be identical.
- It can spit out estimated total current draw on the power source. If using a boost converter, it includes the draw from this as well, determined by the given input > output voltage of the boost converter. This is also used to give an estimated battery life given the battery mAh input, regardless of boost converter use.
- Total current draw can be run by itself, with the proper inputs. Running the led_layout will also run the led_calc to give current draw and battery run time.

Each of the utility functions can also be used if you don't need to run a full calculation:

- get_battery_life(battery_capacity,total_load_current): returns the run time of a battery given its mAh rating and the current draw of the circuit. Uncomment the print line to get results.
- get_current_limiter(volts_in,led_forward_volts, max_leds_per_wire,led_current): Returns the best current limiter for a given circuit branch. Includes the average 5% tolerance of most resistors. Selects the next highest standard resistor if calculated resistance is not a standard resistor. Uncomment print to see result.

### Terminal output examples
```
KEY:  
# = LED
+ = ANODE(Positive leg)
[82Ω] = Calculated Resistor
```  
Input: 4.5v, 2300 mAh batteries. 6 led's with forward voltage of 3v and current of 20mA. using a Boost converter with a rated max efficiency of 90%, and a desired output voltage of 18v. 
Ran with ```led_layout(4.5,3,6,.02,(True,18,.9),2300,)```
```
Max LED's per parallel line: 6 LED's
Total parallel wires with max LED's: 1 parallel wires
18V-+-#--#--#--#--#--#-[1Ω]-
END OF CIRCUIT

BATTERY RUN TIMES AND CURRENT DRAWS
********
***Boost converter efficiency of 90.0%***
Battery Run Time = 25hours and 33 minutes.
Total current draw including boost converter: 90 mA / 0.09 Amps

*\**Boost converter efficiency of 82.0%***
Battery Run Time = 23hours and 0 minutes.
Total current draw including boost converter: 100 mA / 0.1 Amps

*\**Boost converter efficiency of 50.0%***
Battery Run Time = 14hours and 22 minutes.
Total current draw including boost converter: 160 mA / 0.16 Amps
```
Same input as above, except use boost converter set to **FALSE** this ignoring it.
```Max LED's per parallel line: 1 LED's
Total parallel wires with max LED's: 6 parallel wires
4.5V-+-#-[82Ω]-
    -+-#-[82Ω]-
    -+-#-[82Ω]-
    -+-#-[82Ω]-
    -+-#-[82Ω]-
    -+-#-[82Ω]-
END OF CIRCUIT

BATTERY RUN TIMES AND CURRENT DRAWS
********
Battery Run Time = 19hours and 9 minutes.
Total current draw: 120 mA / 0.12 Amps```