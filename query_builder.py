import requests

''' MAP OF TERMS
fulltext - > put in () comma separated          IF THERE ARE MULTIPLE, THEY ARE WITHING THE SAME (()) 
docname -> docname : "term"  OR                 SO WE HAVE 
appno - > appno : "term"   OR                   (A OR B) AND (C OR D)
scl -> scl : "term"   OR
rulesofcourt -> rulesofcourt : "term"  OR
applicability -> applicability = "term"  OR
ecli - > ecli : "term"  OR ??
conclusion -> conclusion : "term" OR
resolutionnumber -> resolutionnumber : "term" OR ?? 
kpdate - >  (kpdate>="first_term" AND kpdate<="second_term")   single quotes here ()
separateopinions -> separateopinions = "term" OR
externalsources - > externalsources : "term" OR
kpthesaurus -> kpthesaurus  = "term" OR
advopidentifier -> advopidentifier = "term" OR
documentcollectionid2 - > documentcollectionid2 = "term" OR


bodyprocedure -> ("PROCEDURE" ONEAR(n=1000) term,term OR "PROCÉDURE" ONEAR(n=1000) term,term) bodyfacts -> ("THE 
FACTS" ONEAR(n=1000) term,term OR "EN FAIT" ONEAR(n=1000) term,term) bodycomplaints -> ("COMPLAINTS" ONEAR(n=1000) 
term, term OR "GRIEFS" ONEAR(n=1000) term, term) bodylaw - >  ("THE LAW" ONEAR(n=1000) term,term OR "EN DROIT" ONEAR(
n=1000) term,term) bodyreasons -> ("FOR THESE REASONS" ONEAR(n=1000) term,term OR "PAR CES MOTIFS" ONEAR(n=1000) 
term,term) bodyseparateopinions -> (("SEPARATE OPINION" OR "SEPARATE OPINIONS") ONEAR(n=5000) term,term OR "OPINION 
SÉPARÉE" ONEAR(n=5000) term,term) bodyappendix -> ("APPENDIX" ONEAR(n=1000) term,term OR "ANNEXE" ONEAR(n=1000) term,
term) 


'''


def link_to_query(link):
    extra_cases_map = {
        "bodyprocedure": '("PROCEDURE" ONEAR(n=1000) terms OR "PROCÉDURE" ONEAR(n=1000) terms)',
        "bodyfacts": '("THE FACTS" ONEAR(n=1000) terms OR "EN FAIT" ONEAR(n=1000) terms)',
        "bodycomplaints": '("COMPLAINTS" ONEAR(n=1000) terms OR "GRIEFS" ONEAR(n=1000) terms)',
        "bodylaw": '("THE LAW" ONEAR(n=1000) terms OR "EN DROIT" ONEAR(n=1000) terms)',
        "bodyreasons": '("FOR THESE REASONS" ONEAR(n=1000) terms OR "PAR CES MOTIFS" ONEAR(n=1000) terms)',
        "bodyseparateopinions": '(("SEPARATE OPINION" OR "SEPARATE OPINIONS") ONEAR(n=5000) terms OR "OPINION '
                                'SÉPARÉE" ONEAR(n=5000) terms)',
        "bodyappendix": '("APPENDIX" ONEAR(n=1000) terms OR "ANNEXE" ONEAR(n=1000) terms)'
    }

    def basic_function(term, values):
        values = ['"' + i + '"' for i in values]
        main_body = list()
        cut_term = term.replace('"', '')
        for v in values:
            main_body.append(f"({cut_term}={v}) OR ({cut_term}:{v})")
        query = f"({' OR '.join(main_body)})"
        return query

    def full_text_function(term, values):
        return f"({','.join(values)})"

    def date_function(term, values):
        values = ['"' + i + '"' for i in values]
        query = '(kpdate >= "first_term" AND kpdate <= "second_term")'
        query = query.replace("first_term", values[0])
        query = query.replace("second_term", values[1])
        return query

    def advanced_function(term, values):
        body = extra_cases_map.get(term)
        query = body.replace("terms", ",".join(vals))
        return query

    query_map = {
        "docname": basic_function,
        "appno": basic_function,
        "scl": basic_function,
        "rulesofcourt": basic_function,
        "applicability": basic_function,
        "ecli": basic_function,
        "conclusion": basic_function,
        "resolutionnumber": basic_function,
        "separateopinions": basic_function,
        "externalsources": basic_function,
        "kpthesaurus": basic_function,
        "advopidentifier": basic_function,
        "documentcollectionid2": basic_function,
        "fulltext": full_text_function,
        "kpdate": date_function,
        "bodyprocedure": advanced_function,
        "bodyfacts": advanced_function,
        "bodycomplaints": advanced_function,
        "bodylaw": advanced_function,
        "bodyreasons": advanced_function,
        "bodyseparateopinions": advanced_function,
        "bodyappendix": advanced_function

    }
    start = link.index("{")
    link_dictionary = eval(link[start:])
    base_query = 'https://hudoc.echr.coe.int/app/query/results?query=contentsitename:ECHR AND ' \
                 'inPutter&select=itemid&sort=itemid%20Ascending&length=4000'
    query_elements = list()
    for key in list(link_dictionary.keys()):
        vals = link_dictionary.get(key)
        funct = query_map.get(key)
        query_elements.append(funct(key, vals))
    query_total = ' AND '.join(query_elements)
    final_query = base_query.replace('inPutter', query_total)
    print(final_query)
    page = requests.get(final_query)
    results = eval(page.text)
    print(results.get('resultcount'))


tester = 'https://hudoc.echr.coe.int/eng#{"documentcollectionid2":["JUDGMENTS","DECISIONS"],"bodycomplaints":["test"]}'
link_to_query(tester)
