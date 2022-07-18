from spacy import displacy, load
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher, Matcher
import app.phrasematch_training as pt
import ast

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
    final_statement = code_statement + " assigns the value of " + str_val + " into a variable named " + str(var_name) + "."
    
    return final_statement

def response(question):
    nlp = load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")

    pt.test_all(matcher, nlp)
        
    doc = nlp(question)
    tokens = question.split()

    code_found = ""
    code_status = False


    start_code = 0
    end_code = 0

    for match_id, start, end in matcher(doc):
        print("Matched based for initialization:", doc[start:end])
        code_found = ""
        for i in range(start, end):
            code_found = code_found + " " + tokens[i]

        start_code = start
        end_code = end
        code_found = code_found[1:]
        code_status = True


    if code_status:
        #tokenizes the code into one token and changes part of speech tag
        with doc.retokenize() as retokenizer:
            attrs = {"POS": "X"}
            retokenizer.merge(doc[start_code:end_code], attrs=attrs)

        
        graph = displacy.render(doc, style="dep")
        with open("graph.html", 'w') as graph_file:
            graph_file.write(graph)

        #creates another matcher to see "what does code mean"
        define_matcher = Matcher(nlp.vocab)
        pattern = [{"LOWER": "what"}, {"LOWER": "does"}, {"POS": "X"}, {"LOWER": "mean"}]
        define_matcher.add("define", [pattern])

        define_status = False

        for match_id, start, end in define_matcher(doc):
            print("Matched based to define:", doc[start:end])
            define_status = True
    
        print("code_found:", code_found)
        if define_status:
            parsed_statement = ast.parse(code_found, mode='exec')
            if isinstance(parsed_statement.body[0], ast.Assign):
                return get_assign_definition(parsed_statement)
        else:
            return "Sorry, I do not understand your question."
    else:
        return "Sorry, I do not understand your question." #change output