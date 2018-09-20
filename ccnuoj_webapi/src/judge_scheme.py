from .model import JudgeScheme


scheme_cache = {}


def get(id: int):

    if id not in scheme_cache:
        scheme = JudgeScheme.query.get(id)
        context = {
            "judgeScheme": {
                "displayName": scheme.displayName,
                "extraInfo": scheme.extraInfo
            }
        }
        exec(scheme, context, context)
        scheme_cache[id] = context

    return scheme_cache[id]
