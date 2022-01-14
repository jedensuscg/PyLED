import math
from typing import Union
import numpy as np
import bisect
from numpy.core.multiarray import array, empty
from numpy.lib.arraysetops import setdiff1d
#Power(Watts) = Volts(V) * Amps(A)
led_voltages = np.array([3,3,3,2.4,2.4])
eff_list = [.94, .82, .7, .5]
standard_resistors = [1,10,100,1000,10000,100000,1000000,1.1,11,110,1100,11000,110000,1100000,1.2,12,120,1200,12000,120000,1200000,1.3,13,130,1300,13000,130000,1300000,1.5,15,150,1500,15000,150000,1500000,1.6,16,160,1600,16000,160000,1600000,1.8,18,180,1800,18000,180000,1800000,2,20,200,2000,20000,200000,2000000,2.2,22,220,2200,22000,220000,2200000,2.4,24,240,2400,24000,240000,2400000,2.7,27,270,2700,27000,270000,2700000,3,30,300,3000,30000,300000,3000000,3.3,33,330,3300,33000,330000,3300000,3.6,36,360,3600,36000,360000,3600000,3.9,39,390,3900,39000,390000,3900000,4.3,43,430,4300,43000,430000,4300000,4.7,47,470,4700,47000,470000,4700000,5.1,51,510,5100,51000,510000,5100000,5.6,56,560,5600,56000,560000,5600000,6.2,62,620,6200,62000,620000,6200000,6.8,68,680,6800,68000,680000,6800000,7.5,75,750,7500,75000,750000,7500000,8.2,82,820,8200,82000,820000,8200000,9.1,91,910,9100,91000,910000,9100000]
sorted_resistors = sorted(standard_resistors, key = lambda x:float(x))
def boost_current_draw(volts_in: int,volts_out: Union[int,tuple,list],load_current: Union[int, float],max_efficiency: float):
#region DOCSTRING
    """The current draw of circuit accounting for boost converter draw
    Parameters
    ----------
    volts_in : int
        Voltage from the original power source
    volts_out : int or list of int or tuple of in
        Voltage required from boost converter. Total voltage if know or list of led's forward voltages.
    load_current : float or int
        The calculated current of the load
    max_efficiency : float
        The listed maximum efficiency of the boost converter
    Returns
    -------
    list
        [Total current in milliAmps, Total current in Amps]
    """
#end region
    if type(volts_out) is np.ndarray:
        volts_out = sum(volts_out)
    total_current_amps = round(load_current*volts_out/(volts_in*max_efficiency),2)
    total_current_ma = round((total_current_amps*1000))
    #print(f"Current output of boost converter: {total_current_ma} mA")
    return [total_current_ma, total_current_amps]


def Battery_Life(battery_capacity, total_load_current):
    battery_life_list = math.modf(battery_capacity / total_load_current)
    battery_life_whole_hour = int(battery_life_list[1])
    battery_life_minutes = math.floor(battery_life_list[0] * 60)
    return[battery_life_whole_hour,battery_life_minutes]
    # print(f"Battery Run Time = {battery_life_whole_hour}hours and {battery_life_minutes} minutes")


def led_layout(volts_in: Union[int, float], led_forward_volts: Union[int, float], led_count: int, led_current: float):
#region DOCSTRING
    """Prints an ASCII layout of an LED circuit with given parameters
    ----------
    volts_in : int or float
        Voltage from the original power source or boost converter
    led_forward_volts : int or float
        Rated forward voltage of the LED's being used.
    led_count : int
        number of LED's being used.
    led_current : float
        The rated current draw of the LED, in AMPS (20 mA = .02 Amps)
    """
