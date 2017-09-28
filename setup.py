# The whole fountain consisting of its 77 jets.
U0=range(0,77)
# The outer circle of 36 jets
U1=range(0,36)
# The even and odd jets on the outer circle
U1_EVEN=[jet for jet in U1 if jet%2==0]
U1_ODD=[jet for jet in U1 if jet%2!=0]
# The two halves of the outer circle
U1_HALF1=U1[:18]
U1_HALF2=U1[18:]
# The two triplet groups of the outer circle
U1_TRIPLETS1=[0,1,2,6,7,8,12,13,14,18,19,20,24,25,26,30,31,32]
U1_TRIPLETS2=[3,4,5,9,10,11,15,16,17,21,22,23,27,28,29,33,34,35]
# The middle circle of 36 jets
U2=range(36,72)
# The even and odd jets on the middle circle
U2_EVEN=[jet for jet in U2 if jet%2==0]
U2_ODD=[jet for jet in U2 if jet%2!=0]
# The two halves of the middle circle
U2_HALF1=U2[:18]
U2_HALF2=U2[18:]
# The two triplet groups of the middle circle
U2_TRIPLETS1=[jet+36 for jet in U1_TRIPLETS1]
U2_TRIPLETS2=[jet+36 for jet in U1_TRIPLETS2]
# The inner circle of 4 jets
U3=range(72,76)
# The two (opposite) halves of the inner circle
U3_HALF1=[72,74]
U3_HALF2=[73,75]
# The middle jet
U4=[76]
# Maximum and minimum velocities of the four units, given that that they are on
# i.e. their velocity is not 0m/s.
MAX_VELOCITIES={"U1":11.0,"U2":14.0,"U3":15.0,"U4":17.0}
MIN_VELOCITIES={"U1":6.0,"U2":8.0,"U3":10.0,"U4":12.0}
# Maximum and minimum light intensities of the four units
MAX_INTENSITIES={"U0":7.0,"U1":7.0,"U2":7.0,"U3":7.0,"U4":7.0}
MIN_INTENSITIES={"U0":4.0,"U1":4.0,"U2":4.0,"U3":4.0,"U4":4.0}

# The probability transition matrix of the scenarios.
TRANSITIONS=[
    # Intro
    [0,0,0,0.4,0.3,0.3],
    # Outro
    [0,0,0,0,0,0],
    # Chorus
    [0,0,0,0.5,0,0.5],
    # scVerse_1
    [0,0,0,0,0.5,0.5],
    # scVerse_2
    [0,0,0,0.5,0,0.5],
    # scVerse_3
    [0,0,0,0.5,0.5,0]]

# Calculate the cumulative transition matrix
CUM_TRANSITIONS=[list(row) for row in TRANSITIONS]
for i in range(0,len(TRANSITIONS)):
    for j in range(0,len(TRANSITIONS[i])):
        CUM_TRANSITIONS[i][j]=sum(TRANSITIONS[i][:j+1])

# The colors names used are found from "https://en.wikipedia.org/wiki/List_of_colors:_A-F"
# Our color groups are divided in 8 equal-sized sectors around the centre .They are
# defined by the respective boundary conditions.
# NB: (5,5) is center
COLOR_GROUPS=[
    # Top-right
    #  Aureolin rgb(0.99,0.93,0), Cadmium Orange rgb(0.93,0.53,0.18)
    {"bounds":(lambda x,y: y>=x and x>=5),"color1":{"r":0.99,"g":0.93,"b":0.0,"a":1.0},"color2":{"r":0.93,"g":0.53,"b":0.18,"a":1.0}},
    # Azure rgb(0,0.5,1), Aureolin rgb(0.99,0.93,0)
    {"bounds":(lambda x,y: y<=x and y>=5),"color1":{"r":0.0,"g":0.5,"b":1.0,"a":1.0},"color2":{"r":0.99,"g":0.93,"b":0.0,"a":1.0}},
    # Bottom-right
    # Bright Green rgb(0.4,1,0),Azure rgb(0,0.5,1)
    {"bounds":(lambda x,y: y>=-x+10 and y<=5),"color1":{"r":0.0,"g":0.5,"b":1.0,"a":1.0},"color2":{"r":0.4,"g":1.0,"b":0.0,"a":1.0}},
    # Cadmium Green rgb(0,0.42,0.24), Caribbean Green (0,0.8,0.6)
    {"bounds":(lambda x,y: y<=-x+10 and x>=5),"color1":{"r":0.0,"g":0.42,"b":0.24,"a":1.0},"color2":{"r":0.0,"g":0.8,"b":0.6,"a":1.0}},
    # Bottom-left
    # Dark Orchid rgb(0.6,0.2,0.8), Deep Mauve rgb(0.83,0.45,0.83)
    {"bounds":(lambda x,y: y<=x and x<5),"color1":{"r":0.6,"g":0.2,"b":0.8,"a":1.0},"color2":{"r":0.83,"g":0.45,"b":0.83,"a":1.0}},
    # Fresh Air rgb(0.65,0.91,1), Cyan Cobalt Blue rgb(0.16,0.35,0.61)
    {"bounds":(lambda x,y: y>=x and y<5),"color1":{"r":0.65,"g":0.91,"b":1.0,"a":1.0},"color2":{"r":0.16,"g":0.35,"b":0.61,"a":1.0}},
    # Top-left
    # Crimson Red rgb(0.6,0,0), Awesome (shade of red) rgb(1,0.13,0.32)
    {"bounds":(lambda x,y: y<=-x+10 and y>5),"color1":{"r":0.6,"g":0.0,"b":0.0,"a":1.0},"color2":{"r":1.0,"g":0.13,"b":0.32,"a":1.0}},
    # Candy Apple Red rgb(1,0.03,0), Chrome Yellow rgb(1,0.65,0)
    {"bounds":(lambda x,y: y>=-x+10 and x<5),"color1":{"r":1.0,"g":0.03,"b":0.0,"a":1.0},"color2":{"r":1.0,"g":0.65,"b":0.0,"a":1.0}}
]
