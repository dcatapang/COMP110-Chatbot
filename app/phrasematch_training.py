from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

def test_all(matcher, nlp):
    define_training(matcher, nlp)
    print("finished define training")
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

def define_training(matcher, nlp):
    symbols = [" + ", " - ", " / ", " // ", " * ", " ** ", " % "]
    for sym in symbols:
        code_1 = "a"
        for i in range(8):    
            code_2 = "b"
            code_3 = "c"
            code_8 = "1"
            code_9 = "2"
            for j in range(8):
                code_4 = "d"
                code_5 = "e"
                code_6 = "1"
                code_7 = "2"
                for k in range(8):
                    final_code1 = code_1 + " = " + code_2 + sym + code_4
                    final_code2 = code_1 + " = " + code_3 + sym + code_5
                    final_code3 = code_1 + " = " + code_2 + sym + code_6
                    final_code4 = code_1 + " = " + code_3 + sym + code_7
                    final_code5 = code_1 + " = " + code_8 + sym + code_4
                    final_code6 = code_1 + " = " + code_9 + sym + code_5
                    final_code7 = code_1 + " = " + code_8 + sym + code_6
                    final_code8 = code_1 + " = " + code_9 + sym + code_7
                    print("adding to word_word")
                    matcher.add("code3", [nlp(final_code1), nlp(final_code2)]) #how to do this in different processors
                    matcher.add("code4", [nlp(final_code3), nlp(final_code4)]) #how to do this in different processors
                    matcher.add("code5", [nlp(final_code5), nlp(final_code6)]) #how to do this in different processors
                    matcher.add("code6", [nlp(final_code7), nlp(final_code8)]) #how to do this in different processors
                    code_4 += "d"
                    code_5 += "e"
                    code_6 += "3"
                    code_7 += "4"
                code_2 += "b"
                code_3 += "c"
                code_8 += "1"
                code_9 += "2"

            code_1 += "a"