#end region
    led = "-#-"
    total_forward_volts = led_forward_volts * led_count
    led_per_wire = divmod(volts_in,led_forward_volts)
    total_wires = divmod(led_count,led_per_wire[0])
    
    max_leds_per_wire = int(led_per_wire[0])
    full_wires_count = int(total_wires[0])
    remaining_leds = int(total_wires[1])

    print(f"Max LED's per parallel line: {max_leds_per_wire} LED's")
    print(f"Total parallel wires with max LED's: {full_wires_count} parallel wires")
    if remaining_leds > 0:
        print(f"wire with any remaining LED's: {remaining_leds}")

    for x in range(0, full_wires_count):
        resistor = get_current_limiter(volts_in,led_forward_volts,max_leds_per_wire,led_current)
        if x == 0:
            print(f"{volts_in}V-+" + led * max_leds_per_wire + f"[{resistor}\u03A9]-")
        else:
            print(' '*len(str(volts_in)) + " " + led * max_leds_per_wire + f"[{resistor}\u03A9]-")
    
    if remaining_leds > 0: 
        resistor_remain = get_current_limiter(volts_in,led_forward_volts,remaining_leds,led_current)
        print(' '*len(str(volts_in)) + " " + led * remaining_leds + f"[{resistor_remain}\u03A9]-")

def get_current_limiter(volts_in,led_forward_volts, max_leds_per_wire,led_current):
    resistor = math.ceil((volts_in - (led_forward_volts * max_leds_per_wire)) / led_current)
    if resistor == 0:
        return 1
    else:
        if not resistor in sorted_resistors:
            next_highest = sorted_resistors[bisect.bisect(sorted_resistors, resistor)]
            return next_highest
        else:
            return resistor

def led_calc(volts_in: Union[int,float], volts_out:Union[int,float], max_efficiency: float, battery_capacity: int, load_amp: float = .02, load_ma: float = 0, isBoosted: bool = False,):
    #region DOCSTRING
    """Outputs total current draw from power source, including that from boost converter. Gives battery run times.
    ----------
    volts_in : int or float
        Voltage from the original power source or boost converter
    volts_out : int or float
        Desired voltage from boost converter
    max_efficiency : float
        Max  rated efficiency of boost converter
    battery_capacity : int
        Rated capacity of battery in mAh
    load_amp: float
        Current draw of the LED's, in Amps. Default .02 Optional
    load_ma: float
        Current Current draw of the LED's, in milliAmps. Default 0. Any other numbers will override load_amp setting.
    usBoosted: bool
        Sets if the circuit is using a boost converter, or straight draw from the power source(i.e battery)
    """
#end region    
    eff_list[0] = max_efficiency
    battery_life_list = []
    length = len(eff_list)
    if load_ma != 0:
        load_amp = load_ma / 1000
        print("Ignoring load_amp value(is entered) as mA value was input")
    if isBoosted:

        for i in range(length):
            total_load_current = boost_current_draw(volts_in,volts_out,load_amp, eff_list[i])
            eff_load_ma = total_load_current[0]
            eff_load_amp = total_load_current[1]
            battery_life = Battery_Life(battery_capacity,eff_load_ma)
            battery_life_list.append([eff_load_ma,eff_load_amp,battery_life])
        print_current_msg = "Total current draw including boost converter:"
    else:
        battery_life_list.append(Battery_Life(battery_capacity,load_amp * 1000))
        print_current_msg = "Total current draw:"

    if len(battery_life_list) > 1:
        for x in range(len(battery_life_list)):
            print(f"***Boost converter efficiency of {eff_list[x] * 100}%***")
            print(f"Battery Run Time = {battery_life_list[x][2][0]}hours and {battery_life_list[x][2][1]} minutes.")
            print(f"{print_current_msg} {battery_life_list[x][0]} mA / {battery_life_list[x][1]} Amps\n")
    else:
        print(f"Battery Run Time = {battery_life_list[0][0]}hours and {battery_life_list[0][1]} minutes.")
        print(f"{print_current_msg} {load_amp * 1000} mA / {load_amp} Amps")

led_layout(16,3,8,.02)
led_calc(4.5,18,.94,750,load_ma=20,isBoosted=True)