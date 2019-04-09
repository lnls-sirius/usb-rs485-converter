#!/usr/bin/python
# -*- coding: utf-8 -*-

output_file = open("baud_rates.txt", "w")

output_file.write("FT232RL - Baud rates permitidos (bps)\r\n\r\n")
output_file.write("3000000.0\r\n")

n = 2
while (n <= 16384):
    x = 0
    while (x <= 0.875):
        output_file.write("{:0.1f}".format(3000000.0 / (n + x)) + "\r\n")
        x += 0.125
    n += 1

output_file.close()
