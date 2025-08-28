dvar int Complex_expressions_A1 in 0..11;
dvar int Complex_expressions_A10 in 0..11;
dvar int Complex_expressions_A11 in 0..11;
dvar int Complex_expressions_A2 in 0..11;
dvar int Complex_expressions_A3 in 0..11;
dvar int Complex_expressions_A4 in 0..11;
dvar int Complex_expressions_A5 in 0..11;
dvar int Complex_expressions_A6 in 0..11;
dvar int Complex_expressions_A7 in 0..11;
dvar int Complex_expressions_A8 in 0..11;
dvar int Complex_expressions_A9 in 0..11;
dvar int Complex_expressions_B1 in 0..11;
dvar int Complex_expressions_B10 in 0..11;
dvar int Complex_expressions_B11 in 0..11;
dvar int Complex_expressions_B2 in 0..11;
dvar int Complex_expressions_B3 in 0..11;
dvar int Complex_expressions_B4 in 0..11;
dvar int Complex_expressions_B5 in 0..11;
dvar int Complex_expressions_B6 in 0..11;
dvar int Complex_expressions_B7 in 0..11;
dvar int Complex_expressions_B8 in 0..11;
dvar int Complex_expressions_B9 in 0..11;
dvar int Complex_expressions_E1;

minimize  - Complex_expressions_E1;

subject to {
  Complex_expressions_E1 == (Complex_expressions_A1 + Complex_expressions_A2 + Complex_expressions_A3 + Complex_expressions_A4 + Complex_expressions_A5 + Complex_expressions_A6 + Complex_expressions_A7 + Complex_expressions_A8 + Complex_expressions_A9 + Complex_expressions_A10 + Complex_expressions_A11) * 100 + (Complex_expressions_B1 + Complex_expressions_B2 + Complex_expressions_B3 + Complex_expressions_B4 + Complex_expressions_B5 + Complex_expressions_B6 + Complex_expressions_B7 + Complex_expressions_B8 + Complex_expressions_B9 + Complex_expressions_B10 + Complex_expressions_B11) * 2;
}
