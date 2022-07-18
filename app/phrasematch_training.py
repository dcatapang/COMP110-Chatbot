from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

def test_all(matcher, nlp):
    word_word(matcher, nlp)
    word_num(matcher, nlp)
    num_word(matcher, nlp)
    num_num(matcher, nlp)
    simple_test(matcher, nlp)

 
def simple_test(matcher, nlp):
    #tests for simple word = num
    code_1 = "a"

    for i in range(8):    
        code_2 = "1"
        code_3 = "2"
        for j in range(8):
            final_code1 = code_1 + " = " + code_2
            final_code2 = code_1 + " = " + code_3
            matcher.add("code", [nlp(final_code1), nlp(final_code2)])
            code_2 += "1"
            code_3 += "2"

        code_1 += "a"

    #tests for simple word = word
    code_1 = "a"

    for i in range(8):    
        code_2 = "b"
        code_3 = "c"
        for j in range(8):
            final_code1 = code_1 + " = " + code_2
            final_code2 = code_1 + " = " + code_3
            matcher.add("code2", [nlp(final_code1), nlp(final_code2)])
            code_2 += "b"
            code_3 += "c"

        code_1 += "a"

def word_word(matcher, nlp):
    symbols = [" + ", " - ", " / ", " // ", " * ", " ** ", " % ", " and ", " or "]
    for sym in symbols:
        code_1 = "a"
        for i in range(8):    
            code_2 = "b"
            code_3 = "c"
            for j in range(8):
                code_4 = "d"
                code_5 = "e"
                for k in range(8):
                    final_code1 = code_1 + " = " + code_2 + sym + code_4
                    final_code2 = code_1 + " = " + code_3 + sym + code_5
                    matcher.add("code3", [nlp(final_code1), nlp(final_code2)])
                    code_4 += "d"
                    code_5 += "e"
                code_2 += "b"
                code_3 += "c"

            code_1 += "a"

def word_num(matcher, nlp):
    symbols = [" + ", " - ", " / ", " // ", " * ", " ** ", " % ", " and ", " or "]
    for sym in symbols:
        code_1 = "a"
        for i in range(8):    
            code_2 = "b"
            code_3 = "c"
            for j in range(8):
                code_4 = "1"
                code_5 = "2"
                for k in range(8):
                    final_code1 = code_1 + " = " + code_2 + sym + code_4
                    final_code2 = code_1 + " = " + code_3 + sym + code_5
                    matcher.add("code4", [nlp(final_code1), nlp(final_code2)])
                    code_4 += "3"
                    code_5 += "4"
                code_2 += "b"
                code_3 += "c"

            code_1 += "a"

def num_word(matcher, nlp):
    symbols = [" + ", " - ", " / ", " // ", " * ", " ** ", " % ", " and ", " or "]
    for sym in symbols:
        code_1 = "a"
        for i in range(8):    
            code_2 = "1"
            code_3 = "2"
            for j in range(8):
                code_4 = "d"
                code_5 = "e"
                for k in range(8):
                    final_code1 = code_1 + " = " + code_2 + sym + code_4
                    final_code2 = code_1 + " = " + code_3 + sym + code_5
                    matcher.add("code5", [nlp(final_code1), nlp(final_code2)])
                    code_4 += "d"
                    code_5 += "e"
                code_2 += "1"
                code_3 += "2"

            code_1 += "a"

def num_num(matcher, nlp):
    symbols = [" + ", " - ", " / ", " // ", " * ", " ** ", " % ", " and ", " or "]
    for sym in symbols:
        code_1 = "a"
        for i in range(8):    
            code_2 = "1"
            code_3 = "2"
            for j in range(8):
                code_4 = "3"
                code_5 = "4"
                for k in range(8):
                    final_code1 = code_1 + " = " + code_2 + sym + code_4
                    final_code2 = code_1 + " = " + code_3 + sym + code_5
                    matcher.add("code6", [nlp(final_code1), nlp(final_code2)])
                    code_4 += "3"
                    code_5 += "4"
                code_2 += "1"
                code_3 += "2"

            code_1 += "a"