from spacy import displacy, load
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher, Matcher
import ast
import re

def get_assign_definition(parsed_statement):
    var_name = parsed_statement.body[0].targets[0].id

    var_val = parsed_statement.body[0].value

    str_val = ""

    if isinstance(var_val, ast.BinOp):
        first_val = parsed_statement.body[0].value.left
        operation = parsed_statement.body[0].value.op
        second_val = parsed_statement.body[0].value.right

        #checks for first value in the binary operation
        if isinstance(first_val, ast.Name):
            str_val += first_val.id
        else:
            str_val += str(first_val.s)
    
        #checks for the operator in the binary operation
        operation_dic = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.FloorDiv: "//", ast.Mod: "%", ast.Pow: "**"}
        oper_type = type(operation)
        str_oper = operation_dic[oper_type]

        str_val = str_val + " " + str_oper + " "

        #checks for second value in binary operation
        if isinstance(second_val, ast.Constant):
            str_val += str(second_val.s)
        else:
            str_val += second_val.id

    elif isinstance(var_val, ast.Name):
        str_val = var_val.id
    elif isinstance(var_val, ast.Constant):
        str_val = var_val.s

    code_statement = ast.unparse(parsed_statement)
    final_statement = code_statement + " assigns the value of " + str(str_val) + " into a variable named " + str(var_name) + "."
    
    return final_statement

def create_dictionary():
    
    dictionary = {}
    
    rfile = open("dictionary.txt", "r")
    for line in rfile:
        term = line.strip()
        dictionary[term] = {}
        dictionary[term]['definition'] = rfile.readline().strip()
        dictionary[term]['example'] = rfile.readline().strip()

    return dictionary



