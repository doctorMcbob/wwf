import re

class TemplateError(Exception):
    pass

def format_html(html, context):
    print context
    html = re.split(r'{{ | }}', html)    
    for i, text in enumerate(html):
        if i % 2:
            cmds = text.split(" ")
            while True:
                try:
                    var_idx = cmds.index("var")
                    cmds[var_idx + 1] = str(
                        context[cmds[var_idx + 1]])
                    del cmds[var_idx]
                except KeyError:
                    raise TemplateError("{} is not defined".format(
                        cmds[var_idx + 1]
                    ))
                except ValueError:
                    break
            
    
            if cmds[0] == "for":
                tocopy = html[i + 1:html.index("endfor")]
                del html[i + 1:html.index("endfor") + 1]
                var = cmds[1:cmds.index("in")]
                iterable = context[cmds[cmds.index("in") + 1]]
                cmds = []
                
                for item in iterable:
                    con = context.copy()
                    if len(var) == 1:
                        con.update({var[0]: item})
                    else:
                        for t in var:
                            con.update({t: item.pop()})
                    sect = format_html(
                        "{{ ".join(tocopy), con
                    )
                    
                    cmds.append(sect)
            html[i] = " ".join(cmds)

    return "".join(html) 


if __name__ == "__main__":
    text = """
This is text that will be {{ var VERB }}.
{{ for x n in LIST }}
test1
{{ var n }}
{{ var x }}
test2
{{ endfor }}
The end :)
"""

    context = {
        "VERB": "formatted",
        "LIST": [["This", ".."],  ["Is", "A"], ["Loop", "sdfsadf"]]
    }
    print format_html(text, context)
