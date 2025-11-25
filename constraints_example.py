from z3 import *

in1_p = Real('in1_p')
in2_p = Real('in2_p')
in3_p = Real('in3_p')
in4_p = Real('in4_p')
asm1_spd = Real('asm1_spd')
asm2_spd = Real('asm2_spd')


SOURCE_P = 100
IN_P1 = 0.5
IN_P2 = 0.75 # TODO: adjust these!
IN_P3 = 1.5
ASM_S1 = 0.5
ASM_S2 = 0.75 # TODO: adjust these!
ASM_S3 = 1.25

ASM1_R1 = 1 # quantity for asm1 recipe ingredient 1, etc.
ASM1_R2 = 1
ASM1_RT = 0.1 # time for asm1 recipe

ASM2_R1 = 1
ASM2_R2 = 1
ASM2_RT = 0.5


# Solver.
s = Optimize()

# in1 constraints
s.add(Or(in1_p == IN_P1, in1_p == IN_P2, in1_p == IN_P3, in1_p == SOURCE_P))
s.add(in1_p <= SOURCE_P)
s.add(in1_p <= IN_P3)

# in2 constraints
s.add(Or(in2_p == IN_P1, in2_p == IN_P2, in2_p == IN_P3, in2_p <= SOURCE_P))
s.add(in2_p <= SOURCE_P)
s.add(in2_p <= IN_P3)

# asm1 constraints
s.add(Or(asm1_spd == ASM_S1, asm1_spd == ASM_S2, asm1_spd == ASM_S3))
s.add(in1_p >= ASM1_R1 * asm1_spd / ASM1_RT)
s.add(in2_p >= ASM1_R2 * asm1_spd / ASM1_RT)


# in3 constraints
s.add(Or(in3_p == IN_P1, in3_p == IN_P2, in3_p == IN_P3, in3_p == SOURCE_P))
s.add(in3_p <= SOURCE_P)
s.add(in3_p <= IN_P3)

# in4 constraints
s.add(Or(in4_p == IN_P1, in4_p == IN_P2, in4_p == IN_P3, in4_p == SOURCE_P))
s.add(in4_p <= SOURCE_P)
s.add(in4_p <= IN_P3)

# asm4 constraints
s.add(Or(asm2_spd == ASM_S1, asm2_spd == ASM_S2, asm2_spd == ASM_S3))
s.add(in3_p >= ASM2_R1 * asm2_spd / ASM2_RT)
s.add(in4_p >= ASM2_R2 * asm2_spd / ASM2_RT)

# Minimize all of the production rates. TODO: what order should these
# calls be in?
s.minimize(in1_p)
s.minimize(in2_p)
s.minimize(in3_p)
s.minimize(in4_p)
s.minimize(asm1_spd)
s.minimize(asm2_spd)

res = s.check()
print(res)
m = s.model()
print(f"in1_p: {m[in1_p]}") 
print(f"in2_p: {m[in2_p]}")
print(f"in3_p: {m[in3_p]}")
print(f"in4_p: {m[in4_p]}")
print(f"asm1_spd: {m[asm1_spd]}")
print(f"asm2_spd: {m[asm2_spd]}")
