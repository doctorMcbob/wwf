import re

class TemplateError(Exception):
    pass

def format_html(html, context):
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
                tocopy = html[i + 1:html.index(endfor)]
                var = cmds[1]
                iterable = cmds[3]

                for item in iterable:
                    sect = tocopy
                    # TODO!!

            html[i] = " ".join(cmds)

    return "".join(html) 


if __name__ == "__main__":
    text = """
This is text that will be {{ var VERB }}.
{{ for n in var LIST }}
{{ n }}
{{ endfor }}
The end :)
"""
    print text
    context = {
        "VERB": "formatted",
        "LIST": ["This", "Is", "A", "Loop"]
    }
    print format_html(text, context)
