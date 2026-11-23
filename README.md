## Neural Net
My handmade neural network program. Can build and traverse arbitrary graph structures.

## Features
    * Supports arbitrary graph structures and runtime modification.
    * Allows for flexible swapping between activation functions, evaluation functions, and optimizer functions.
    * Supports file saving and loading, so data can be used later.
    * Built using only the standard Python library
    * Thorough testing suite

## Technologies
    * Python for portability

## Usage
Clone the repo using 'git clone https://github.com/OnetrueMaple/Neural-Net' and use the functions to build whatever you like.
Do be aware that autodiff is broken at the moment, only single neurons can learn a function.

## Preview
```
user@User:~$ python3 testmain.py
Initial network values are: Target=6.0
modelID        =
version        = 0.3
activation     = <function linear at 0x7cca68c5ede0>
evaluator      = <function basic at 0x7cca68c5ef20>
solver         = <function autodiff at 0x7cca68c5f060>
node ids       = [0, -1]
start          = [-1]
end            = [0]
currents       = [-1]
currentDepth   = 0
base_precision = -2
base_modifier  = 0
precision      = -2
learning_rate  = 1.2
node_data={'id': 0, 'out': [], 'inc': [-1], 'inputs': 0.0, 'output': 0.0, 'weights': {-1: -0.37611}, 'bias': 0.12991}
node_data={'id': -1, 'out': [0], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0}
---------------------------------
loop=1
ID    =0 |-----------------
Input =-0.977164 |
Weight={-1: -0.325721376} |
Bias  =0.146706
Output=-0.830458 |
Target=6.000000 |
---------------------------------------------
loop=2
ID    =0 |-----------------
Input =-0.829626 |
Weight={-1: -0.276542078976} |
Bias  =0.163099
Output=-0.666527 |
Target=6.000000 |
---------------------------------------------
loop=3
ID    =0 |-----------------
Input =-0.685629 |
Weight={-1: -0.22854308508057603} |
Bias  =0.179099
Output=-0.506530 |
Target=6.000000 |
---------------------------------------------
loop=4
ID    =0 |-----------------
Input =-0.545088 |
Weight={-1: -0.1816960670386422} |
Bias  =0.194715
Output=-0.350374 |
Target=6.000000 |
---------------------------------------------
loop=5
ID    =0 |-----------------
Input =-0.407920 |
Weight={-1: -0.13597337742971477} |
Bias  =0.209956
Output=-0.197965 |
Target=6.000000 |
---------------------------------------------
loop=6
ID    =0 |-----------------
Input =-0.274044 |
Weight={-1: -0.0913480323714016} |
Bias  =0.224831
Output=-0.049213 |
Target=6.000000 |
---------------------------------------------
loop=7
ID    =0 |-----------------
Input =-0.143381 |
Weight={-1: -0.047793695594487956} |
Bias  =0.239349
Output=0.095968 |
Target=6.000000 |
---------------------------------------------
loop=8
ID    =0 |-----------------
Input =1.131890 |
Weight={-1: 0.37729663134818914} |
Bias  =0.381046
Output=1.512935 |
Target=6.000000 |
---------------------------------------------
loop=9
ID    =0 |-----------------
Input =2.101096 |
Weight={-1: 0.7003652798246238} |
Bias  =0.488735
Output=2.589831 |
Target=6.000000 |
---------------------------------------------
loop=10
ID    =0 |-----------------
Input =2.837692 |
Weight={-1: 0.9458974526667141} |
Bias  =0.570579
Output=3.408272 |
Target=6.000000 |
---------------------------------------------
loop=11
ID    =0 |-----------------
Input =3.397506 |
Weight={-1: 1.1325019040267028} |
Bias  =0.632781
Output=4.030286 |
Target=6.000000 |
---------------------------------------------
loop=12
ID    =0 |-----------------
Input =3.822964 |
Weight={-1: 1.2743212870602942} |
Bias  =0.680054
Output=4.503018 |
Target=6.000000 |
---------------------------------------------
loop=13
ID    =0 |-----------------
Input =4.146312 |
Weight={-1: 1.3821040181658237} |
Bias  =0.715981
Output=4.862293 |
Target=6.000000 |
---------------------------------------------
loop=14
ID    =0 |-----------------
Input =4.392057 |
Weight={-1: 1.464018893806026} |
Bias  =0.743286
Output=5.135343 |
Target=6.000000 |
---------------------------------------------
loop=15
ID    =0 |-----------------
Input =4.578823 |
Weight={-1: 1.5262741992925797} |
Bias  =0.764038
Output=5.342861 |
Target=6.000000 |
---------------------------------------------
loop=16
ID    =0 |-----------------
Input =4.720765 |
Weight={-1: 1.5735882314623606} |
Bias  =0.779809
Output=5.500574 |
Target=6.000000 |
---------------------------------------------
loop=17
ID    =0 |-----------------
Input =4.828641 |
Weight={-1: 1.609546895911394} |
Bias  =0.791796
Output=5.620436 |
Target=6.000000 |
---------------------------------------------
loop=18
ID    =0 |-----------------
Input =4.910626 |
Weight={-1: 1.6368754808926596} |
Bias  =0.800905
Output=5.711532 |
Target=6.000000 |
---------------------------------------------
loop=19
ID    =0 |-----------------
Input =4.972936 |
Weight={-1: 1.6576452054784212} |
Bias  =0.807828
Output=5.780764 |
Target=6.000000 |
---------------------------------------------
loop=20
ID    =0 |-----------------
Input =5.020291 |
Weight={-1: 1.6734301961636002} |
Bias  =0.813090
Output=5.833381 |
Target=6.000000 |
---------------------------------------------
loop=21
ID    =0 |-----------------
Input =5.056280 |
Weight={-1: 1.6854267890843362} |
Bias  =0.817089
Output=5.873369 |
Target=6.000000 |
---------------------------------------------
loop=22
ID    =0 |-----------------
Input =5.083633 |
Weight={-1: 1.6945441997040955} |
Bias  =0.820128
Output=5.903761 |
Target=6.000000 |
---------------------------------------------
loop=23
ID    =0 |-----------------
Input =5.104420 |
Weight={-1: 1.7014734317751126} |
Bias  =0.822438
Output=5.926858 |
Target=6.000000 |
---------------------------------------------
loop=24
ID    =0 |-----------------
Input =5.120219 |
Weight={-1: 1.7067396481490855} |
Bias  =0.824193
Output=5.944412 |
Target=6.000000 |
---------------------------------------------
loop=25
ID    =0 |-----------------
Input =5.132226 |
Weight={-1: 1.710741972593305} |
Bias  =0.825527
Output=5.957753 |
Target=6.000000 |
---------------------------------------------
loop=26
ID    =0 |-----------------
Input =5.141351 |
Weight={-1: 1.7137837391709119} |
Bias  =0.826541
Output=5.967892 |
Target=6.000000 |
---------------------------------------------
loop=27
ID    =0 |-----------------
Input =5.148286 |
Weight={-1: 1.716095481769893} |
Bias  =0.827312
Output=5.975598 |
Target=6.000000 |
---------------------------------------------
loop=28
ID    =0 |-----------------
Input =5.153557 |
Weight={-1: 1.7178524061451186} |
Bias  =0.827897
Output=5.981455 |
Target=6.000000 |
---------------------------------------------
loop=29
ID    =0 |-----------------
Input =5.157563 |
Weight={-1: 1.71918766867029} |
Bias  =0.828343
Output=5.985906 |
Target=6.000000 |
---------------------------------------------
loop=30
ID    =0 |-----------------
Input =5.160607 |
Weight={-1: 1.7202024681894204} |
Bias  =0.828681
Output=5.989288 |
Target=6.000000 |
---------------------------------------------
loop=31
ID    =0 |-----------------
Input =5.162921 |
Weight={-1: 1.7209737158239595} |
Bias  =0.828938
Output=5.991859 |
Target=6.000000 |
---------------------------------------------
Finished after 32 cycles! Network values are: Target=6.0
modelID        =
version        = 0.3
activation     = <function linear at 0x7cca68c5ede0>
evaluator      = <function basic at 0x7cca68c5ef20>
solver         = <function autodiff at 0x7cca68c5f060>
node ids       = [0, -1]
start          = [-1]
end            = [0]
currents       = []
currentDepth   = 2
base_precision = -2
base_modifier  = 0
precision      = -2
learning_rate  = 1.2
node_data={'id': 0, 'out': [], 'inc': [-1], 'inputs': 5.16292, 'output': 5.99186, 'weights': {-1: 1.7209737158239595}, 'bias': 0.82894}
node_data={'id': -1, 'out': [0], 'inc': [], 'inputs': 0.0, 'output': 3.0, 'weights': {}, 'bias': 0.0}
```
