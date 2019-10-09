
import re
import xmlrpc.client

import ConverterModule

xmlrpcUrl = "http://localhost:8088/"

def evaluate(data):
    expressionConverter = [{'name' : 'tuple', 'pattern' : "^[(].+[)]$",'expressionMatcher' : re.compile("^[(].+[)]$"), 'converter' : convertToTuple}]
    converted = None

    for r in expressionConverter:
        if (r['expressionMatcher'].match(data)):
            print('matched on: ', r['name'])
            converted = r['converter'](data)
            break

    return converted

def convertToTuple(data):
    return eval(data)
    #formatted = re.sub("^[(]", "", data)
    #formatted = re.sub("[)]$", "", formatted)
    #return tuple(map(lambda s: itemMap(s), formatted.split(',')))

def reConverter(t):
    formatted = t.replace('re.compile(', '')
    formatted = re.sub("[)]$", "", formatted)
    formatted = re.compile(formatted)

def rangeConverter(u):
    formatted = u.replace('range(', '')
    formatted = re.sub("[)]$", "", formatted)
    rangeList = list(map(lambda s: itemMap(s), formatted.split(',')))
    print(type(rangeList), len(rangeList), " r ", rangeList)
    return range(rangeList[0], rangeList[1])

def itemMap(item):
    expressionConverter = [
        {'name' : 'range', 'test' : lambda m:m.startswith('range('), 'converter' : rangeConverter},
        {'name' : 'regex', 'test' : lambda m:m.startswith('re.compile('), 'converter' : reConverter},
        {'name' : 'str', 'test' : lambda i:i.lower()=='str', 'converter' : lambda j:str},
        {'name' : 'int', 'test' : lambda k:k.lower()=='int', 'converter' : lambda l:int},
        {'name' : 'string', 'test' : lambda n:re.match("^['].+[']$", n), 'converter' : lambda o:str(o.replace("'", ''))},
        {'name' : 'numeric', 'test' : lambda p:True, 'converter' : lambda q:int(q)},
    ]
    converted = item.strip()

    print('to be tested: ', converted)

    for converter in expressionConverter:
        if (converter['test'](converted)):
            print('matched on: ', converter['name'])
            converted = converter['converter'](converted)
            break
    
    return converted

doLoop = True
while (doLoop):
    data = input('Expression: ')

    stripped = data.strip()
    if (stripped == 'exit'):
        break
    expr = evaluate(stripped)
    converted = ConverterModule.Converter.tupleToXMLRPCData(expr)
    print('converted: ', converted)

    try:
        with xmlrpc.client.ServerProxy(xmlrpcUrl) as proxy:
            srv = proxy.test
            print(srv.foo(converted))
    except Exception as e:
        print(e)