def response(question):
    nlp = load("en_core_web_trf")
        
    doc = nlp(question)


    code_found = ""
    code_status = False

    start_code = 0
    end_code = 0

    expression = r"\w+\s*=\s*\w+(\s*[\+\-\*\/]\s*\w+){0,1}"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            print("Found match:", span.text)
        code_found = span.text
        code_status = True
        start_code = span[0].i
        end_code = span[-1].i + 1


    if code_status:
        #tokenizes the code into one token and changes part of speech tag
        with doc.retokenize() as retokenizer:
            attrs = {"POS": "X"}
            retokenizer.merge(doc[start_code:end_code], attrs=attrs)


        #creates another matcher to see "what does code mean"
        define_matcher = Matcher(nlp.vocab)
        pattern = [{"LOWER": "what"}, {"LOWER": "does"}, {"POS": "X"}, {"LOWER": "mean"}]
        define_matcher.add("define", [pattern])

        define_status = False

        for match_id, start, end in define_matcher(doc):
            print("Matched based to define:", doc[start:end])
            define_status = True
    
        if define_status:
            parsed_statement = ast.parse(code_found, mode='exec')
            if isinstance(parsed_statement.body[0], ast.Assign):
                return get_assign_definition(parsed_statement)
        else:
            return "Sorry, I do not understand your question."
    
    #if no code was found, analyze the sentence without the code
    else:

        topics = ["algorithm", "string", "integer", "data type", "operator", "double", "modulus operator", "variable"]
        verbs = ["construct", "create", "make", "do", "find"]
        nsubj_possibilities = ["example", "definition", "meaning", "PSA", "project", "quizz"]
        doc = nlp(question)

        roots = []

        sentence_dictionary = {"attr": "", "nsubj": "", "advmod": "", "root": "", "prep": "", "pobj": "", "dobj": "", "topic": "", "acomp":"" , "nummod":"" }
        topic_dictionary = create_dictionary()

        verb = ""
        attr = ""
        topic = ""
        advmod = ""
        acomp = ""

        needs_example = False
        needs_definition = False
        topic_not_supported = False
        needs_how_to = False 
        needs_event = False

        #finds the root in the sentence
        for tok in doc:
            if tok.dep_ == 'ROOT':
                roots.append(tok)
                verb = tok.text
                if verb == "'s":
                    verb = "is"
                sp_verb = nlp(verb)
                for token in sp_verb:
                    verb_lemma = token.lemma_
                sentence_dictionary["root"] = verb_lemma

        for tok in roots[0].children:
            print(tok.text, tok.lemma_, tok.dep_)

            #check if there is an nsubj
            if tok.dep_ == "attr":
                has_attribute = True
                attr = tok.text
                sentence_dictionary["attr"] = attr
            
            if tok.dep == "acomp":
                acomp = tok.text 
                sentence_dictionary["acomp"] = acomp
                has_acomp = True 

            #collect what nsubj is
            if tok.dep_ == "nsubj":
                sentence_dictionary["topic"] = tok.text
                sentence_dictionary["nsubj"] = tok.text

            if tok.dep_ == "advmod":
                advmod = tok.text
                sentence_dictionary["advmod"] = advmod
                has_adv = True 
            
            if tok.dep_ == "dobj":
                sentence_dictionary["topic"] = tok.text
        
            
        #check if nsubj is in topic list and there is an attribute
        
        if sentence_dictionary["attr"] != "":
            if sentence_dictionary["attr"].lower() == "what" and (sentence_dictionary["root"] == "be"):
                if sentence_dictionary["topic"] not in topics:
                    if sentence_dictionary["topic"].lower() == "example":
                        needs_example = True
                    elif sentence_dictionary["topic"].lower() == "meaning" or sentence_dictionary["topic"].lower() == "definition":
                        needs_definition = True
                    else:
                        needs_definition = True


                    if sentence_dictionary["nsubj"].lower() in nsubj_possibilities:
                        #check if there is a prep based on nsubj
                        new_roots = [tok for tok in doc if tok.dep_ == 'nsubj']
                        for tok in new_roots[0].children:    
                        #check if there is an nsubj
                            if tok.dep_ == "prep":
                                prep_roots = [tok for tok in doc if tok.dep_ == 'prep']
                                for tok in prep_roots[0].children:
                                    if tok.dep_ == "pobj":
                                        topic = tok.text
                                        sentence_dictionary["topic"] = topic
                            elif tok.dep_ == "nummod": 
                                nummod_roots = [tok for tok in doc if tok.dep_ =='nummod']
                                for tok in nummod_roots[0].children:
                                    if tok.dep_ == "nummod":
                                        sentence_dictionary["nummod"] = tok.text
                else:
                    needs_definition = True
        else:
            if sentence_dictionary["advmod"].lower() == "how" and sentence_dictionary["root"].lower() in verbs:
                needs_how_to = True
            elif sentence_dictionary["advmod"].lower() == "when": 
                needs_event = True   

        #checks if the lemmatized version of the
        # topic is in the list
        sp_topic = nlp(sentence_dictionary["topic"])
        lemma_topic = ""
        for token in sp_topic:
            lemma_topic = token.lemma_
        
        if lemma_topic not in topics:
            topic_not_supported = True
    
        #if user is asking for example
        if needs_example:
            if topic_not_supported:
                return "Look at Google for the example of " + sentence_dictionary["topic"]
            else:
                return topic_dictionary[lemma_topic]["example"]
        #if user is asking for definition
        elif needs_definition:
            if topic_not_supported:
                return "Look at Google for the definition of " + sentence_dictionary["topic"]
            else:
                return topic_dictionary[lemma_topic]["definition"]
        #if user is asking how to do something
        elif needs_how_to:
            vowels = ["a", "e", "i", "o", "u"]
            if lemma_topic[0].lower() in vowels:
                prep = "an"
            else:
                prep = "a"

            if topic_not_supported:
                return "Look at Google on " + sentence_dictionary["advmod"] + " to "  + sentence_dictionary["root"] + " " + prep + " " + sentence_dictionary["topic"]
            else:
                return "This is " + sentence_dictionary["advmod"] + " to " + sentence_dictionary["root"] + " " + prep + " " + lemma_topic
        else:
            return "You should probably ask Google." 


        