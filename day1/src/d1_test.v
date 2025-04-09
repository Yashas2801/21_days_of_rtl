module d1_test;
  reg [7:0] a_i;
  reg [7:0] b_i;
  wire [7:0] y_o;
  reg sel_i;

  d1_design dut (
      .a_i  (a_i),
      .b_i  (b_i),
      .sel_i(sel_i),
      .y_o  (y_o)
  );

  initial begin
    #0 a_i = 0;
    b_i   = 0;
    sel_i = 0;

    #5 a_i = 8'b0011_1101;
    b_i   = 8'b1011_1101;
    sel_i = 0;

    #5 sel_i = 1;

    #5 $finish;
  end

  initial begin
    $monitor("a_i = %-b, b_i = %0b, sel_i = %0b, y_o = %0b,time = %0t", a_i, b_i, sel_i, y_o,
             $time);
  end
endmodule
