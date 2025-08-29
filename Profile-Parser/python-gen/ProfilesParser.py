# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Profiles.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,58,511,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,1,0,
        1,0,1,0,1,1,1,1,1,1,1,1,3,1,74,8,1,1,1,1,1,3,1,78,8,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,109,8,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,125,8,1,1,1,1,
        1,3,1,129,8,1,1,1,1,1,1,1,1,1,3,1,135,8,1,1,1,1,1,5,1,139,8,1,10,
        1,12,1,142,9,1,1,2,1,2,1,2,1,2,1,2,5,2,149,8,2,10,2,12,2,152,9,2,
        1,2,3,2,155,8,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,166,8,2,
        10,2,12,2,169,9,2,1,2,3,2,172,8,2,1,2,1,2,1,2,1,2,1,2,3,2,179,8,
        2,1,3,1,3,3,3,183,8,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,5,4,192,8,4,10,
        4,12,4,195,9,4,1,4,3,4,198,8,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,206,8,
        4,1,5,3,5,209,8,5,1,5,1,5,1,6,1,6,1,6,1,6,3,6,217,8,6,1,6,1,6,1,
        6,1,6,5,6,223,8,6,10,6,12,6,226,9,6,1,6,1,6,3,6,230,8,6,1,6,3,6,
        233,8,6,1,7,1,7,1,7,3,7,238,8,7,1,7,3,7,241,8,7,3,7,243,8,7,1,7,
        1,7,1,7,1,7,5,7,249,8,7,10,7,12,7,252,9,7,1,7,1,7,1,8,1,8,1,8,5,
        8,259,8,8,10,8,12,8,262,9,8,1,8,1,8,1,9,1,9,1,9,3,9,269,8,9,1,9,
        1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,3,11,284,
        8,11,1,11,3,11,287,8,11,1,11,1,11,1,11,5,11,292,8,11,10,11,12,11,
        295,9,11,1,11,1,11,3,11,299,8,11,1,11,3,11,302,8,11,1,11,1,11,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,313,8,11,1,11,1,11,1,11,3,
        11,318,8,11,1,11,1,11,3,11,322,8,11,3,11,324,8,11,1,12,3,12,327,
        8,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,3,12,339,
        8,12,1,13,1,13,1,13,1,13,1,14,1,14,1,14,3,14,348,8,14,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,3,14,358,8,14,1,15,1,15,1,16,1,16,
        3,16,364,8,16,1,16,1,16,3,16,368,8,16,1,16,1,16,1,16,1,16,3,16,374,
        8,16,1,16,1,16,1,16,1,16,3,16,380,8,16,1,16,1,16,1,16,1,16,1,16,
        3,16,387,8,16,1,17,1,17,3,17,391,8,17,1,17,1,17,1,17,1,18,3,18,397,
        8,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,405,8,18,1,19,1,19,1,20,
        1,20,1,21,1,21,1,22,1,22,1,22,1,22,5,22,417,8,22,10,22,12,22,420,
        9,22,1,22,1,22,1,23,1,23,1,23,5,23,427,8,23,10,23,12,23,430,9,23,
        1,23,3,23,433,8,23,1,23,1,23,1,23,1,24,1,24,1,24,5,24,441,8,24,10,
        24,12,24,444,9,24,1,24,3,24,447,8,24,1,24,1,24,1,24,1,25,1,25,1,
        25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,3,25,463,8,25,1,25,1,
        25,1,25,1,25,1,25,1,25,5,25,471,8,25,10,25,12,25,474,9,25,1,26,1,
        26,1,26,1,26,1,26,3,26,481,8,26,1,27,1,27,1,27,1,27,1,28,1,28,3,
        28,489,8,28,1,29,3,29,492,8,29,1,29,4,29,495,8,29,11,29,12,29,496,
        1,30,4,30,500,8,30,11,30,12,30,501,1,31,3,31,505,8,31,1,31,1,31,
        1,32,1,32,1,32,0,2,2,50,33,0,2,4,6,8,10,12,14,16,18,20,22,24,26,
        28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,0,11,2,
        0,8,8,11,11,1,0,13,18,1,0,1,2,1,0,24,25,1,0,15,16,2,0,27,27,30,30,
        2,0,4,4,31,31,1,0,38,39,1,0,43,44,1,0,45,46,2,0,12,12,50,51,566,
        0,66,1,0,0,0,2,124,1,0,0,0,4,178,1,0,0,0,6,180,1,0,0,0,8,205,1,0,
        0,0,10,208,1,0,0,0,12,212,1,0,0,0,14,234,1,0,0,0,16,255,1,0,0,0,
        18,265,1,0,0,0,20,273,1,0,0,0,22,323,1,0,0,0,24,326,1,0,0,0,26,340,
        1,0,0,0,28,357,1,0,0,0,30,359,1,0,0,0,32,386,1,0,0,0,34,388,1,0,
        0,0,36,404,1,0,0,0,38,406,1,0,0,0,40,408,1,0,0,0,42,410,1,0,0,0,
        44,412,1,0,0,0,46,423,1,0,0,0,48,437,1,0,0,0,50,462,1,0,0,0,52,480,
        1,0,0,0,54,482,1,0,0,0,56,488,1,0,0,0,58,491,1,0,0,0,60,499,1,0,
        0,0,62,504,1,0,0,0,64,508,1,0,0,0,66,67,3,2,1,0,67,68,5,0,0,1,68,
        1,1,0,0,0,69,70,6,1,-1,0,70,71,3,50,25,0,71,73,3,30,15,0,72,74,5,
        4,0,0,73,72,1,0,0,0,73,74,1,0,0,0,74,77,1,0,0,0,75,76,5,5,0,0,76,
        78,5,6,0,0,77,75,1,0,0,0,77,78,1,0,0,0,78,79,1,0,0,0,79,80,3,52,
        26,0,80,125,1,0,0,0,81,82,3,50,25,0,82,83,3,4,2,0,83,84,3,50,25,
        0,84,125,1,0,0,0,85,86,3,50,25,0,86,87,3,6,3,0,87,125,1,0,0,0,88,
        89,3,50,25,0,89,90,3,32,16,0,90,91,3,50,25,0,91,125,1,0,0,0,92,93,
        3,50,25,0,93,94,3,36,18,0,94,95,3,50,25,0,95,96,5,7,0,0,96,97,3,
        50,25,0,97,125,1,0,0,0,98,99,3,50,25,0,99,100,3,30,15,0,100,101,
        5,8,0,0,101,102,3,50,25,0,102,103,5,2,0,0,103,104,3,50,25,0,104,
        125,1,0,0,0,105,106,3,50,25,0,106,108,3,30,15,0,107,109,5,4,0,0,
        108,107,1,0,0,0,108,109,1,0,0,0,109,110,1,0,0,0,110,111,5,7,0,0,
        111,112,3,44,22,0,112,125,1,0,0,0,113,114,5,4,0,0,114,125,3,2,1,
        7,115,125,3,12,6,0,116,125,3,22,11,0,117,125,3,14,7,0,118,125,3,
        16,8,0,119,125,3,20,10,0,120,121,5,9,0,0,121,122,3,2,1,0,122,123,
        5,10,0,0,123,125,1,0,0,0,124,69,1,0,0,0,124,81,1,0,0,0,124,85,1,
        0,0,0,124,88,1,0,0,0,124,92,1,0,0,0,124,98,1,0,0,0,124,105,1,0,0,
        0,124,113,1,0,0,0,124,115,1,0,0,0,124,116,1,0,0,0,124,117,1,0,0,
        0,124,118,1,0,0,0,124,119,1,0,0,0,124,120,1,0,0,0,125,140,1,0,0,
        0,126,128,10,16,0,0,127,129,5,1,0,0,128,127,1,0,0,0,128,129,1,0,
        0,0,129,130,1,0,0,0,130,131,5,2,0,0,131,139,3,2,1,17,132,134,10,
        15,0,0,133,135,5,1,0,0,134,133,1,0,0,0,134,135,1,0,0,0,135,136,1,
        0,0,0,136,137,5,3,0,0,137,139,3,2,1,16,138,126,1,0,0,0,138,132,1,
        0,0,0,139,142,1,0,0,0,140,138,1,0,0,0,140,141,1,0,0,0,141,3,1,0,
        0,0,142,140,1,0,0,0,143,179,3,56,28,0,144,145,5,9,0,0,145,150,3,
        56,28,0,146,147,5,1,0,0,147,149,3,56,28,0,148,146,1,0,0,0,149,152,
        1,0,0,0,150,148,1,0,0,0,150,151,1,0,0,0,151,154,1,0,0,0,152,150,
        1,0,0,0,153,155,5,1,0,0,154,153,1,0,0,0,154,155,1,0,0,0,155,156,
        1,0,0,0,156,157,5,2,0,0,157,158,3,56,28,0,158,159,1,0,0,0,159,160,
        5,10,0,0,160,179,1,0,0,0,161,162,5,9,0,0,162,167,3,56,28,0,163,164,
        5,1,0,0,164,166,3,56,28,0,165,163,1,0,0,0,166,169,1,0,0,0,167,165,
        1,0,0,0,167,168,1,0,0,0,168,171,1,0,0,0,169,167,1,0,0,0,170,172,
        5,1,0,0,171,170,1,0,0,0,171,172,1,0,0,0,172,173,1,0,0,0,173,174,
        5,3,0,0,174,175,3,56,28,0,175,176,1,0,0,0,176,177,5,10,0,0,177,179,
        1,0,0,0,178,143,1,0,0,0,178,144,1,0,0,0,178,161,1,0,0,0,179,5,1,
        0,0,0,180,182,3,30,15,0,181,183,5,4,0,0,182,181,1,0,0,0,182,183,
        1,0,0,0,183,184,1,0,0,0,184,185,3,56,28,0,185,7,1,0,0,0,186,187,
        3,10,5,0,187,188,7,0,0,0,188,193,3,50,25,0,189,190,5,1,0,0,190,192,
        3,50,25,0,191,189,1,0,0,0,192,195,1,0,0,0,193,191,1,0,0,0,193,194,
        1,0,0,0,194,197,1,0,0,0,195,193,1,0,0,0,196,198,5,1,0,0,197,196,
        1,0,0,0,197,198,1,0,0,0,198,199,1,0,0,0,199,200,5,2,0,0,200,201,
        3,50,25,0,201,206,1,0,0,0,202,203,5,54,0,0,203,204,5,11,0,0,204,
        206,3,50,25,0,205,186,1,0,0,0,205,202,1,0,0,0,206,9,1,0,0,0,207,
        209,5,12,0,0,208,207,1,0,0,0,208,209,1,0,0,0,209,210,1,0,0,0,210,
        211,7,1,0,0,211,11,1,0,0,0,212,213,5,19,0,0,213,216,3,30,15,0,214,
        217,5,20,0,0,215,217,3,64,32,0,216,214,1,0,0,0,216,215,1,0,0,0,216,
        217,1,0,0,0,217,218,1,0,0,0,218,219,3,62,31,0,219,224,5,52,0,0,220,
        221,7,2,0,0,221,223,5,52,0,0,222,220,1,0,0,0,223,226,1,0,0,0,224,
        222,1,0,0,0,224,225,1,0,0,0,225,229,1,0,0,0,226,224,1,0,0,0,227,
        228,5,7,0,0,228,230,3,50,25,0,229,227,1,0,0,0,229,230,1,0,0,0,230,
        232,1,0,0,0,231,233,3,26,13,0,232,231,1,0,0,0,232,233,1,0,0,0,233,
        13,1,0,0,0,234,235,3,50,25,0,235,242,5,21,0,0,236,238,5,20,0,0,237,
        236,1,0,0,0,237,238,1,0,0,0,238,243,1,0,0,0,239,241,3,64,32,0,240,
        239,1,0,0,0,240,241,1,0,0,0,241,243,1,0,0,0,242,237,1,0,0,0,242,
        240,1,0,0,0,243,244,1,0,0,0,244,245,3,62,31,0,245,250,5,52,0,0,246,
        247,7,2,0,0,247,249,5,52,0,0,248,246,1,0,0,0,249,252,1,0,0,0,250,
        248,1,0,0,0,250,251,1,0,0,0,251,253,1,0,0,0,252,250,1,0,0,0,253,
        254,3,26,13,0,254,15,1,0,0,0,255,260,3,18,9,0,256,257,5,2,0,0,257,
        259,3,18,9,0,258,256,1,0,0,0,259,262,1,0,0,0,260,258,1,0,0,0,260,
        261,1,0,0,0,261,263,1,0,0,0,262,260,1,0,0,0,263,264,3,26,13,0,264,
        17,1,0,0,0,265,266,3,50,25,0,266,268,5,21,0,0,267,269,5,22,0,0,268,
        267,1,0,0,0,268,269,1,0,0,0,269,270,1,0,0,0,270,271,3,62,31,0,271,
        272,5,52,0,0,272,19,1,0,0,0,273,274,3,50,25,0,274,275,5,21,0,0,275,
        276,5,22,0,0,276,277,3,62,31,0,277,278,5,52,0,0,278,21,1,0,0,0,279,
        280,5,23,0,0,280,283,7,3,0,0,281,284,5,20,0,0,282,284,3,64,32,0,
        283,281,1,0,0,0,283,282,1,0,0,0,283,284,1,0,0,0,284,286,1,0,0,0,
        285,287,3,62,31,0,286,285,1,0,0,0,286,287,1,0,0,0,287,288,1,0,0,
        0,288,293,5,52,0,0,289,290,7,2,0,0,290,292,5,52,0,0,291,289,1,0,
        0,0,292,295,1,0,0,0,293,291,1,0,0,0,293,294,1,0,0,0,294,298,1,0,
        0,0,295,293,1,0,0,0,296,297,5,7,0,0,297,299,3,50,25,0,298,296,1,
        0,0,0,298,299,1,0,0,0,299,301,1,0,0,0,300,302,3,26,13,0,301,300,
        1,0,0,0,301,302,1,0,0,0,302,303,1,0,0,0,303,304,5,1,0,0,304,324,
        3,2,1,0,305,306,5,26,0,0,306,307,3,62,31,0,307,312,5,52,0,0,308,
        309,5,11,0,0,309,313,3,50,25,0,310,311,5,7,0,0,311,313,3,44,22,0,
        312,308,1,0,0,0,312,310,1,0,0,0,313,314,1,0,0,0,314,315,5,27,0,0,
        315,321,3,4,2,0,316,318,5,1,0,0,317,316,1,0,0,0,317,318,1,0,0,0,
        318,319,1,0,0,0,319,320,5,2,0,0,320,322,3,2,1,0,321,317,1,0,0,0,
        321,322,1,0,0,0,322,324,1,0,0,0,323,279,1,0,0,0,323,305,1,0,0,0,
        324,23,1,0,0,0,325,327,3,64,32,0,326,325,1,0,0,0,326,327,1,0,0,0,
        327,328,1,0,0,0,328,329,7,4,0,0,329,330,5,11,0,0,330,331,3,50,25,
        0,331,332,5,23,0,0,332,333,5,24,0,0,333,334,3,62,31,0,334,335,5,
        52,0,0,335,336,5,7,0,0,336,338,3,50,25,0,337,339,3,26,13,0,338,337,
        1,0,0,0,338,339,1,0,0,0,339,25,1,0,0,0,340,341,5,28,0,0,341,342,
        5,29,0,0,342,343,3,2,1,0,343,27,1,0,0,0,344,347,5,9,0,0,345,348,
        3,46,23,0,346,348,3,48,24,0,347,345,1,0,0,0,347,346,1,0,0,0,348,
        349,1,0,0,0,349,350,5,10,0,0,350,351,5,11,0,0,351,352,3,50,25,0,
        352,358,1,0,0,0,353,354,3,58,29,0,354,355,5,11,0,0,355,356,3,50,
        25,0,356,358,1,0,0,0,357,344,1,0,0,0,357,353,1,0,0,0,358,29,1,0,
        0,0,359,360,7,5,0,0,360,31,1,0,0,0,361,363,3,30,15,0,362,364,7,6,
        0,0,363,362,1,0,0,0,363,364,1,0,0,0,364,367,1,0,0,0,365,368,3,38,
        19,0,366,368,3,40,20,0,367,365,1,0,0,0,367,366,1,0,0,0,368,369,1,
        0,0,0,369,373,5,32,0,0,370,371,5,3,0,0,371,372,5,5,0,0,372,374,5,
        6,0,0,373,370,1,0,0,0,373,374,1,0,0,0,374,387,1,0,0,0,375,376,3,
        30,15,0,376,379,5,33,0,0,377,380,5,34,0,0,378,380,5,35,0,0,379,377,
        1,0,0,0,379,378,1,0,0,0,380,387,1,0,0,0,381,387,3,34,17,0,382,383,
        3,30,15,0,383,384,5,20,0,0,384,385,5,36,0,0,385,387,1,0,0,0,386,
        361,1,0,0,0,386,375,1,0,0,0,386,381,1,0,0,0,386,382,1,0,0,0,387,
        33,1,0,0,0,388,390,3,30,15,0,389,391,5,4,0,0,390,389,1,0,0,0,390,
        391,1,0,0,0,391,392,1,0,0,0,392,393,5,5,0,0,393,394,5,6,0,0,394,
        35,1,0,0,0,395,397,5,37,0,0,396,395,1,0,0,0,396,397,1,0,0,0,397,
        398,1,0,0,0,398,405,7,7,0,0,399,405,5,40,0,0,400,401,3,30,15,0,401,
        402,5,41,0,0,402,403,5,42,0,0,403,405,1,0,0,0,404,396,1,0,0,0,404,
        399,1,0,0,0,404,400,1,0,0,0,405,37,1,0,0,0,406,407,7,8,0,0,407,39,
        1,0,0,0,408,409,7,9,0,0,409,41,1,0,0,0,410,411,5,53,0,0,411,43,1,
        0,0,0,412,413,5,47,0,0,413,418,3,50,25,0,414,415,5,1,0,0,415,417,
        3,50,25,0,416,414,1,0,0,0,417,420,1,0,0,0,418,416,1,0,0,0,418,419,
        1,0,0,0,419,421,1,0,0,0,420,418,1,0,0,0,421,422,5,48,0,0,422,45,
        1,0,0,0,423,428,3,58,29,0,424,425,5,1,0,0,425,427,3,58,29,0,426,
        424,1,0,0,0,427,430,1,0,0,0,428,426,1,0,0,0,428,429,1,0,0,0,429,
        432,1,0,0,0,430,428,1,0,0,0,431,433,5,1,0,0,432,431,1,0,0,0,432,
        433,1,0,0,0,433,434,1,0,0,0,434,435,5,2,0,0,435,436,3,58,29,0,436,
        47,1,0,0,0,437,442,3,58,29,0,438,439,5,1,0,0,439,441,3,58,29,0,440,
        438,1,0,0,0,441,444,1,0,0,0,442,440,1,0,0,0,442,443,1,0,0,0,443,
        446,1,0,0,0,444,442,1,0,0,0,445,447,5,1,0,0,446,445,1,0,0,0,446,
        447,1,0,0,0,447,448,1,0,0,0,448,449,5,3,0,0,449,450,3,58,29,0,450,
        49,1,0,0,0,451,452,6,25,-1,0,452,463,3,8,4,0,453,463,3,28,14,0,454,
        463,3,58,29,0,455,463,3,24,12,0,456,463,3,52,26,0,457,463,3,44,22,
        0,458,459,5,9,0,0,459,460,3,50,25,0,460,461,5,10,0,0,461,463,1,0,
        0,0,462,451,1,0,0,0,462,453,1,0,0,0,462,454,1,0,0,0,462,455,1,0,
        0,0,462,456,1,0,0,0,462,457,1,0,0,0,462,458,1,0,0,0,463,472,1,0,
        0,0,464,465,10,7,0,0,465,466,5,2,0,0,466,471,3,50,25,8,467,468,10,
        6,0,0,468,469,5,3,0,0,469,471,3,50,25,7,470,464,1,0,0,0,470,467,
        1,0,0,0,471,474,1,0,0,0,472,470,1,0,0,0,472,473,1,0,0,0,473,51,1,
        0,0,0,474,472,1,0,0,0,475,481,3,42,21,0,476,481,5,57,0,0,477,481,
        5,52,0,0,478,481,5,55,0,0,479,481,3,54,27,0,480,475,1,0,0,0,480,
        476,1,0,0,0,480,477,1,0,0,0,480,478,1,0,0,0,480,479,1,0,0,0,481,
        53,1,0,0,0,482,483,5,55,0,0,483,484,5,49,0,0,484,485,5,55,0,0,485,
        55,1,0,0,0,486,489,3,58,29,0,487,489,3,60,30,0,488,486,1,0,0,0,488,
        487,1,0,0,0,489,57,1,0,0,0,490,492,3,64,32,0,491,490,1,0,0,0,491,
        492,1,0,0,0,492,494,1,0,0,0,493,495,5,56,0,0,494,493,1,0,0,0,495,
        496,1,0,0,0,496,494,1,0,0,0,496,497,1,0,0,0,497,59,1,0,0,0,498,500,
        5,56,0,0,499,498,1,0,0,0,500,501,1,0,0,0,501,499,1,0,0,0,501,502,
        1,0,0,0,502,61,1,0,0,0,503,505,3,64,32,0,504,503,1,0,0,0,504,505,
        1,0,0,0,505,506,1,0,0,0,506,507,5,56,0,0,507,63,1,0,0,0,508,509,
        7,10,0,0,509,65,1,0,0,0,63,73,77,108,124,128,134,138,140,150,154,
        167,171,178,182,193,197,205,208,216,224,229,232,237,240,242,250,
        260,268,283,286,293,298,301,312,317,321,323,326,338,347,357,363,
        367,373,379,386,390,396,404,418,428,432,442,446,462,470,472,480,
        488,491,496,501,504
    ]

