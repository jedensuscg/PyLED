WORK IN PROGRESS

Simple little tool I am making for help in setting up simple LED circuits. There are many calculators on the web, I am making my own for fun. It it also combining different calculations into one.

Currently is supports (though there is no menu yet, just manually running the functions or using the Jupyter notebook layout)
- Create a basic ASCII (I mean basic) layout of a circuit given parameters such as power source voltage, number of LED's, forward voltage of LED's, and current draw of LED's. Currently all LED's have to be identical.
- It can spit out estimated total current draw on the power source. If using a boost converter, it includes the draw from this as well, determined by the given input > output voltage of the boost converter. This is also used to give an estimated battery life given the battery mAh input, regardless of boost converter use.
- These two functions are not tied together. So you have to run them independently.

To run the LED Schematic, use led_layout with the required inputs. uses DOCSTRING to help.
To run the Total Current draw use the led_cal function with required inputs. isBoosted = False will ignore any boost converter input and isBoosted = True will include it.

Next up will be to pass the LED draw of the LED's directly into the battery run time calc. For now, you can just multiply the number of parallel circuits spit out by the schematic by the current draw of the LED is use. so 3 parallel circuits of 20mA LED's will draw 60 mA. Input this into the led_calc for the battery run time. 