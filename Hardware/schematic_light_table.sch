EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr User 6693 4724
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:+12V #PWR?
U 1 1 5D97A415
P 1000 1850
F 0 "#PWR?" H 1000 1700 50  0001 C CNN
F 1 "+12V" H 1015 2023 50  0000 C CNN
F 2 "" H 1000 1850 50  0001 C CNN
F 3 "" H 1000 1850 50  0001 C CNN
	1    1000 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	1000 650  2500 650 
$Comp
L Device:CP 50V
U 1 1 5D980EF5
P 4000 2200
F 0 "50V" H 4118 2246 50  0000 L CNN
F 1 "CP" H 4118 2155 50  0000 L CNN
F 2 "" H 4038 2050 50  0001 C CNN
F 3 "~" H 4000 2200 50  0001 C CNN
	1    4000 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 1650 5000 1650
Wire Wire Line
	5000 1650 5000 1750
$Comp
L Device:LED 12V
U 1 1 5D98204D
P 5000 1900
F 0 "12V" V 5039 1783 50  0000 R CNN
F 1 "LED" V 4948 1783 50  0000 R CNN
F 2 "" H 5000 1900 50  0001 C CNN
F 3 "~" H 5000 1900 50  0001 C CNN
	1    5000 1900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5000 2400 5000 2450
$Comp
L Device:LED 12V
U 1 1 5D982EEF
P 5000 2600
F 0 "12V" V 5039 2483 50  0000 R CNN
F 1 "LED" V 4948 2483 50  0000 R CNN
F 2 "" H 5000 2600 50  0001 C CNN
F 3 "~" H 5000 2600 50  0001 C CNN
	1    5000 2600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1000 650  1000 2700
$Comp
L Device:LED 12V
U 1 1 5D98E5EF
P 5000 2250
F 0 "12V" V 5039 2133 50  0000 R CNN
F 1 "LED" V 4948 2133 50  0000 R CNN
F 2 "" H 5000 2250 50  0001 C CNN
F 3 "~" H 5000 2250 50  0001 C CNN
	1    5000 2250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5000 2100 5000 2050
Wire Wire Line
	1000 2700 2500 2700
Wire Wire Line
	1500 2900 4000 2900
Wire Wire Line
	5000 2750 5000 2900
Wire Wire Line
	4000 2350 4000 2900
Connection ~ 4000 2900
Wire Wire Line
	4000 2900 5000 2900
Wire Wire Line
	4000 1650 4000 2050
Wire Wire Line
	1500 1650 1500 2900
$Comp
L Device:D_Bridge_+-AA 1000V
U 1 1 5D998817
P 2500 1650
F 0 "1000V" H 2844 1696 50  0000 L CNN
F 1 "D_Bridge_+-AA" H 2844 1605 50  0000 L CNN
F 2 "" H 2500 1650 50  0001 C CNN
F 3 "~" H 2500 1650 50  0001 C CNN
	1    2500 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 650  2500 1350
Wire Wire Line
	2200 1650 1500 1650
Wire Wire Line
	2500 1950 2500 2700
Wire Wire Line
	4000 1650 2800 1650
Connection ~ 4000 1650
$EndSCHEMATC