class ProfilesParser ( Parser ):

    grammarFileName = "Profiles.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'and'", "'or'", "'not'", "'equal'", 
                     "'to'", "'in'", "'between'", "'('", "')'", "'of'", 
                     "'the'", "'intersection'", "'union'", "'sum'", "'product'", 
                     "'difference'", "'quotient'", "'there'", "'different'", 
                     "'has'", "'one'", "'for'", "'all'", "'each'", "'every'", 
                     "'is'", "'such'", "'that'", "'are'", "'no'", "'than'", 
                     "'at'", "'least'", "'most'", "'from'", "'immediately'", 
                     "'precedes'", "'follows'", "'overlaps'", "'disjoint'", 
                     "'with'", "'greater'", "'more'", "'smaller'", "'less'", 
                     "'{'", "'}'", "'-'", "'a'", "'an'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "VARIABLE", "NUMBER", "PERCENT", "TIME", "WORD", "STRING", 
                      "WS" ]

    RULE_profile = 0
    RULE_condition = 1
    RULE_predicate = 2
    RULE_unary_predicate = 3
    RULE_function = 4
    RULE_function_name = 5
    RULE_existential = 6
    RULE_binding_existential_with_diff = 7
    RULE_binding_existential_with_unique = 8
    RULE_binding_existential_with_unique1 = 9
    RULE_binding_existential_unique = 10
    RULE_universal = 11
    RULE_aggregate = 12
    RULE_such_that = 13
    RULE_attribute = 14
    RULE_to_be = 15
    RULE_comparison_operator = 16
    RULE_eq_not_eq = 17
    RULE_temporal_operator = 18
    RULE_greater = 19
    RULE_smaller = 20
    RULE_quantity = 21
    RULE_general_set = 22
    RULE_conjunction_of_np = 23
    RULE_disjunction_of_np = 24
    RULE_expr = 25
    RULE_atomic_expr = 26
    RULE_period = 27
    RULE_phrase = 28
    RULE_noun_phrase = 29
    RULE_verb_phrase = 30
    RULE_type_name = 31
    RULE_article = 32

    ruleNames =  [ "profile", "condition", "predicate", "unary_predicate", 
                   "function", "function_name", "existential", "binding_existential_with_diff", 
                   "binding_existential_with_unique", "binding_existential_with_unique1", 
                   "binding_existential_unique", "universal", "aggregate", 
                   "such_that", "attribute", "to_be", "comparison_operator", 
                   "eq_not_eq", "temporal_operator", "greater", "smaller", 
                   "quantity", "general_set", "conjunction_of_np", "disjunction_of_np", 
                   "expr", "atomic_expr", "period", "phrase", "noun_phrase", 
                   "verb_phrase", "type_name", "article" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    VARIABLE=52
    NUMBER=53
    PERCENT=54
    TIME=55
    WORD=56
    STRING=57
    WS=58

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProfileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)


        def EOF(self):
            return self.getToken(ProfilesParser.EOF, 0)

        def getRuleIndex(self):
            return ProfilesParser.RULE_profile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProfile" ):
                listener.enterProfile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProfile" ):
                listener.exitProfile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProfile" ):
                return visitor.visitProfile(self)
            else:
                return visitor.visitChildren(self)




    def profile(self):

        localctx = ProfilesParser.ProfileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_profile)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.condition(0)
            self.state = 67
            self.match(ProfilesParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_condition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class NegationContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNegation" ):
                listener.enterNegation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNegation" ):
                listener.exitNegation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNegation" ):
                return visitor.visitNegation(self)
            else:
                return visitor.visitChildren(self)


    class InContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.negate = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)

        def general_set(self):
            return self.getTypedRuleContext(ProfilesParser.General_setContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIn" ):
                listener.enterIn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIn" ):
                listener.exitIn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIn" ):
                return visitor.visitIn(self)
            else:
                return visitor.visitChildren(self)


    class UniversalCondContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def universal(self):
            return self.getTypedRuleContext(ProfilesParser.UniversalContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUniversalCond" ):
                listener.enterUniversalCond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUniversalCond" ):
                listener.exitUniversalCond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUniversalCond" ):
                return visitor.visitUniversalCond(self)
            else:
                return visitor.visitChildren(self)


    class BetweenContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.value = None # ExprContext
            self.lower_bound = None # ExprContext
            self.upper_bound = None # ExprContext
            self.copyFrom(ctx)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBetween" ):
                listener.enterBetween(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBetween" ):
                listener.exitBetween(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBetween" ):
                return visitor.visitBetween(self)
            else:
                return visitor.visitChildren(self)


    class BindingExistentialWithDiffContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def binding_existential_with_diff(self):
            return self.getTypedRuleContext(ProfilesParser.Binding_existential_with_diffContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBindingExistentialWithDiff" ):
                listener.enterBindingExistentialWithDiff(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBindingExistentialWithDiff" ):
                listener.exitBindingExistentialWithDiff(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBindingExistentialWithDiff" ):
                return visitor.visitBindingExistentialWithDiff(self)
            else:
                return visitor.visitChildren(self)


    class BindingExistentialWithUniqueContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def binding_existential_with_unique(self):
            return self.getTypedRuleContext(ProfilesParser.Binding_existential_with_uniqueContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBindingExistentialWithUnique" ):
                listener.enterBindingExistentialWithUnique(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBindingExistentialWithUnique" ):
                listener.exitBindingExistentialWithUnique(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBindingExistentialWithUnique" ):
                return visitor.visitBindingExistentialWithUnique(self)
            else:
                return visitor.visitChildren(self)


    class ParenCondContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenCond" ):
                listener.enterParenCond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenCond" ):
                listener.exitParenCond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenCond" ):
                return visitor.visitParenCond(self)
            else:
                return visitor.visitChildren(self)


    class UnaryPredApplContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def unary_predicate(self):
            return self.getTypedRuleContext(ProfilesParser.Unary_predicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryPredAppl" ):
                listener.enterUnaryPredAppl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryPredAppl" ):
                listener.exitUnaryPredAppl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryPredAppl" ):
                return visitor.visitUnaryPredAppl(self)
            else:
                return visitor.visitChildren(self)


    class TemporalOpContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)

        def temporal_operator(self):
            return self.getTypedRuleContext(ProfilesParser.Temporal_operatorContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalOp" ):
                listener.enterTemporalOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalOp" ):
                listener.exitTemporalOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemporalOp" ):
                return visitor.visitTemporalOp(self)
            else:
                return visitor.visitChildren(self)


    class DisjunctionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ConditionContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ConditionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDisjunction" ):
                listener.enterDisjunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDisjunction" ):
                listener.exitDisjunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDisjunction" ):
                return visitor.visitDisjunction(self)
            else:
                return visitor.visitChildren(self)


    class ExistentialCondContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def existential(self):
            return self.getTypedRuleContext(ProfilesParser.ExistentialContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistentialCond" ):
                listener.enterExistentialCond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistentialCond" ):
                listener.exitExistentialCond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistentialCond" ):
                return visitor.visitExistentialCond(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)

        def comparison_operator(self):
            return self.getTypedRuleContext(ProfilesParser.Comparison_operatorContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)


    class ConjunctionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ConditionContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ConditionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConjunction" ):
                listener.enterConjunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConjunction" ):
                listener.exitConjunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunction" ):
                return visitor.visitConjunction(self)
            else:
                return visitor.visitChildren(self)


    class PredicateApplContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)

        def predicate(self):
            return self.getTypedRuleContext(ProfilesParser.PredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicateAppl" ):
                listener.enterPredicateAppl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicateAppl" ):
                listener.exitPredicateAppl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicateAppl" ):
                return visitor.visitPredicateAppl(self)
            else:
                return visitor.visitChildren(self)


    class BindingExistentialUniqueContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def binding_existential_unique(self):
            return self.getTypedRuleContext(ProfilesParser.Binding_existential_uniqueContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBindingExistentialUnique" ):
                listener.enterBindingExistentialUnique(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBindingExistentialUnique" ):
                listener.exitBindingExistentialUnique(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBindingExistentialUnique" ):
                return visitor.visitBindingExistentialUnique(self)
            else:
                return visitor.visitChildren(self)


    class IsConstantContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ConditionContext
            super().__init__(parser)
            self.negate = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)

        def atomic_expr(self):
            return self.getTypedRuleContext(ProfilesParser.Atomic_exprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIsConstant" ):
                listener.enterIsConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIsConstant" ):
                listener.exitIsConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIsConstant" ):
                return visitor.visitIsConstant(self)
            else:
                return visitor.visitChildren(self)



    def condition(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ProfilesParser.ConditionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_condition, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = ProfilesParser.IsConstantContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 70
                self.expr(0)
                self.state = 71
                self.to_be()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 72
                    localctx.negate = self.match(ProfilesParser.T__3)


                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==5:
                    self.state = 75
                    self.match(ProfilesParser.T__4)
                    self.state = 76
                    self.match(ProfilesParser.T__5)


                self.state = 79
                self.atomic_expr()
                pass

            elif la_ == 2:
                localctx = ProfilesParser.PredicateApplContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 81
                self.expr(0)
                self.state = 82
                self.predicate()
                self.state = 83
                self.expr(0)
                pass

            elif la_ == 3:
                localctx = ProfilesParser.UnaryPredApplContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 85
                self.expr(0)
                self.state = 86
                self.unary_predicate()
                pass

            elif la_ == 4:
                localctx = ProfilesParser.ComparisonContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 88
                self.expr(0)
                self.state = 89
                self.comparison_operator()
                self.state = 90
                self.expr(0)
                pass

            elif la_ == 5:
                localctx = ProfilesParser.TemporalOpContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 92
                self.expr(0)
                self.state = 93
                self.temporal_operator()
                self.state = 94
                self.expr(0)
                self.state = 95
                self.match(ProfilesParser.T__6)
                self.state = 96
                self.expr(0)
                pass

            elif la_ == 6:
                localctx = ProfilesParser.BetweenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 98
                localctx.value = self.expr(0)
                self.state = 99
                self.to_be()
                self.state = 100
                self.match(ProfilesParser.T__7)
                self.state = 101
                localctx.lower_bound = self.expr(0)
                self.state = 102
                self.match(ProfilesParser.T__1)
                self.state = 103
                localctx.upper_bound = self.expr(0)
                pass

            elif la_ == 7:
                localctx = ProfilesParser.InContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.expr(0)
                self.state = 106
                self.to_be()
                self.state = 108
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 107
                    localctx.negate = self.match(ProfilesParser.T__3)


                self.state = 110
                self.match(ProfilesParser.T__6)
                self.state = 111
                self.general_set()
                pass

            elif la_ == 8:
                localctx = ProfilesParser.NegationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 113
                self.match(ProfilesParser.T__3)
                self.state = 114
                self.condition(7)
                pass

            elif la_ == 9:
                localctx = ProfilesParser.ExistentialCondContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                self.existential()
                pass

            elif la_ == 10:
                localctx = ProfilesParser.UniversalCondContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 116
                self.universal()
                pass

            elif la_ == 11:
                localctx = ProfilesParser.BindingExistentialWithDiffContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 117
                self.binding_existential_with_diff()
                pass

            elif la_ == 12:
                localctx = ProfilesParser.BindingExistentialWithUniqueContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 118
                self.binding_existential_with_unique()
                pass

            elif la_ == 13:
                localctx = ProfilesParser.BindingExistentialUniqueContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 119
                self.binding_existential_unique()
                pass

            elif la_ == 14:
                localctx = ProfilesParser.ParenCondContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 120
                self.match(ProfilesParser.T__8)
                self.state = 121
                self.condition(0)
                self.state = 122
                self.match(ProfilesParser.T__9)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 140
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 138
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                    if la_ == 1:
                        localctx = ProfilesParser.ConjunctionContext(self, ProfilesParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 126
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 128
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==1:
                            self.state = 127
                            self.match(ProfilesParser.T__0)


                        self.state = 130
                        self.match(ProfilesParser.T__1)
                        self.state = 131
                        self.condition(17)
                        pass

                    elif la_ == 2:
                        localctx = ProfilesParser.DisjunctionContext(self, ProfilesParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 132
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 134
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==1:
                            self.state = 133
                            self.match(ProfilesParser.T__0)


                        self.state = 136
                        self.match(ProfilesParser.T__2)
                        self.state = 137
                        self.condition(16)
                        pass

             
                self.state = 142
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_predicate

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ConjunctivePredContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def phrase(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.PhraseContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.PhraseContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConjunctivePred" ):
                listener.enterConjunctivePred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConjunctivePred" ):
                listener.exitConjunctivePred(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunctivePred" ):
                return visitor.visitConjunctivePred(self)
            else:
                return visitor.visitChildren(self)


    class AtomicPredContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def phrase(self):
            return self.getTypedRuleContext(ProfilesParser.PhraseContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomicPred" ):
                listener.enterAtomicPred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomicPred" ):
                listener.exitAtomicPred(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomicPred" ):
                return visitor.visitAtomicPred(self)
            else:
                return visitor.visitChildren(self)


    class DisjunctivePredContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def phrase(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.PhraseContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.PhraseContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDisjunctivePred" ):
                listener.enterDisjunctivePred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDisjunctivePred" ):
                listener.exitDisjunctivePred(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDisjunctivePred" ):
                return visitor.visitDisjunctivePred(self)
            else:
                return visitor.visitChildren(self)



    def predicate(self):

        localctx = ProfilesParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_predicate)
        self._la = 0 # Token type
        try:
            self.state = 178
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = ProfilesParser.AtomicPredContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.phrase()
                pass

            elif la_ == 2:
                localctx = ProfilesParser.ConjunctivePredContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 144
                self.match(ProfilesParser.T__8)
                self.state = 145
                self.phrase()
                self.state = 150
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 146
                        self.match(ProfilesParser.T__0)
                        self.state = 147
                        self.phrase() 
                    self.state = 152
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

                self.state = 154
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 153
                    self.match(ProfilesParser.T__0)


                self.state = 156
                self.match(ProfilesParser.T__1)
                self.state = 157
                self.phrase()
                self.state = 159
                self.match(ProfilesParser.T__9)
                pass

            elif la_ == 3:
                localctx = ProfilesParser.DisjunctivePredContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 161
                self.match(ProfilesParser.T__8)
                self.state = 162
                self.phrase()
                self.state = 167
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 163
                        self.match(ProfilesParser.T__0)
                        self.state = 164
                        self.phrase() 
                    self.state = 169
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

                self.state = 171
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 170
                    self.match(ProfilesParser.T__0)


                self.state = 173
                self.match(ProfilesParser.T__2)
                self.state = 174
                self.phrase()
                self.state = 176
                self.match(ProfilesParser.T__9)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Unary_predicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.negate = None # Token

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def phrase(self):
            return self.getTypedRuleContext(ProfilesParser.PhraseContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_unary_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnary_predicate" ):
                listener.enterUnary_predicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnary_predicate" ):
                listener.exitUnary_predicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary_predicate" ):
                return visitor.visitUnary_predicate(self)
            else:
                return visitor.visitChildren(self)




    def unary_predicate(self):

        localctx = ProfilesParser.Unary_predicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_unary_predicate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.to_be()
            self.state = 182
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 181
                localctx.negate = self.match(ProfilesParser.T__3)


            self.state = 184
            self.phrase()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_function

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionAppContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.FunctionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def function_name(self):
            return self.getTypedRuleContext(ProfilesParser.Function_nameContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionApp" ):
                listener.enterFunctionApp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionApp" ):
                listener.exitFunctionApp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionApp" ):
                return visitor.visitFunctionApp(self)
            else:
                return visitor.visitChildren(self)


    class PercentOfContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.FunctionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PERCENT(self):
            return self.getToken(ProfilesParser.PERCENT, 0)
        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPercentOf" ):
                listener.enterPercentOf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPercentOf" ):
                listener.exitPercentOf(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPercentOf" ):
                return visitor.visitPercentOf(self)
            else:
                return visitor.visitChildren(self)



    def function(self):

        localctx = ProfilesParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.state = 205
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12, 13, 14, 15, 16, 17, 18]:
                localctx = ProfilesParser.FunctionAppContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 186
                self.function_name()
                self.state = 187
                _la = self._input.LA(1)
                if not(_la==8 or _la==11):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 188
                self.expr(0)

                self.state = 193
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 189
                        self.match(ProfilesParser.T__0)
                        self.state = 190
                        self.expr(0) 
                    self.state = 195
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

                self.state = 197
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 196
                    self.match(ProfilesParser.T__0)


                self.state = 199
                self.match(ProfilesParser.T__1)
                self.state = 200
                self.expr(0)
                pass
            elif token in [54]:
                localctx = ProfilesParser.PercentOfContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 202
                self.match(ProfilesParser.PERCENT)
                self.state = 203
                self.match(ProfilesParser.T__10)
                self.state = 204
                self.expr(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Function_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token


        def getRuleIndex(self):
            return ProfilesParser.RULE_function_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_name" ):
                listener.enterFunction_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_name" ):
                listener.exitFunction_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction_name" ):
                return visitor.visitFunction_name(self)
            else:
                return visitor.visitChildren(self)




    def function_name(self):

        localctx = ProfilesParser.Function_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_function_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 207
                self.match(ProfilesParser.T__11)


            self.state = 210
            localctx.op = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 516096) != 0)):
                localctx.op = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistentialContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.diff = None # Token

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)


        def VARIABLE(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.VARIABLE)
            else:
                return self.getToken(ProfilesParser.VARIABLE, i)

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)


        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def such_that(self):
            return self.getTypedRuleContext(ProfilesParser.Such_thatContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_existential

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistential" ):
                listener.enterExistential(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistential" ):
                listener.exitExistential(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistential" ):
                return visitor.visitExistential(self)
            else:
                return visitor.visitChildren(self)




    def existential(self):

        localctx = ProfilesParser.ExistentialContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_existential)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(ProfilesParser.T__18)
            self.state = 213
            self.to_be()
            self.state = 216
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.state = 214
                localctx.diff = self.match(ProfilesParser.T__19)

            elif la_ == 2:
                self.state = 215
                self.article()


            self.state = 218
            self.type_name()
            self.state = 219
            self.match(ProfilesParser.VARIABLE)
            self.state = 224
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 220
                    _la = self._input.LA(1)
                    if not(_la==1 or _la==2):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 221
                    self.match(ProfilesParser.VARIABLE) 
                self.state = 226
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

            self.state = 229
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 227
                self.match(ProfilesParser.T__6)
                self.state = 228
                self.expr(0)


            self.state = 232
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 231
                self.such_that()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Binding_existential_with_diffContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.diff = None # Token
            self._VARIABLE = None # Token
            self.mvars = list() # of Tokens

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)


        def such_that(self):
            return self.getTypedRuleContext(ProfilesParser.Such_thatContext,0)


        def VARIABLE(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.VARIABLE)
            else:
                return self.getToken(ProfilesParser.VARIABLE, i)

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_binding_existential_with_diff

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinding_existential_with_diff" ):
                listener.enterBinding_existential_with_diff(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinding_existential_with_diff" ):
                listener.exitBinding_existential_with_diff(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinding_existential_with_diff" ):
                return visitor.visitBinding_existential_with_diff(self)
            else:
                return visitor.visitChildren(self)




    def binding_existential_with_diff(self):

        localctx = ProfilesParser.Binding_existential_with_diffContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_binding_existential_with_diff)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234
            self.expr(0)
            self.state = 235
            self.match(ProfilesParser.T__20)

            self.state = 242
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.state = 237
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==20:
                    self.state = 236
                    localctx.diff = self.match(ProfilesParser.T__19)


                pass

            elif la_ == 2:
                self.state = 240
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
                if la_ == 1:
                    self.state = 239
                    self.article()


                pass


            self.state = 244
            self.type_name()
            self.state = 245
            localctx._VARIABLE = self.match(ProfilesParser.VARIABLE)
            localctx.mvars.append(localctx._VARIABLE)
            self.state = 250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==2:
                self.state = 246
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 247
                localctx._VARIABLE = self.match(ProfilesParser.VARIABLE)
                localctx.mvars.append(localctx._VARIABLE)
                self.state = 252
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 253
            self.such_that()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Binding_existential_with_uniqueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def binding_existential_with_unique1(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.Binding_existential_with_unique1Context)
            else:
                return self.getTypedRuleContext(ProfilesParser.Binding_existential_with_unique1Context,i)


        def such_that(self):
            return self.getTypedRuleContext(ProfilesParser.Such_thatContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_binding_existential_with_unique

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinding_existential_with_unique" ):
                listener.enterBinding_existential_with_unique(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinding_existential_with_unique" ):
                listener.exitBinding_existential_with_unique(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinding_existential_with_unique" ):
                return visitor.visitBinding_existential_with_unique(self)
            else:
                return visitor.visitChildren(self)




    def binding_existential_with_unique(self):

        localctx = ProfilesParser.Binding_existential_with_uniqueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_binding_existential_with_unique)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            self.binding_existential_with_unique1()
            self.state = 260
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 256
                self.match(ProfilesParser.T__1)
                self.state = 257
                self.binding_existential_with_unique1()
                self.state = 262
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 263
            self.such_that()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Binding_existential_with_unique1Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.unique = None # Token

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)


        def VARIABLE(self):
            return self.getToken(ProfilesParser.VARIABLE, 0)

        def getRuleIndex(self):
            return ProfilesParser.RULE_binding_existential_with_unique1

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinding_existential_with_unique1" ):
                listener.enterBinding_existential_with_unique1(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinding_existential_with_unique1" ):
                listener.exitBinding_existential_with_unique1(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinding_existential_with_unique1" ):
                return visitor.visitBinding_existential_with_unique1(self)
            else:
                return visitor.visitChildren(self)




    def binding_existential_with_unique1(self):

        localctx = ProfilesParser.Binding_existential_with_unique1Context(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_binding_existential_with_unique1)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 265
            self.expr(0)
            self.state = 266
            self.match(ProfilesParser.T__20)
            self.state = 268
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==22:
                self.state = 267
                localctx.unique = self.match(ProfilesParser.T__21)


            self.state = 270
            self.type_name()
            self.state = 271
            self.match(ProfilesParser.VARIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Binding_existential_uniqueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)


        def VARIABLE(self):
            return self.getToken(ProfilesParser.VARIABLE, 0)

        def getRuleIndex(self):
            return ProfilesParser.RULE_binding_existential_unique

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinding_existential_unique" ):
                listener.enterBinding_existential_unique(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinding_existential_unique" ):
                listener.exitBinding_existential_unique(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinding_existential_unique" ):
                return visitor.visitBinding_existential_unique(self)
            else:
                return visitor.visitChildren(self)




    def binding_existential_unique(self):

        localctx = ProfilesParser.Binding_existential_uniqueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_binding_existential_unique)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
            self.expr(0)
            self.state = 274
            self.match(ProfilesParser.T__20)
            self.state = 275
            self.match(ProfilesParser.T__21)
            self.state = 276
            self.type_name()
            self.state = 277
            self.match(ProfilesParser.VARIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UniversalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_universal

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class EveryContext(UniversalContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.UniversalContext
            super().__init__(parser)
            self.of_expr = None # ExprContext
            self.in_set = None # General_setContext
            self.copyFrom(ctx)

        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)

        def VARIABLE(self):
            return self.getToken(ProfilesParser.VARIABLE, 0)
        def predicate(self):
            return self.getTypedRuleContext(ProfilesParser.PredicateContext,0)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def general_set(self):
            return self.getTypedRuleContext(ProfilesParser.General_setContext,0)

        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEvery" ):
                listener.enterEvery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEvery" ):
                listener.exitEvery(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEvery" ):
                return visitor.visitEvery(self)
            else:
                return visitor.visitChildren(self)


    class ForAllContext(UniversalContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.UniversalContext
            super().__init__(parser)
            self.diff = None # Token
            self.copyFrom(ctx)

        def VARIABLE(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.VARIABLE)
            else:
                return self.getToken(ProfilesParser.VARIABLE, i)
        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)

        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def such_that(self):
            return self.getTypedRuleContext(ProfilesParser.Such_thatContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForAll" ):
                listener.enterForAll(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForAll" ):
                listener.exitForAll(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForAll" ):
                return visitor.visitForAll(self)
            else:
                return visitor.visitChildren(self)



    def universal(self):

        localctx = ProfilesParser.UniversalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_universal)
        self._la = 0 # Token type
        try:
            self.state = 323
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                localctx = ProfilesParser.ForAllContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 279
                self.match(ProfilesParser.T__22)
                self.state = 280
                _la = self._input.LA(1)
                if not(_la==24 or _la==25):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 283
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
                if la_ == 1:
                    self.state = 281
                    localctx.diff = self.match(ProfilesParser.T__19)

                elif la_ == 2:
                    self.state = 282
                    self.article()


                self.state = 286
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 75435293758459904) != 0):
                    self.state = 285
                    self.type_name()


                self.state = 288
                self.match(ProfilesParser.VARIABLE)
                self.state = 293
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,30,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 289
                        _la = self._input.LA(1)
                        if not(_la==1 or _la==2):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 290
                        self.match(ProfilesParser.VARIABLE) 
                    self.state = 295
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,30,self._ctx)

                self.state = 298
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 296
                    self.match(ProfilesParser.T__6)
                    self.state = 297
                    self.expr(0)


                self.state = 301
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==28:
                    self.state = 300
                    self.such_that()


                self.state = 303
                self.match(ProfilesParser.T__0)
                self.state = 304
                self.condition(0)
                pass
            elif token in [26]:
                localctx = ProfilesParser.EveryContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 305
                self.match(ProfilesParser.T__25)
                self.state = 306
                self.type_name()
                self.state = 307
                self.match(ProfilesParser.VARIABLE)
                self.state = 312
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [11]:
                    self.state = 308
                    self.match(ProfilesParser.T__10)
                    self.state = 309
                    localctx.of_expr = self.expr(0)
                    pass
                elif token in [7]:
                    self.state = 310
                    self.match(ProfilesParser.T__6)
                    self.state = 311
                    localctx.in_set = self.general_set()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 314
                self.match(ProfilesParser.T__26)
                self.state = 315
                self.predicate()
                self.state = 321
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
                if la_ == 1:
                    self.state = 317
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==1:
                        self.state = 316
                        self.match(ProfilesParser.T__0)


                    self.state = 319
                    self.match(ProfilesParser.T__1)
                    self.state = 320
                    self.condition(0)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AggregateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token
            self.term = None # ExprContext
            self.v = None # Token
            self.collection = None # ExprContext

        def type_name(self):
            return self.getTypedRuleContext(ProfilesParser.Type_nameContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def VARIABLE(self):
            return self.getToken(ProfilesParser.VARIABLE, 0)

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)


        def such_that(self):
            return self.getTypedRuleContext(ProfilesParser.Such_thatContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_aggregate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAggregate" ):
                listener.enterAggregate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAggregate" ):
                listener.exitAggregate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAggregate" ):
                return visitor.visitAggregate(self)
            else:
                return visitor.visitChildren(self)




    def aggregate(self):

        localctx = ProfilesParser.AggregateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_aggregate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3377699720531968) != 0):
                self.state = 325
                self.article()


            self.state = 328
            localctx.op = self._input.LT(1)
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                localctx.op = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 329
            self.match(ProfilesParser.T__10)
            self.state = 330
            localctx.term = self.expr(0)
            self.state = 331
            self.match(ProfilesParser.T__22)
            self.state = 332
            self.match(ProfilesParser.T__23)
            self.state = 333
            self.type_name()
            self.state = 334
            localctx.v = self.match(ProfilesParser.VARIABLE)
            self.state = 335
            self.match(ProfilesParser.T__6)
            self.state = 336
            localctx.collection = self.expr(0)
            self.state = 338
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,38,self._ctx)
            if la_ == 1:
                self.state = 337
                self.such_that()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Such_thatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(ProfilesParser.ConditionContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_such_that

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSuch_that" ):
                listener.enterSuch_that(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSuch_that" ):
                listener.exitSuch_that(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSuch_that" ):
                return visitor.visitSuch_that(self)
            else:
                return visitor.visitChildren(self)




    def such_that(self):

        localctx = ProfilesParser.Such_thatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_such_that)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 340
            self.match(ProfilesParser.T__27)
            self.state = 341
            self.match(ProfilesParser.T__28)
            self.state = 342
            self.condition(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_attribute

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SingleAttributeContext(AttributeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.AttributeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def noun_phrase(self):
            return self.getTypedRuleContext(ProfilesParser.Noun_phraseContext,0)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleAttribute" ):
                listener.enterSingleAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleAttribute" ):
                listener.exitSingleAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleAttribute" ):
                return visitor.visitSingleAttribute(self)
            else:
                return visitor.visitChildren(self)


    class MultipleAttributesContext(AttributeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.AttributeContext
            super().__init__(parser)
            self.cnp = None # Conjunction_of_npContext
            self.dnp = None # Disjunction_of_npContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)

        def conjunction_of_np(self):
            return self.getTypedRuleContext(ProfilesParser.Conjunction_of_npContext,0)

        def disjunction_of_np(self):
            return self.getTypedRuleContext(ProfilesParser.Disjunction_of_npContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipleAttributes" ):
                listener.enterMultipleAttributes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipleAttributes" ):
                listener.exitMultipleAttributes(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultipleAttributes" ):
                return visitor.visitMultipleAttributes(self)
            else:
                return visitor.visitChildren(self)



    def attribute(self):

        localctx = ProfilesParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_attribute)
        try:
            self.state = 357
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                localctx = ProfilesParser.MultipleAttributesContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 344
                self.match(ProfilesParser.T__8)
                self.state = 347
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
                if la_ == 1:
                    self.state = 345
                    localctx.cnp = self.conjunction_of_np()
                    pass

                elif la_ == 2:
                    self.state = 346
                    localctx.dnp = self.disjunction_of_np()
                    pass


                self.state = 349
                self.match(ProfilesParser.T__9)
                self.state = 350
                self.match(ProfilesParser.T__10)
                self.state = 351
                self.expr(0)
                pass
            elif token in [12, 50, 51, 56]:
                localctx = ProfilesParser.SingleAttributeContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 353
                self.noun_phrase()
                self.state = 354
                self.match(ProfilesParser.T__10)
                self.state = 355
                self.expr(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class To_beContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_to_be

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTo_be" ):
                listener.enterTo_be(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTo_be" ):
                listener.exitTo_be(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTo_be" ):
                return visitor.visitTo_be(self)
            else:
                return visitor.visitChildren(self)




    def to_be(self):

        localctx = ProfilesParser.To_beContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_to_be)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 359
            _la = self._input.LA(1)
            if not(_la==27 or _la==30):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Comparison_operatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_comparison_operator

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ComparisonOp1Context(Comparison_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Comparison_operatorContext
            super().__init__(parser)
            self.negate = None # Token
            self.gr = None # GreaterContext
            self.sm = None # SmallerContext
            self.or_eq = None # Token
            self.copyFrom(ctx)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)

        def greater(self):
            return self.getTypedRuleContext(ProfilesParser.GreaterContext,0)

        def smaller(self):
            return self.getTypedRuleContext(ProfilesParser.SmallerContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp1" ):
                listener.enterComparisonOp1(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp1" ):
                listener.exitComparisonOp1(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp1" ):
                return visitor.visitComparisonOp1(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonOp4Context(Comparison_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Comparison_operatorContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp4" ):
                listener.enterComparisonOp4(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp4" ):
                listener.exitComparisonOp4(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp4" ):
                return visitor.visitComparisonOp4(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonOp2Context(Comparison_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Comparison_operatorContext
            super().__init__(parser)
            self.gr = None # Token
            self.sm = None # Token
            self.copyFrom(ctx)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp2" ):
                listener.enterComparisonOp2(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp2" ):
                listener.exitComparisonOp2(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp2" ):
                return visitor.visitComparisonOp2(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonOp3Context(Comparison_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Comparison_operatorContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def eq_not_eq(self):
            return self.getTypedRuleContext(ProfilesParser.Eq_not_eqContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp3" ):
                listener.enterComparisonOp3(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp3" ):
                listener.exitComparisonOp3(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp3" ):
                return visitor.visitComparisonOp3(self)
            else:
                return visitor.visitChildren(self)



    def comparison_operator(self):

        localctx = ProfilesParser.Comparison_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_comparison_operator)
        self._la = 0 # Token type
        try:
            self.state = 386
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
            if la_ == 1:
                localctx = ProfilesParser.ComparisonOp1Context(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 361
                self.to_be()
                self.state = 363
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4 or _la==31:
                    self.state = 362
                    localctx.negate = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==4 or _la==31):
                        localctx.negate = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 367
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [43, 44]:
                    self.state = 365
                    localctx.gr = self.greater()
                    pass
                elif token in [45, 46]:
                    self.state = 366
                    localctx.sm = self.smaller()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 369
                self.match(ProfilesParser.T__31)
                self.state = 373
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 370
                    self.match(ProfilesParser.T__2)
                    self.state = 371
                    localctx.or_eq = self.match(ProfilesParser.T__4)
                    self.state = 372
                    self.match(ProfilesParser.T__5)


                pass

            elif la_ == 2:
                localctx = ProfilesParser.ComparisonOp2Context(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 375
                self.to_be()
                self.state = 376
                self.match(ProfilesParser.T__32)
                self.state = 379
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [34]:
                    self.state = 377
                    localctx.gr = self.match(ProfilesParser.T__33)
                    pass
                elif token in [35]:
                    self.state = 378
                    localctx.sm = self.match(ProfilesParser.T__34)
                    pass
                else:
                    raise NoViableAltException(self)

                pass

            elif la_ == 3:
                localctx = ProfilesParser.ComparisonOp3Context(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 381
                self.eq_not_eq()
                pass

            elif la_ == 4:
                localctx = ProfilesParser.ComparisonOp4Context(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 382
                self.to_be()
                self.state = 383
                self.match(ProfilesParser.T__19)
                self.state = 384
                self.match(ProfilesParser.T__35)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Eq_not_eqContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.negate = None # Token

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_eq_not_eq

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEq_not_eq" ):
                listener.enterEq_not_eq(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEq_not_eq" ):
                listener.exitEq_not_eq(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEq_not_eq" ):
                return visitor.visitEq_not_eq(self)
            else:
                return visitor.visitChildren(self)




    def eq_not_eq(self):

        localctx = ProfilesParser.Eq_not_eqContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_eq_not_eq)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 388
            self.to_be()
            self.state = 390
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 389
                localctx.negate = self.match(ProfilesParser.T__3)


            self.state = 392
            self.match(ProfilesParser.T__4)
            self.state = 393
            self.match(ProfilesParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Temporal_operatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_temporal_operator

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TemporalOrderContext(Temporal_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Temporal_operatorContext
            super().__init__(parser)
            self.immed = None # Token
            self.order = None # Token
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalOrder" ):
                listener.enterTemporalOrder(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalOrder" ):
                listener.exitTemporalOrder(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemporalOrder" ):
                return visitor.visitTemporalOrder(self)
            else:
                return visitor.visitChildren(self)


    class TemporalDisjointContext(Temporal_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Temporal_operatorContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def to_be(self):
            return self.getTypedRuleContext(ProfilesParser.To_beContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalDisjoint" ):
                listener.enterTemporalDisjoint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalDisjoint" ):
                listener.exitTemporalDisjoint(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemporalDisjoint" ):
                return visitor.visitTemporalDisjoint(self)
            else:
                return visitor.visitChildren(self)


    class TemporalOverlapContext(Temporal_operatorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Temporal_operatorContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalOverlap" ):
                listener.enterTemporalOverlap(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalOverlap" ):
                listener.exitTemporalOverlap(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemporalOverlap" ):
                return visitor.visitTemporalOverlap(self)
            else:
                return visitor.visitChildren(self)



    def temporal_operator(self):

        localctx = ProfilesParser.Temporal_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_temporal_operator)
        self._la = 0 # Token type
        try:
            self.state = 404
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [37, 38, 39]:
                localctx = ProfilesParser.TemporalOrderContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 396
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==37:
                    self.state = 395
                    localctx.immed = self.match(ProfilesParser.T__36)


                self.state = 398
                localctx.order = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==38 or _la==39):
                    localctx.order = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [40]:
                localctx = ProfilesParser.TemporalOverlapContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 399
                self.match(ProfilesParser.T__39)
                pass
            elif token in [27, 30]:
                localctx = ProfilesParser.TemporalDisjointContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 400
                self.to_be()
                self.state = 401
                self.match(ProfilesParser.T__40)
                self.state = 402
                self.match(ProfilesParser.T__41)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GreaterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_greater

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGreater" ):
                listener.enterGreater(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGreater" ):
                listener.exitGreater(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGreater" ):
                return visitor.visitGreater(self)
            else:
                return visitor.visitChildren(self)




    def greater(self):

        localctx = ProfilesParser.GreaterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_greater)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 406
            _la = self._input.LA(1)
            if not(_la==43 or _la==44):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SmallerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_smaller

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSmaller" ):
                listener.enterSmaller(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSmaller" ):
                listener.exitSmaller(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSmaller" ):
                return visitor.visitSmaller(self)
            else:
                return visitor.visitChildren(self)




    def smaller(self):

        localctx = ProfilesParser.SmallerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_smaller)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 408
            _la = self._input.LA(1)
            if not(_la==45 or _la==46):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(ProfilesParser.NUMBER, 0)

        def getRuleIndex(self):
            return ProfilesParser.RULE_quantity

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantity" ):
                listener.enterQuantity(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantity" ):
                listener.exitQuantity(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuantity" ):
                return visitor.visitQuantity(self)
            else:
                return visitor.visitChildren(self)




    def quantity(self):

        localctx = ProfilesParser.QuantityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_quantity)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 410
            self.match(ProfilesParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class General_setContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def getRuleIndex(self):
            return ProfilesParser.RULE_general_set

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeneral_set" ):
                listener.enterGeneral_set(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeneral_set" ):
                listener.exitGeneral_set(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneral_set" ):
                return visitor.visitGeneral_set(self)
            else:
                return visitor.visitChildren(self)




    def general_set(self):

        localctx = ProfilesParser.General_setContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_general_set)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 412
            self.match(ProfilesParser.T__46)
            self.state = 413
            self.expr(0)
            self.state = 418
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 414
                self.match(ProfilesParser.T__0)
                self.state = 415
                self.expr(0)
                self.state = 420
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 421
            self.match(ProfilesParser.T__47)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Conjunction_of_npContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def noun_phrase(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.Noun_phraseContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.Noun_phraseContext,i)


        def getRuleIndex(self):
            return ProfilesParser.RULE_conjunction_of_np

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConjunction_of_np" ):
                listener.enterConjunction_of_np(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConjunction_of_np" ):
                listener.exitConjunction_of_np(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunction_of_np" ):
                return visitor.visitConjunction_of_np(self)
            else:
                return visitor.visitChildren(self)




    def conjunction_of_np(self):

        localctx = ProfilesParser.Conjunction_of_npContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_conjunction_of_np)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 423
            self.noun_phrase()
            self.state = 428
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,50,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 424
                    self.match(ProfilesParser.T__0)
                    self.state = 425
                    self.noun_phrase() 
                self.state = 430
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,50,self._ctx)

            self.state = 432
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 431
                self.match(ProfilesParser.T__0)


            self.state = 434
            self.match(ProfilesParser.T__1)
            self.state = 435
            self.noun_phrase()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Disjunction_of_npContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def noun_phrase(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.Noun_phraseContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.Noun_phraseContext,i)


        def getRuleIndex(self):
            return ProfilesParser.RULE_disjunction_of_np

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDisjunction_of_np" ):
                listener.enterDisjunction_of_np(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDisjunction_of_np" ):
                listener.exitDisjunction_of_np(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDisjunction_of_np" ):
                return visitor.visitDisjunction_of_np(self)
            else:
                return visitor.visitChildren(self)




    def disjunction_of_np(self):

        localctx = ProfilesParser.Disjunction_of_npContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_disjunction_of_np)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 437
            self.noun_phrase()
            self.state = 442
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,52,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 438
                    self.match(ProfilesParser.T__0)
                    self.state = 439
                    self.noun_phrase() 
                self.state = 444
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,52,self._ctx)

            self.state = 446
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 445
                self.match(ProfilesParser.T__0)


            self.state = 448
            self.match(ProfilesParser.T__2)
            self.state = 449
            self.noun_phrase()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AtomicExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atomic_expr(self):
            return self.getTypedRuleContext(ProfilesParser.Atomic_exprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomicExpr" ):
                listener.enterAtomicExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomicExpr" ):
                listener.exitAtomicExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomicExpr" ):
                return visitor.visitAtomicExpr(self)
            else:
                return visitor.visitChildren(self)


    class DisjunctionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDisjunctionExpr" ):
                listener.enterDisjunctionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDisjunctionExpr" ):
                listener.exitDisjunctionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDisjunctionExpr" ):
                return visitor.visitDisjunctionExpr(self)
            else:
                return visitor.visitChildren(self)


    class FunctionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def function(self):
            return self.getTypedRuleContext(ProfilesParser.FunctionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionExpr" ):
                listener.enterFunctionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionExpr" ):
                listener.exitFunctionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionExpr" ):
                return visitor.visitFunctionExpr(self)
            else:
                return visitor.visitChildren(self)


    class SetExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def general_set(self):
            return self.getTypedRuleContext(ProfilesParser.General_setContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetExpr" ):
                listener.enterSetExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetExpr" ):
                listener.exitSetExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetExpr" ):
                return visitor.visitSetExpr(self)
            else:
                return visitor.visitChildren(self)


    class ConjunctionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProfilesParser.ExprContext)
            else:
                return self.getTypedRuleContext(ProfilesParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConjunctionExpr" ):
                listener.enterConjunctionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConjunctionExpr" ):
                listener.exitConjunctionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunctionExpr" ):
                return visitor.visitConjunctionExpr(self)
            else:
                return visitor.visitChildren(self)


    class AttributeExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def attribute(self):
            return self.getTypedRuleContext(ProfilesParser.AttributeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeExpr" ):
                listener.enterAttributeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeExpr" ):
                listener.exitAttributeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeExpr" ):
                return visitor.visitAttributeExpr(self)
            else:
                return visitor.visitChildren(self)


    class AggregateExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aggregate(self):
            return self.getTypedRuleContext(ProfilesParser.AggregateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAggregateExpr" ):
                listener.enterAggregateExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAggregateExpr" ):
                listener.exitAggregateExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAggregateExpr" ):
                return visitor.visitAggregateExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ProfilesParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class PhraseExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def noun_phrase(self):
            return self.getTypedRuleContext(ProfilesParser.Noun_phraseContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhraseExpr" ):
                listener.enterPhraseExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhraseExpr" ):
                listener.exitPhraseExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhraseExpr" ):
                return visitor.visitPhraseExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ProfilesParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 50
        self.enterRecursionRule(localctx, 50, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 462
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                localctx = ProfilesParser.FunctionExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 452
                self.function()
                pass

            elif la_ == 2:
                localctx = ProfilesParser.AttributeExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 453
                self.attribute()
                pass

            elif la_ == 3:
                localctx = ProfilesParser.PhraseExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 454
                self.noun_phrase()
                pass

            elif la_ == 4:
                localctx = ProfilesParser.AggregateExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 455
                self.aggregate()
                pass

            elif la_ == 5:
                localctx = ProfilesParser.AtomicExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 456
                self.atomic_expr()
                pass

            elif la_ == 6:
                localctx = ProfilesParser.SetExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 457
                self.general_set()
                pass

            elif la_ == 7:
                localctx = ProfilesParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 458
                self.match(ProfilesParser.T__8)
                self.state = 459
                self.expr(0)
                self.state = 460
                self.match(ProfilesParser.T__9)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 472
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,56,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 470
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
                    if la_ == 1:
                        localctx = ProfilesParser.ConjunctionExprContext(self, ProfilesParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 464
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 465
                        self.match(ProfilesParser.T__1)
                        self.state = 466
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = ProfilesParser.DisjunctionExprContext(self, ProfilesParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 467
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 468
                        self.match(ProfilesParser.T__2)
                        self.state = 469
                        self.expr(7)
                        pass

             
                self.state = 474
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,56,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Atomic_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_atomic_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringExprContext(Atomic_exprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Atomic_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(ProfilesParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringExpr" ):
                listener.enterStringExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringExpr" ):
                listener.exitStringExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringExpr" ):
                return visitor.visitStringExpr(self)
            else:
                return visitor.visitChildren(self)


    class TimeExprContext(Atomic_exprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Atomic_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TIME(self):
            return self.getToken(ProfilesParser.TIME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeExpr" ):
                listener.enterTimeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeExpr" ):
                listener.exitTimeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimeExpr" ):
                return visitor.visitTimeExpr(self)
            else:
                return visitor.visitChildren(self)


    class PeriodExprContext(Atomic_exprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Atomic_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def period(self):
            return self.getTypedRuleContext(ProfilesParser.PeriodContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeriodExpr" ):
                listener.enterPeriodExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeriodExpr" ):
                listener.exitPeriodExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPeriodExpr" ):
                return visitor.visitPeriodExpr(self)
            else:
                return visitor.visitChildren(self)


    class QuantityExprContext(Atomic_exprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Atomic_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def quantity(self):
            return self.getTypedRuleContext(ProfilesParser.QuantityContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantityExpr" ):
                listener.enterQuantityExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantityExpr" ):
                listener.exitQuantityExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuantityExpr" ):
                return visitor.visitQuantityExpr(self)
            else:
                return visitor.visitChildren(self)


    class VariableExprContext(Atomic_exprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ProfilesParser.Atomic_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(ProfilesParser.VARIABLE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableExpr" ):
                listener.enterVariableExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableExpr" ):
                listener.exitVariableExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableExpr" ):
                return visitor.visitVariableExpr(self)
            else:
                return visitor.visitChildren(self)



    def atomic_expr(self):

        localctx = ProfilesParser.Atomic_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_atomic_expr)
        try:
            self.state = 480
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                localctx = ProfilesParser.QuantityExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 475
                self.quantity()
                pass

            elif la_ == 2:
                localctx = ProfilesParser.StringExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 476
                self.match(ProfilesParser.STRING)
                pass

            elif la_ == 3:
                localctx = ProfilesParser.VariableExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 477
                self.match(ProfilesParser.VARIABLE)
                pass

            elif la_ == 4:
                localctx = ProfilesParser.TimeExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 478
                self.match(ProfilesParser.TIME)
                pass

            elif la_ == 5:
                localctx = ProfilesParser.PeriodExprContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 479
                self.period()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PeriodContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TIME(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.TIME)
            else:
                return self.getToken(ProfilesParser.TIME, i)

        def getRuleIndex(self):
            return ProfilesParser.RULE_period

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeriod" ):
                listener.enterPeriod(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeriod" ):
                listener.exitPeriod(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPeriod" ):
                return visitor.visitPeriod(self)
            else:
                return visitor.visitChildren(self)




    def period(self):

        localctx = ProfilesParser.PeriodContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_period)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 482
            self.match(ProfilesParser.TIME)
            self.state = 483
            self.match(ProfilesParser.T__48)
            self.state = 484
            self.match(ProfilesParser.TIME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PhraseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def noun_phrase(self):
            return self.getTypedRuleContext(ProfilesParser.Noun_phraseContext,0)


        def verb_phrase(self):
            return self.getTypedRuleContext(ProfilesParser.Verb_phraseContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhrase" ):
                listener.enterPhrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhrase" ):
                listener.exitPhrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhrase" ):
                return visitor.visitPhrase(self)
            else:
                return visitor.visitChildren(self)




    def phrase(self):

        localctx = ProfilesParser.PhraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_phrase)
        try:
            self.state = 488
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,58,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 486
                self.noun_phrase()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 487
                self.verb_phrase()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Noun_phraseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)


        def WORD(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.WORD)
            else:
                return self.getToken(ProfilesParser.WORD, i)

        def getRuleIndex(self):
            return ProfilesParser.RULE_noun_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNoun_phrase" ):
                listener.enterNoun_phrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNoun_phrase" ):
                listener.exitNoun_phrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNoun_phrase" ):
                return visitor.visitNoun_phrase(self)
            else:
                return visitor.visitChildren(self)




    def noun_phrase(self):

        localctx = ProfilesParser.Noun_phraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_noun_phrase)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 491
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3377699720531968) != 0):
                self.state = 490
                self.article()


            self.state = 494 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 493
                    self.match(ProfilesParser.WORD)

                else:
                    raise NoViableAltException(self)
                self.state = 496 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,60,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Verb_phraseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self, i:int=None):
            if i is None:
                return self.getTokens(ProfilesParser.WORD)
            else:
                return self.getToken(ProfilesParser.WORD, i)

        def getRuleIndex(self):
            return ProfilesParser.RULE_verb_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerb_phrase" ):
                listener.enterVerb_phrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerb_phrase" ):
                listener.exitVerb_phrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVerb_phrase" ):
                return visitor.visitVerb_phrase(self)
            else:
                return visitor.visitChildren(self)




    def verb_phrase(self):

        localctx = ProfilesParser.Verb_phraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_verb_phrase)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 499 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 498
                    self.match(ProfilesParser.WORD)

                else:
                    raise NoViableAltException(self)
                self.state = 501 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,61,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Type_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(ProfilesParser.WORD, 0)

        def article(self):
            return self.getTypedRuleContext(ProfilesParser.ArticleContext,0)


        def getRuleIndex(self):
            return ProfilesParser.RULE_type_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType_name" ):
                listener.enterType_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType_name" ):
                listener.exitType_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType_name" ):
                return visitor.visitType_name(self)
            else:
                return visitor.visitChildren(self)




    def type_name(self):

        localctx = ProfilesParser.Type_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_type_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 504
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3377699720531968) != 0):
                self.state = 503
                self.article()


            self.state = 506
            self.match(ProfilesParser.WORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArticleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ProfilesParser.RULE_article

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArticle" ):
                listener.enterArticle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArticle" ):
                listener.exitArticle(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArticle" ):
                return visitor.visitArticle(self)
            else:
                return visitor.visitChildren(self)




    def article(self):

        localctx = ProfilesParser.ArticleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_article)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 508
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3377699720531968) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.condition_sempred
        self._predicates[25] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def condition_sempred(self, localctx:ConditionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 15)
         

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         




