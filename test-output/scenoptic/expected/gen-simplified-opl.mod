dvar int Simplified_A1 in 0..11;
dvar int Simplified_A10 in 0..11;
dvar int Simplified_A11 in 0..11;
dvar int Simplified_A2 in 0..11;
dvar int Simplified_A3 in 0..11;
dvar int Simplified_A4 in 0..11;
dvar int Simplified_A5 in 0..11;
dvar int Simplified_A6 in 0..11;
dvar int Simplified_A7 in 0..11;
dvar int Simplified_A8 in 0..11;
dvar int Simplified_A9 in 0..11;
dvar int Simplified_B1 in 0..11;
dvar int Simplified_B10 in 0..11;
dvar int Simplified_B11 in 0..11;
dvar int Simplified_B2 in 0..11;
dvar int Simplified_B3 in 0..11;
dvar int Simplified_B4 in 0..11;
dvar int Simplified_B5 in 0..11;
dvar int Simplified_B6 in 0..11;
dvar int Simplified_B7 in 0..11;
dvar int Simplified_B8 in 0..11;
dvar int Simplified_B9 in 0..11;
dvar int Simplified_E3;
dvar int Simplified_E4;
dvar int Simplified_E5;

minimize  - Simplified_E5;

subject to {
  Simplified_E5 == Simplified_E3 * 100 + Simplified_E4 * 2;
  Simplified_E3 == Simplified_A1 + Simplified_A2 + Simplified_A3 + Simplified_A4 + Simplified_A5 + Simplified_A6 + Simplified_A7 + Simplified_A8 + Simplified_A9 + Simplified_A10 + Simplified_A11;
  Simplified_E4 == Simplified_B1 + Simplified_B2 + Simplified_B3 + Simplified_B4 + Simplified_B5 + Simplified_B6 + Simplified_B7 + Simplified_B8 + Simplified_B9 + Simplified_B10 + Simplified_B11;
}
